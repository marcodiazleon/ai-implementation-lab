"""Loopback-only viewer. Never use this development server on a public host."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from .controller import Lab, ROOT, load_data
from .models import RuleError
from .cloud import CloudSessions, CloudError

def make_server(port=8765, cloud=None):
    lab = Lab()
    cloud = cloud or CloudSessions()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def respond(self, code, payload, mime="application/json"):
            raw = json.dumps(payload).encode() if mime == "application/json" else payload
            self.send_response(code)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def trusted(self):
            hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            origin = self.headers.get("Origin")
            return self.headers.get("Host") in hosts and (origin is None or origin in {"http://" + h for h in hosts})

        def do_GET(self):
            if not self.trusted():
                return self.respond(403, {"error": "HOST_OR_ORIGIN_BLOCKED"})
            path = urlsplit(self.path).path
            if path == "/api/state":
                return self.respond(200, lab.snapshot())
            if path == "/api/scenarios":
                return self.respond(200, load_data("scenarios.json"))
            assets = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "application/javascript"),
                      "/style.css": ("style.css", "text/css"), "/cloud.js": ("cloud.js", "application/javascript")}
            if path in assets:
                filename, mime = assets[path]
                return self.respond(200, (ROOT / "web" / filename).read_bytes(), mime)
            self.respond(404, {"error": "NOT_FOUND"})

        def do_POST(self):
            if not self.trusted():
                return self.respond(403, {"error": "HOST_OR_ORIGIN_BLOCKED"})
            if self.headers.get("Content-Type") != "application/json":
                return self.respond(415, {"error": "JSON_REQUIRED"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                body_limit = 16384 if urlsplit(self.path).path.startswith("/api/cloud/") else 4096
                if not 0 < length <= body_limit:
                    return self.respond(413, {"error": "INVALID_BODY_SIZE"})
                body = json.loads(self.rfile.read(length))
                if not isinstance(body, dict):
                    raise ValueError()
            except (ValueError, UnicodeError):
                return self.respond(400, {"error": "INVALID_JSON"})
            path = urlsplit(self.path).path
            try:
                if path.startswith("/api/cloud/"):
                    handlers = {"/api/cloud/connect": cloud.connect, "/api/cloud/ask": cloud.ask,
                                "/api/cloud/clear": cloud.clear, "/api/cloud/disconnect": cloud.disconnect}
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
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)

def serve(port=8765):
    server = make_server(port)
    print(f"Local demo: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
