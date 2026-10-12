"""Loopback-only viewer. Never use this development server on a public host.

R55a / D46 / D51: the number of connections handled at once is bounded before a thread exists or a byte is
read (the excess gets 503 on the socket), each handler has a socket inactivity timeout and a total deadline to
deliver the request line, headers and body, and every unexpected exception becomes a fixed error code with no
message (R54c). Host and Origin checks are a same-origin boundary for browsers, not authentication against
other processes on the same computer.
"""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from .controller import Lab, ROOT, load_data
from .models import RuleError
from .cloud import CloudSessions, CloudError
from .agents import contracts, run_agent
from .context7 import Context7Sessions
from .agent_store import AgentStore
from .model_catalog import catalog
from scripts.sdd_check import requirement_rows
from scripts.revision import status_payload

MAX_ACTIVE = 8          # connections handled at once; the ninth gets 503 SERVER_BUSY before any thread or byte
READ_TIMEOUT = 10       # seconds without bytes from the client before 408 REQUEST_TIMEOUT
REQUEST_DEADLINE = 30   # seconds from accept to the end of the body, whatever the pace of the bytes
BUSY = (b"HTTP/1.0 503 Service Unavailable\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: 24\r\n"
        b"Cache-Control: no-store\r\nConnection: close\r\n\r\n{\"error\": \"SERVER_BUSY\"}")
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; "
       "object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
BODY_LIMITS = {"/api/agents/run": 100000, "/api/custom-agents/save": 20000}
ASSETS = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "application/javascript"),
          "/workbench.js": ("workbench.js", "application/javascript"), "/studio.js": ("studio.js", "application/javascript"),
          "/evidence.js": ("evidence.js", "application/javascript"), "/evidence-rules.js": ("evidence-rules.js", "application/javascript"),
          "/orientation.js": ("orientation.js", "application/javascript"), "/style.css": ("style.css", "text/css"),
          "/cloud.js": ("cloud.js", "application/javascript"), "/i18n.js": ("i18n.js", "application/javascript"),
          "/sensitive-rules.js": ("sensitive-rules.js", "application/javascript")}


class DeadlineReader:
    """R55a / D51 / D55: reads on the raw socket; every receive waits at most min(inactivity, time remaining).

    The request line, the headers and the body all come through here, so neither silence nor a continuous trickle
    (within one line or within the body) can hold a handler past the deadline."""

    def __init__(self, connection, deadline, inactivity, chunk=65536):
        self.connection, self.deadline, self.inactivity, self.chunk = connection, deadline, inactivity, chunk
        self.buffer = b""
        self.closed = False

    def _recv(self):
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("request deadline")
        self.connection.settimeout(min(self.inactivity, remaining))
        data = self.connection.recv(self.chunk)
        if not data:
            self.closed = True
        return data

    def readline(self, limit=-1):
        while True:
            index = self.buffer.find(b"\n")
            if index >= 0 and (limit < 0 or index < limit):
                line, self.buffer = self.buffer[:index + 1], self.buffer[index + 1:]
                return line
            if limit >= 0 and len(self.buffer) >= limit:
                line, self.buffer = self.buffer[:limit], self.buffer[limit:]
                return line
            if self.closed or not self._recv_into():
                line, self.buffer = self.buffer, b""
                return line

    def read(self, size=-1):
        while (size < 0 or len(self.buffer) < size) and not self.closed:
            if not self._recv_into():
                break
        if size < 0:
            data, self.buffer = self.buffer, b""
        else:
            data, self.buffer = self.buffer[:size], self.buffer[size:]
        return data

    def _recv_into(self):
        data = self._recv()
        self.buffer += data
        return bool(data)

    def close(self):
        self.buffer = b""


class LabServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 16   # listen backlog: a queue of accepted-but-unserved connections, not a cap

    def __init__(self, address, handler, max_active=MAX_ACTIVE):
        super().__init__(address, handler)
        self.slots = threading.BoundedSemaphore(max_active)
        self.refused = 0

    def process_request(self, request, client_address):
        # R55a / D51: the cap is applied here, before a thread is created and before any byte is read.
        if not self.slots.acquire(blocking=False):
            self.refused += 1
            try:
                request.sendall(BUSY)
            except OSError:
                pass
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()

    def handle_error(self, request, client_address):
        # R54c: nothing from the exception (a provider message could carry the key) reaches standard error.
        print("Request handling failed; details withheld (R54c)", file=sys.stderr, flush=True)


def make_server(port=8765, cloud=None, mcp=None, agent_store=None, max_active=MAX_ACTIVE, read_timeout=READ_TIMEOUT, deadline=REQUEST_DEADLINE):
    lab = Lab()
    cloud = cloud or CloudSessions()
    mcp = mcp or Context7Sessions()
    agent_store = agent_store or AgentStore(ROOT / ".local/agents.json")

    class Handler(BaseHTTPRequestHandler):
        timeout = read_timeout

        def setup(self):
            super().setup()
            self.rfile = DeadlineReader(self.connection, time.monotonic() + deadline, read_timeout)
            self.command, self.requestline, self.request_version = "", "", self.default_request_version

        def log_message(self, *_):
            pass

        def respond(self, code, payload, mime="application/json"):
            raw = json.dumps(payload).encode() if mime == "application/json" else payload
            self.send_response(code)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", CSP)
            self.end_headers()
            self.wfile.write(raw)

        def trusted(self):
            hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            origin = self.headers.get("Origin")
            return self.headers.get("Host") in hosts and (origin is None or origin in {"http://" + h for h in hosts})

        def guarded(self, action):
            try:
                action()
            except TimeoutError:
                self.close_connection = True
                self.respond(408, {"error": "REQUEST_TIMEOUT"})
            except Exception:  # noqa: BLE001 - R54c: fixed envelope, no message
                self.close_connection = True
                self.respond(500, {"error": "INTERNAL_ERROR"})

        def handle_one_request(self):
            # Same steps as BaseHTTPRequestHandler.handle_one_request, but an inactivity timeout or the deadline
            # while reading the request line or the headers answers 408 instead of closing silently (R55a, D51).
            try:
                self.raw_requestline = self.rfile.readline(65537)
                if len(self.raw_requestline) > 65536:
                    self.send_error(414)
                    return
                if not self.raw_requestline:
                    self.close_connection = True
                    return
                if not self.parse_request():
                    return
                method = getattr(self, "do_" + self.command, None)
                if method is None:
                    self.send_error(501, "Unsupported method (%r)" % self.command)
                    return
                method()
                self.wfile.flush()
            except TimeoutError:
                self.close_connection = True
                try:
                    self.respond(408, {"error": "REQUEST_TIMEOUT"})
                except OSError:
                    pass

        def do_GET(self):
            self.guarded(self.get)

        def do_POST(self):
            self.guarded(self.post)

        def get(self):
            if not self.trusted():
                return self.respond(403, {"error": "HOST_OR_ORIGIN_BLOCKED"})
            path = urlsplit(self.path).path
            if path == "/api/model-catalog":
                return self.respond(200, catalog())
            if path == "/api/state":
                return self.respond(200, lab.snapshot())
            if path == "/api/scenarios":
                return self.respond(200, load_data("scenarios.json"))
            if path == "/api/custom-agents":
                try:
                    return self.respond(200, agent_store.list())
                except CloudError as exc:
                    return self.respond(exc.status, {"error": exc.code})
            if path == "/api/agents":
                return self.respond(200, contracts())
            # Read-only traceability data: fixed files, no request parameters.
            if path == "/api/evidence":
                return self.respond(200, json.loads((ROOT / "evidence/latest.json").read_text(encoding="utf-8")))
            if path == "/api/acceptance":
                return self.respond(200, (ROOT / "specs/001-support-demo/acceptance.csv").read_bytes(), "text/csv")
            if path == "/api/status":
                # R36b, R42, R43a: project records, fingerprints and the Git revision of this checkout.
                return self.respond(200, status_payload())
            if path == "/api/requirements":
                return self.respond(200, requirement_rows((ROOT / "specs/001-support-demo/spec.md").read_text(encoding="utf-8")))
            if path in ASSETS:
                filename, mime = ASSETS[path]
                return self.respond(200, (ROOT / "web" / filename).read_bytes(), mime)
            self.respond(404, {"error": "NOT_FOUND"})

        def post(self):
            if not self.trusted():
                return self.respond(403, {"error": "HOST_OR_ORIGIN_BLOCKED"})
            if self.headers.get("Content-Type") != "application/json":
                return self.respond(415, {"error": "JSON_REQUIRED"})
            path = urlsplit(self.path).path
            try:
                length = int(self.headers.get("Content-Length", "0"))
                body_limit = BODY_LIMITS.get(path, 16384 if path.startswith(("/api/cloud/", "/api/mcp/")) else 4096)
                if not 0 < length <= body_limit:
                    return self.respond(413, {"error": "INVALID_BODY_SIZE"})
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError()
            except (ValueError, UnicodeError, RecursionError):
                return self.respond(400, {"error": "INVALID_JSON"})
            try:
                if path == "/api/custom-agents/save":
                    return self.respond(200, agent_store.save(body))
                if path == "/api/cloud/ask" and set(body) == {"session_id", "message", "agent_id"}:
                    instructions, context_id = agent_store.resolve(body["agent_id"])
                    return self.respond(200, cloud.ask({"session_id": body["session_id"], "message": body["message"]}, instructions, context_id))
                if path == "/api/agents/run":
                    return self.respond(200, run_agent(body, cloud))
                if path.startswith("/api/mcp/"):
                    handlers = {"/api/mcp/connect": mcp.connect, "/api/mcp/call": mcp.call, "/api/mcp/disconnect": mcp.disconnect}
                    if path not in handlers:
                        return self.respond(404, {"error": "NOT_FOUND"})
                    return self.respond(200, handlers[path](body))
                if path.startswith("/api/cloud/"):
                    handlers = {"/api/cloud/connect": cloud.connect, "/api/cloud/ask": cloud.ask,
                                "/api/cloud/configure": cloud.configure, "/api/cloud/clear": cloud.clear, "/api/cloud/disconnect": cloud.disconnect}
                    if path not in handlers:
                        return self.respond(404, {"error": "NOT_FOUND"})
                    return self.respond(200, handlers[path](body))
                if path == "/api/request":
                    result = lab.request(body)
                elif path == "/api/decision" and set(body) == {"proposal_id", "decision"}:
                    if not all(isinstance(v, str) for v in body.values()):
                        raise ValueError()
                    result = lab.decide(body["proposal_id"], body["decision"], "human_reviewer")
                elif path == "/api/execute" and set(body) <= {"proposal_id", "fail_connector"} and "proposal_id" in body:
                    if not isinstance(body["proposal_id"], str) or type(body.get("fail_connector", False)) is not bool:
                        raise ValueError()
                    result = lab.execute(body["proposal_id"], body.get("fail_connector", False))
                else:
                    return self.respond(400, {"error": "INVALID_ACTION"})
                self.respond(200, result)
            except CloudError as exc:
                self.respond(exc.status, {"error": exc.code})
            except RuleError as exc:
                self.respond(409, {"status": "BLOCKED", "reason": exc.code})
            except (TypeError, ValueError):
                self.respond(400, {"error": "INVALID_ARGUMENTS"})

    return LabServer(("127.0.0.1", port), Handler, max_active=max_active)


def serve(port=8765):
    server = make_server(port)
    print(f"Local demo: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
