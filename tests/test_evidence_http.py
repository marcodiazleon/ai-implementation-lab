import http.client, json, threading, unittest
from src.lab.server import make_server

class EvidenceHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def get(self, path, host=None):
        c = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=5)
        c.request("GET", path, headers={"Host": host} if host else {})
        r = c.getresponse(); result = (r.status, r.getheader("Content-Type"), r.read()); c.close()
        return result

    def test_evidence_route_serves_committed_run(self):
        status, mime, raw = self.get("/api/evidence")
        self.assertEqual((status, mime), (200, "application/json; charset=utf-8"))
        self.assertIsInstance(json.loads(raw)["passed"], bool)

    def test_acceptance_route_serves_csv_text(self):
        status, mime, raw = self.get("/api/acceptance")
        self.assertEqual((status, mime), (200, "text/csv; charset=utf-8"))
        self.assertTrue(raw.decode("utf-8").startswith("case_id,"))

    def test_requirements_route_lists_spec_rows(self):
        status, _, raw = self.get("/api/requirements")
        rows = json.loads(raw)
        self.assertEqual(status, 200)
        self.assertEqual(rows[0]["id"], "R01")
        self.assertEqual(set(rows[0]), {"id", "text", "source", "cu"})

    def test_untrusted_host_is_blocked(self):
        for path in ("/api/evidence", "/api/acceptance", "/api/requirements"):
            self.assertEqual(self.get(path, host="evil.example")[0], 403)

if __name__ == "__main__":
    unittest.main()
