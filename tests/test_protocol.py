import json
import subprocess
import sys
import unittest
from src.lab.controller import ROOT
from src.lab.mcp_server import Protocol, VERSION

def req(method, params=None, ident=1):
    return {"jsonrpc": "2.0", "id": ident, "method": method, "params": params or {}}

class ProtocolTests(unittest.TestCase):
    def ready(self):
        p = Protocol()
        result = p.handle(req("initialize", {"protocolVersion": VERSION, "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}))
        self.assertEqual(result["result"]["protocolVersion"], VERSION)
        p.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
        return p

    def test_initialization_required(self):
        self.assertEqual(Protocol().handle(req("tools/list"))["error"]["code"], -32002)

    def test_only_two_read_tools(self):
        tools = self.ready().handle(req("tools/list"))["result"]["tools"]
        self.assertEqual({t["name"] for t in tools}, {"lookup_demo_order", "read_demo_policy"})
        self.assertTrue(all(t["annotations"]["readOnlyHint"] for t in tools))

    def test_write_tool_denied(self):
        self.assertIn("error", self.ready().handle(req("tools/call", {"name": "execute_refund", "arguments": {}})))

    def test_scope_is_preserved(self):
        result = self.ready().handle(req("tools/call", {"name": "lookup_demo_order", "arguments": {"order_id": "DEMO-104"}}))["result"]
        self.assertTrue(result["isError"])
        self.assertEqual(json.loads(result["content"][0]["text"])["reason"], "ORDER_UNAVAILABLE")

    def test_bad_args(self):
        self.assertIn("error", self.ready().handle(req("tools/call", {"name": "read_demo_policy", "arguments": {"secret": "no"}})))

    def test_stdio_round_trip(self):
        messages = [
            req("initialize", {"protocolVersion": VERSION, "capabilities": {}, "clientInfo": {"name": "wire-test", "version": "1"}}),
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            req("tools/list", ident=2),
            req("tools/call", {"name": "lookup_demo_order", "arguments": {"order_id": "DEMO-101"}}, 3),
            req("tools/call", {"name": "execute_refund", "arguments": {}}, 4)]
        run = subprocess.run([sys.executable, "-X", "utf8", "run.py", "mcp"], cwd=ROOT,
                             input="\n".join(json.dumps(x) for x in messages) + "\n",
                             text=True, capture_output=True, timeout=10, check=True)
        rows = [json.loads(line) for line in run.stdout.splitlines()]
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows[2]["id"], 3)
        self.assertEqual(json.loads(rows[2]["result"]["content"][0]["text"])["status"], "READ_ONLY")
        self.assertIn("error", rows[3])
        self.assertEqual(run.stderr, "")

    def test_invalid_initialization_does_not_mark_ready(self):
        p = Protocol()
        self.assertEqual(p.handle(req("initialize"))["error"]["code"], -32602)
        self.assertFalse(p.initialized)

    def test_protocol_negotiation_returns_supported_version(self):
        p = Protocol()
        result = p.handle(req("initialize", {"protocolVersion": "unknown-version", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}))
        self.assertEqual(result["result"]["protocolVersion"], VERSION)
