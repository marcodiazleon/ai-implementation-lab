"""Loopback-only viewer. Never use this development server on a public host.

R55a / D46: each handler has a socket read timeout, the number of handlers working at once is bounded by a
semaphore that refuses instead of queueing, and every unexpected exception becomes a fixed error code with no
message (R54c). Host and Origin checks are a same-origin boundary for browsers, not authentication against
other processes on the same computer.
"""
import json
import sys
import threading
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

MAX_ACTIVE = 8          # handlers working at once; the ninth gets 503 SERVER_BUSY
READ_TIMEOUT = 10       # seconds without bytes from the client before 408 REQUEST_TIMEOUT
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self'; "
       "object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
BODY_LIMITS = {"/api/agents/run": 100000, "/api/custom-agents/save": 20000}
ASSETS = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "application/javascript"),
          "/workbench.js": ("workbench.js", "application/javascript"), "/studio.js": ("studio.js", "application/javascript"),
          "/evidence.js": ("evidence.js", "application/javascript"), "/evidence-rules.js": ("evidence-rules.js", "application/javascript"),
          "/orientation.js": ("orientation.js", "application/javascript"), "/style.css": ("style.css", "text/css"),
          "/cloud.js": ("cloud.js", "application/javascript"), "/i18n.js": ("i18n.js", "application/javascript")}


class LabServer(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 16

    def __init__(self, address, handler, max_active=MAX_ACTIVE):
        super().__init__(address, handler)
        self.slots = threading.BoundedSemaphore(max_active)

    def handle_error(self, request, client_address):
        # R54c: nothing from the exception (a provider message could carry the key) reaches standard error.
        print("Request handling failed; details withheld (R54c)", file=sys.stderr, flush=True)


def make_server(port=8765, cloud=None, mcp=None, agent_store=None, max_active=MAX_ACTIVE, read_timeout=READ_TIMEOUT):
    lab = Lab()
    cloud = cloud or CloudSessions()
    mcp = mcp or Context7Sessions()
    agent_store = agent_store or AgentStore(ROOT / ".local/agents.json")

    class Handler(BaseHTTPRequestHandler):
        timeout = read_timeout

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
            if not self.server.slots.acquire(blocking=False):
                self.close_connection = True
                return self.respond(503, {"error": "SERVER_BUSY"})
            try:
                action()
            except TimeoutError:
                self.close_connection = True
                self.respond(408, {"error": "REQUEST_TIMEOUT"})
            except Exception:  # noqa: BLE001 - R54c: fixed envelope, no message
                self.close_connection = True
                self.respond(500, {"error": "INTERNAL_ERROR"})
            finally:
                self.server.slots.release()

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
