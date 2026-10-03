"""Opt-in text Q&A. No filesystem access, environment keys, tools or fallback."""
import http.client
import json
import re
import secrets
import threading
import time
from urllib.parse import quote

HOST = "api.openai.com"
TTL = 1800
MAX_REQUESTS = 20
MAX_SESSIONS = 8

class CloudError(Exception):
    def __init__(self, code, status=400):
        self.code, self.status = code, status
        super().__init__(code)

class OpenAITransport:
    def request(self, method, path, key, body=None):
        # No redirects, proxy destinations or user-provided hosts.
        connection = http.client.HTTPSConnection(HOST, timeout=30)
        try:
            raw = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
            connection.request(method, path, raw, {
                "Authorization": "Bearer " + key, "Content-Type": "application/json"})
            response = connection.getresponse()
            data = response.read(1048577)
            if response.status != 200:
                code = {401: "API_KEY_REJECTED", 403: "API_ACCESS_DENIED",
                        404: "MODEL_UNAVAILABLE", 429: "API_LIMIT"}.get(response.status, "API_FAILURE")
                raise CloudError(code, 502)
            if len(data) > 1048576:
                raise CloudError("API_RESPONSE_TOO_LARGE", 502)
            parsed = json.loads(data)
            if not isinstance(parsed, dict):
                raise ValueError()
            return parsed
        except CloudError:
            raise
        except (OSError, ValueError, http.client.HTTPException):
            raise CloudError("API_CONNECTION_FAILED", 502) from None
        finally:
            connection.close()

    def check(self, key, model):
        answer = self.request("GET", "/v1/models/" + quote(model, safe=""), key)
        if answer.get("id") != model:
            raise CloudError("MODEL_UNAVAILABLE", 502)

    def answer(self, key, model, messages, limit):
        result = self.request("POST", "/v1/responses", key, {
            "model": model, "input": messages, "max_output_tokens": limit,
            "store": False,
            "instructions": "Responde a la pregunta del usuario. No tienes herramientas ni acceso a archivos, "
                            "proyectos, pedidos o credenciales. No afirmes haber ejecutado acciones."
        })
        parts = []
        output = result.get("output")
        if not isinstance(output, list):
            raise CloudError("API_NO_TEXT", 502)
        for item in output:
            if isinstance(item, dict) and item.get("type") == "message":
                contents = item.get("content")
                if not isinstance(contents, list):
                    raise CloudError("API_NO_TEXT", 502)
                for content in contents:
                    if isinstance(content, dict) and content.get("type") in {"output_text", "refusal"}:
                        value = content.get("text", content.get("refusal", ""))
                        if isinstance(value, str):
                            parts.append(value)
        text = "\n".join(parts).strip()
        if not text or len(text) > 12000:
            raise CloudError("API_NO_TEXT", 502)
        state = result.get("status", "completed")
        if state not in {"completed", "incomplete"}:
            raise CloudError("API_FAILURE", 502)
        usage = result.get("usage") or {}
        clean_usage = {name: usage[name] for name in ("input_tokens", "output_tokens", "total_tokens")
                       if isinstance(usage, dict) and type(usage.get(name)) is int and usage[name] >= 0}
        return {"text": text, "incomplete": state == "incomplete", "usage": clean_usage}

class CloudSessions:
    def __init__(self, transport=None, clock=time.monotonic):
        self.transport = transport or OpenAITransport()
        self.clock = clock
        self.sessions = {}
        self.lock = threading.RLock()
        self.connecting = 0

    def _prune(self):
        expired = [token for token, row in self.sessions.items() if self.clock() - row["touched"] >= TTL]
        for token in expired:
            row = self.sessions.pop(token)
            row["key"] = ""
            row["history"].clear()

    def _session(self, token):
        self._prune()
        if not isinstance(token, str) or token not in self.sessions:
            raise CloudError("SESSION_EXPIRED", 401)
        return self.sessions[token]

    def connect(self, body):
        if set(body) != {"api_key", "model", "max_output_tokens", "consent"} or body.get("consent") is not True:
            raise CloudError("CONSENT_REQUIRED")
        key, model, limit = body["api_key"], body["model"], body["max_output_tokens"]
        if not isinstance(key, str) or not 20 <= len(key) <= 300 or not re.fullmatch(r"[A-Za-z0-9_-]+", key):
            raise CloudError("INVALID_KEY_FORMAT")
        if not isinstance(model, str) or not re.fullmatch(r"[A-Za-z0-9._:-]{1,100}", model):
            raise CloudError("INVALID_MODEL")
        if type(limit) is not int or limit not in {256, 512, 1024}:
            raise CloudError("INVALID_OUTPUT_LIMIT")
        with self.lock:
            self._prune()
            if len(self.sessions) + self.connecting >= MAX_SESSIONS:
                raise CloudError("SESSION_CAPACITY", 429)
            self.connecting += 1
        try:
            self.transport.check(key, model)
            token = secrets.token_urlsafe(32)
            with self.lock:
                self.sessions[token] = {"key": key, "model": model, "limit": limit, "history": [],
                                        "touched": self.clock(), "requests": 0, "busy": False}
        finally:
            with self.lock:
                self.connecting -= 1
        return {"session_id": token, "model": model, "max_output_tokens": limit,
                "expires_after_idle_seconds": TTL, "request_limit": MAX_REQUESTS}

    def ask(self, body):
        if set(body) != {"session_id", "message"}:
            raise CloudError("INVALID_CHAT_REQUEST")
        message = body["message"]
        if not isinstance(message, str) or not message.strip() or len(message) > 2000:
            raise CloudError("INVALID_MESSAGE")
        token = body["session_id"]
        with self.lock:
            row = self._session(token)
            if row["busy"]:
                raise CloudError("REQUEST_IN_PROGRESS", 409)
            if row["requests"] >= MAX_REQUESTS:
                raise CloudError("SESSION_REQUEST_LIMIT", 429)
            row["busy"] = True
            row["requests"] += 1
            row["touched"] = self.clock()
            messages = list(row["history"]) + [{"role": "user", "content": message.strip()}]
            key, model, limit = row["key"], row["model"], row["limit"]
        try:
            answer = self.transport.answer(key, model, messages, limit)
            if not isinstance(answer, dict) or not isinstance(answer.get("text"), str):
                raise CloudError("API_NO_TEXT", 502)
            with self.lock:
                if self.sessions.get(token) is not row:
                    raise CloudError("SESSION_EXPIRED", 401)
                history = messages + [{"role": "assistant", "content": answer["text"]}]
                history = history[-16:]
                while len(history) > 2 and sum(len(m["content"]) for m in history) > 24000:
                    history = history[2:]
                row["history"] = history
                row["touched"] = self.clock()
                return {**answer, "model": model, "requests_used": row["requests"],
                        "request_limit": MAX_REQUESTS}
        finally:
            with self.lock:
                row["busy"] = False

    def clear(self, body):
        if set(body) != {"session_id"}:
            raise CloudError("INVALID_CHAT_REQUEST")
        with self.lock:
            row = self._session(body["session_id"])
            if row["busy"]:
                raise CloudError("REQUEST_IN_PROGRESS", 409)
            row["history"].clear()
            row["touched"] = self.clock()
        return {"status": "HISTORY_CLEARED"}

    def disconnect(self, body):
        if set(body) != {"session_id"} or not isinstance(body["session_id"], str):
            raise CloudError("INVALID_CHAT_REQUEST")
        with self.lock:
            row = self.sessions.pop(body["session_id"], None)
            if row:
                row["key"] = ""
                row["history"].clear()
        return {"status": "DISCONNECTED"}
