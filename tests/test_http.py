import http.client
import json
import threading
import unittest
from src.lab.server import make_server

class HttpTests(unittest.TestCase):
    def setUp(self):
        self.server = make_server(0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def call(self, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=3)
        method = "GET" if body is None else "POST"
        hdrs = {"Content-Type": "application/json"}
        hdrs.update(headers or {})
        connection.request(method, path, None if body is None else json.dumps(body), hdrs)
        response = connection.getresponse()
        raw = response.read()
        result = (response.status, dict(response.getheaders()), raw)
        connection.close()
        return result

    def test_static_and_no_directory_access(self):
        self.assertEqual(self.call("/")[0], 200)
        for path in ("/data/orders.json", "/../run.py", "/.git/config"):
            self.assertEqual(self.call(path)[0], 404)

    def test_external_origin_blocked(self):
        self.assertEqual(self.call("/api/request", {}, {"Origin": "https://example.com"})[0], 403)

    def test_untrusted_host_blocked(self):
        self.assertEqual(self.call("/api/state", headers={"Host": "example.com"})[0], 403)

    def test_content_type_and_size(self):
        self.assertEqual(self.call("/api/request", {}, {"Content-Type": "text/plain"})[0], 415)
        self.assertEqual(self.call("/api/request", {"large": "x" * 5000})[0], 413)

    def test_workflow_and_replay(self):
        status, _, raw = self.call("/api/request", {"order_id": "DEMO-101", "intent": "refund"})
        self.assertEqual(status, 200)
        key = json.loads(raw)["id"]
        self.assertEqual(self.call("/api/execute", {"proposal_id": key})[0], 409)
        self.assertEqual(self.call("/api/decision", {"proposal_id": key, "decision": "approve"})[0], 200)
        first = self.call("/api/execute", {"proposal_id": key})[2]
        second = self.call("/api/execute", {"proposal_id": key})[2]
        self.assertEqual(first, second)
        self.assertFalse(json.loads(first)["real_effect"])

    def test_explain_route_200_and_409(self):
        status, _, raw = self.call("/api/explain", {"amount": 180, "days_since_delivery": 20, "status": "delivered"})
        self.assertEqual(status, 200)
        self.assertEqual([c["ok"] for c in json.loads(raw)["conditions"]], [True, False, False])
        status, _, raw = self.call("/api/explain", {"amount": -1, "days_since_delivery": 20, "status": "delivered"})
        self.assertEqual((status, json.loads(raw)), (409, {"status": "BLOCKED", "reason": "INVALID_REQUEST"}))

    def test_reset_route_returns_empty_snapshot(self):
        self.call("/api/request", {"order_id": "DEMO-101", "intent": "refund"})
        status, _, raw = self.call("/api/reset", {})
        state = json.loads(raw)
        self.assertEqual(status, 200)
        self.assertEqual((state["proposals"], state["receipts"], state["events"]), ([], [], []))
        self.assertEqual(self.call("/api/reset", {"all": True})[0], 400)

    def test_reset_and_explain_untrusted_host_blocked(self):
        for path in ("/api/reset", "/api/explain"):
            self.assertEqual(self.call(path, {}, {"Host": "example.com"})[0], 403)

    def test_security_headers(self):
        _, headers, _ = self.call("/")
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertIn("frame-ancestors 'none'", headers["Content-Security-Policy"])
