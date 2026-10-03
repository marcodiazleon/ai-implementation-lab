import http.client
import json
import threading
import unittest
from unittest.mock import patch
from src.lab.cloud import CloudSessions, CloudError, OpenAITransport, TTL, MAX_REQUESTS
from src.lab.server import make_server
from scripts.check_environment import inspect
from pathlib import Path
import tempfile

KEY = "test-key-for-offline-tests-only"
BODY = {"api_key": KEY, "model": "test-model", "max_output_tokens": 512, "consent": True}

class FakeTransport:
    def __init__(self):
        self.calls = []
    def check(self, key, model):
        self.calls.append(("check", key, model))
    def answer(self, key, model, messages, limit):
        self.calls.append(("answer", key, model, messages, limit))
        return {"text": "<script>mock text only</script>", "usage": {"total_tokens": 12}, "incomplete": False}

class CloudTests(unittest.TestCase):
    def setUp(self):
        self.transport = FakeTransport()
        self.now = 0
        self.cloud = CloudSessions(self.transport, lambda: self.now)
    def connect(self):
        return self.cloud.connect(dict(BODY))["session_id"]

    def test_consent_and_validation_precede_network(self):
        for changed in ({"consent": False}, {"api_key": "bad"}, {"model": "../bad"},
                        {"max_output_tokens": True}, {"max_output_tokens": 999}, {"base_url": "https://evil.invalid"}):
            with self.assertRaises(CloudError):
                self.cloud.connect({**BODY, **changed})
        self.assertEqual(self.transport.calls, [])

    def test_key_not_returned_or_demo_exported(self):
        result = self.cloud.connect(dict(BODY))
        self.assertNotIn(KEY, json.dumps(result))
        self.assertNotEqual(result["session_id"], KEY)
        self.assertEqual(result["model"], "test-model")

    def test_history_clear_and_session_isolation(self):
        one, two = self.connect(), self.connect()
        self.cloud.ask({"session_id": one, "message": "first"})
        self.cloud.ask({"session_id": one, "message": "second"})
        self.assertEqual(len(self.transport.calls[-1][3]), 3)
        self.cloud.ask({"session_id": two, "message": "other"})
        self.assertEqual(len(self.transport.calls[-1][3]), 1)
        self.cloud.clear({"session_id": one})
        self.cloud.ask({"session_id": one, "message": "new"})
        self.assertEqual(len(self.transport.calls[-1][3]), 1)
        self.assertEqual(self.cloud.sessions[one]["requests"], 3)

    def test_expiry_disconnect_and_unknown_session(self):
        token = self.connect()
        row = self.cloud.sessions[token]
        self.now = TTL
        with self.assertRaises(CloudError):
            self.cloud.ask({"session_id": token, "message": "hello"})
        self.assertEqual(row["key"], "")
        token = self.connect()
        self.cloud.disconnect({"session_id": token})
        self.cloud.disconnect({"session_id": token})
        with self.assertRaises(CloudError):
            self.cloud.ask({"session_id": token, "message": "hello"})

    def test_limits_and_failed_attempt_count(self):
        token = self.connect()
        with self.assertRaises(CloudError):
            self.cloud.ask({"session_id": token, "message": "x" * 2001})
        with patch.object(self.transport, "answer", side_effect=CloudError("API_LIMIT", 502)):
            for _ in range(MAX_REQUESTS):
                with self.assertRaises(CloudError):
                    self.cloud.ask({"session_id": token, "message": "hello"})
        with self.assertRaisesRegex(CloudError, "SESSION_REQUEST_LIMIT"):
            self.cloud.ask({"session_id": token, "message": "hello"})
        self.assertFalse(self.cloud.sessions[token]["busy"])

    def test_no_concurrent_request_and_disconnect_discards_result(self):
        token = self.connect()
        entered, release = threading.Event(), threading.Event()
        outcomes = []
        def slow(*args):
            entered.set()
            release.wait(3)
            return {"text": "late answer"}
        def ask():
            try:
                self.cloud.ask({"session_id": token, "message": "hello"})
            except CloudError as error:
                outcomes.append(error.code)
        with patch.object(self.transport, "answer", side_effect=slow):
            worker = threading.Thread(target=ask)
            worker.start()
            try:
                self.assertTrue(entered.wait(2))
                with self.assertRaisesRegex(CloudError, "REQUEST_IN_PROGRESS"):
                    self.cloud.ask({"session_id": token, "message": "again"})
                self.cloud.disconnect({"session_id": token})
            finally:
                release.set()
                worker.join(3)
        self.assertEqual(outcomes, ["SESSION_EXPIRED"])
        self.assertNotIn(token, self.cloud.sessions)

    def test_capacity_and_failed_connection_releases_reservation(self):
        with patch.object(self.transport, "check", side_effect=CloudError("API_KEY_REJECTED")):
            with self.assertRaises(CloudError):
                self.connect()
        self.assertEqual(self.cloud.connecting, 0)
        for _ in range(8):
            self.connect()
        with self.assertRaisesRegex(CloudError, "SESSION_CAPACITY"):
            self.connect()

    def test_transport_contract_and_malformed_response(self):
        transport = OpenAITransport()
        output = {"status": "completed", "output": [{"type": "message", "content": [
            {"type": "output_text", "text": "answer"}]}], "usage": {"total_tokens": 9, "secret": KEY}}
        with patch.object(transport, "request", return_value=output) as request:
            result = transport.answer(KEY, "test-model", [{"role": "user", "content": "hello"}], 256)
            args = request.call_args.args
            self.assertEqual(args[:3], ("POST", "/v1/responses", KEY))
            self.assertFalse(args[3]["store"])
            self.assertEqual(args[3]["max_output_tokens"], 256)
            self.assertNotIn("tools", args[3])
            self.assertEqual(result["usage"], {"total_tokens": 9})
        for malformed in ({"output": None}, {"output": [{"type": "message", "content": None}]},
                          {"output": []}):
            with patch.object(transport, "request", return_value=malformed):
                with self.assertRaises(CloudError):
                    transport.answer(KEY, "test-model", [], 512)

    def test_provider_errors_sanitized_no_retry(self):
        with patch("src.lab.cloud.http.client.HTTPSConnection") as factory:
            connection = factory.return_value
            response = connection.getresponse.return_value
            response.status = 401
            response.read.return_value = (KEY + " provider internal detail").encode()
            with self.assertRaisesRegex(CloudError, "^API_KEY_REJECTED$"):
                OpenAITransport().request("GET", "/v1/models/test-model", KEY)
            factory.assert_called_once_with("api.openai.com", timeout=30)
            connection.request.assert_called_once()
            connection.close.assert_called_once()

class CloudHttpTests(unittest.TestCase):
    def test_http_consent_origin_and_no_key_in_state(self):
        server = make_server(0, CloudSessions(FakeTransport()))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        def call(path, body=None, origin=None):
            connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
            headers = {"Content-Type": "application/json"}
            if origin:
                headers["Origin"] = origin
            connection.request("GET" if body is None else "POST", path,
                               None if body is None else json.dumps(body), headers)
            response = connection.getresponse()
            result = response.status, response.read()
            connection.close()
            return result
        try:
            self.assertEqual(call("/api/cloud/connect", BODY, "https://evil.invalid")[0], 403)
            self.assertEqual(call("/api/cloud/connect", {**BODY, "consent": False})[0], 400)
            status, raw = call("/api/cloud/connect", BODY)
            self.assertEqual(status, 200)
            token = json.loads(raw)["session_id"]
            status, answer = call("/api/cloud/ask", {"session_id": token, "message": "hello"})
            self.assertEqual(status, 200)
            self.assertIn(b"mock text", answer)
            raw = call("/api/state")[1]
            self.assertNotIn(KEY.encode(), raw)
            self.assertNotIn(token.encode(), raw)
            self.assertNotIn(b"mock text", raw)
            self.assertEqual(call("/cloud.js")[0], 200)
            self.assertEqual(call("/api/cloud/sessions")[0], 404)
        finally:
            server.shutdown()
            server.server_close()
            worker.join()

class PortableTests(unittest.TestCase):
    def test_audit_reports_missing_files_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            before = list(Path(directory).iterdir())
            result = inspect(directory, port=0)
            self.assertFalse(result["ready_to_start"])
            self.assertIn("run.py", result["missing"])
            self.assertEqual(before, list(Path(directory).iterdir()))
