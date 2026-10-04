"""Fixed remote MCP adapter. No shell, arbitrary URLs or model-directed tools."""
import http.client
import json
import secrets
import threading
import time
import uuid
from .cloud import CloudError

TOOLS = {"resolve-library-id", "query-docs"}
VERSION = "2025-11-25"

class Context7Transport:
    def exchange(self, payload, key="", session=None, version=VERSION):
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if key:
            headers["Authorization"] = "Bearer " + key
        if session:
            headers["Mcp-Session-Id"] = session
        if payload.get("method") != "initialize":
            headers["MCP-Protocol-Version"] = version
        connection = http.client.HTTPSConnection("mcp.context7.com", timeout=25)
        try:
            connection.request("POST", "/mcp", json.dumps(payload), headers)
            response = connection.getresponse()
            if response.status not in {200, 202, 204}:
                raise CloudError({401: "MCP_AUTH_REQUIRED", 403: "MCP_AUTH_REQUIRED", 429: "MCP_RATE_LIMIT"}.get(response.status, "MCP_REMOTE_ERROR"), 502)
            raw = response.read(262145)
            if len(raw) > 262144:
                raise CloudError("MCP_RESPONSE_TOO_LARGE", 502)
            remote_session = response.getheader("Mcp-Session-Id") or session
            if "id" not in payload:
                return None, remote_session
            text = raw.decode("utf-8")
            if "text/event-stream" in (response.getheader("Content-Type") or ""):
                values = []
                for event in text.replace("\r\n", "\n").split("\n\n"):
                    lines = [line[5:].lstrip() for line in event.splitlines() if line.startswith("data:")]
                    if lines:
                        values.append(json.loads("\n".join(lines)))
                result = next((v for v in values if isinstance(v, dict) and v.get("id") == payload["id"]), None)
            else:
                result = json.loads(text)
            if not isinstance(result, dict) or result.get("id") != payload["id"] or result.get("jsonrpc") != "2.0" or "error" in result or not isinstance(result.get("result"), dict):
                raise CloudError("MCP_INVALID_RESPONSE", 502)
            return result["result"], remote_session
        except CloudError:
            raise
        except (OSError, ValueError, http.client.HTTPException):
            raise CloudError("MCP_CONNECTION_FAILED", 502) from None
        finally:
            connection.close()

class Context7Sessions:
    def __init__(self, transport=None, clock=time.monotonic):
        self.transport = transport or Context7Transport()
        self.clock, self.sessions, self.lock = clock, {}, threading.RLock()
        self.connecting = 0

    def prune(self):
        for token in list(self.sessions):
            if self.clock() - self.sessions[token]["touched"] >= 1800:
                self.sessions.pop(token)["key"] = ""

    def rpc(self, row, method, params=None, notification=False):
        payload = {"jsonrpc": "2.0", "method": method}
        if not notification:
            payload["id"] = str(uuid.uuid4())
        if params is not None:
            payload["params"] = params
        result, session = self.transport.exchange(payload, row["key"], row.get("remote"), row.get("version", VERSION))
        row["remote"] = session
        return result

    def connect(self, body):
        if set(body) != {"api_key", "consent"} or body.get("consent") is not True:
            raise CloudError("MCP_CONSENT_REQUIRED")
        key = body["api_key"]
        if not isinstance(key, str) or len(key) > 300 or any(ord(c) < 33 or ord(c) > 126 for c in key):
            raise CloudError("MCP_INVALID_KEY")
        with self.lock:
            self.prune()
            if len(self.sessions) + self.connecting >= 8:
                raise CloudError("MCP_CAPACITY", 429)
            self.connecting += 1
        row = {"key": key, "busy": False, "touched": self.clock(), "requests": 0}
        try:
            result = self.rpc(row, "initialize", {"protocolVersion": VERSION, "capabilities": {}, "clientInfo": {"name": "ai-implementation-lab", "version": "0.6"}})
            if result.get("protocolVersion") not in {VERSION, "2025-06-18", "2025-03-26", "2024-11-05"}:
                raise CloudError("MCP_PROTOCOL_UNSUPPORTED", 502)
            row["version"] = result["protocolVersion"]
            self.rpc(row, "notifications/initialized", notification=True)
            found = self.rpc(row, "tools/list")
            available = {t.get("name") for t in found.get("tools", []) if isinstance(t, dict) and isinstance(t.get("name"), str)}
            if not TOOLS <= available:
                raise CloudError("MCP_TOOLS_MISSING", 502)
            token = secrets.token_urlsafe(32)
            with self.lock:
                self.sessions[token] = row
            return {"session_id": token, "tools": sorted(TOOLS), "protocol": row["version"], "expires_after_idle_seconds": 1800, "destination": "https://mcp.context7.com/mcp"}
        finally:
            with self.lock:
                self.connecting -= 1

    def call(self, body):
        if set(body) != {"session_id", "tool", "arguments", "consent"} or body.get("consent") is not True:
            raise CloudError("MCP_CONSENT_REQUIRED")
        tool, args, token = body["tool"], body["arguments"], body["session_id"]
        if not isinstance(tool, str) or tool not in TOOLS or not isinstance(args, dict):
            raise CloudError("MCP_TOOL_BLOCKED")
        fields = {"libraryName", "query"} if tool == "resolve-library-id" else {"libraryId", "query"}
        if set(args) != fields or not all(isinstance(v, str) and 1 <= len(v.strip()) <= 1000 for v in args.values()):
            raise CloudError("MCP_INVALID_ARGUMENTS")
        if tool == "query-docs" and not args["libraryId"].startswith("/"):
            raise CloudError("MCP_INVALID_ARGUMENTS")
        with self.lock:
            self.prune()
            if not isinstance(token, str) or token not in self.sessions:
                raise CloudError("MCP_SESSION_EXPIRED", 401)
            row = self.sessions[token]
            if row["busy"]:
                raise CloudError("MCP_BUSY", 409)
            if row["requests"] >= 20:
                raise CloudError("MCP_REQUEST_LIMIT", 429)
            row.update(busy=True, touched=self.clock(), requests=row["requests"] + 1)
        try:
            result = self.rpc(row, "tools/call", {"name": tool, "arguments": args})
            if result.get("isError"):
                raise CloudError("MCP_TOOL_FAILED", 502)
            content = result.get("content")
            if not isinstance(content, list):
                raise CloudError("MCP_INVALID_RESPONSE", 502)
            text = "\n".join(c["text"] for c in content if isinstance(c, dict) and c.get("type") == "text" and isinstance(c.get("text"), str))
            if not text.strip():
                raise CloudError("MCP_NO_TEXT", 502)
            with self.lock:
                if self.sessions.get(token) is not row:
                    raise CloudError("MCP_SESSION_EXPIRED", 401)
                row["touched"] = self.clock()
            return {"text": text[:12000], "truncated": len(text) > 12000, "tool": tool, "arguments": args, "source": "https://mcp.context7.com/mcp", "requests_used": row["requests"]}
        finally:
            with self.lock:
                row["busy"] = False

    def disconnect(self, body):
        if set(body) != {"session_id"} or not isinstance(body["session_id"], str):
            raise CloudError("MCP_INVALID_ARGUMENTS")
        with self.lock:
            row = self.sessions.pop(body["session_id"], None)
            if row:
                row["key"] = ""
        return {"status": "DISCONNECTED"}
