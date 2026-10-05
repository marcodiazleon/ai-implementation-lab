import json
import shutil
import subprocess
import unittest
from src.lab.controller import Lab, ROOT, load_data

# Runs web/public-demo.js in a fresh Node vm context per case, with a minimal browser stub whose fetch reads the
# versioned fixtures from disk. Each case is a list of [method, path, body] calls; prints the JSON responses.
HARNESS = r"""
const fs = require("fs"), path = require("path"), vm = require("vm");
const root = process.argv[1], cases = JSON.parse(fs.readFileSync(0, "utf8"));
const files = { "data/orders.json": "data/orders.json", "data/policy.json": "data/policy.json",
  "data/scenarios.json": "data/scenarios.json", "data/roles.json": "agents/roles.json" };
const source = fs.readFileSync(path.join(root, "web/public-demo.js"), "utf8");
(async () => {
  const out = [];
  for (const calls of cases) {
    const ctx = { document: { documentElement: { classList: { add() {} } } }, location: { href: "http://localhost/" },
      crypto: globalThis.crypto, Response, URL, TextEncoder,
      fetch: async (name) => new Response(fs.readFileSync(path.join(root, files[name]))) };
    ctx.window = ctx;
    vm.runInNewContext(source, ctx);
    const results = [];
    for (const [method, url, body] of calls) {
      const response = await ctx.fetch(url, body === null ? { method } : { method, body: JSON.stringify(body) });
      results.push({ status: response.status, body: await response.json() });
    }
    out.push(results);
  }
  process.stdout.write(JSON.stringify(out));
})().catch((e) => { console.error(e); process.exit(1); });
"""

def run_js(cases):
    node = shutil.which("node")
    result = subprocess.run([node, "-e", HARNESS, str(ROOT)], input=json.dumps(cases),
                            capture_output=True, text=True, encoding="utf-8", timeout=60)
    if result.returncode:
        raise AssertionError("node harness failed: " + result.stderr)
    return json.loads(result.stdout)

class ParityTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which("node"):
            self.skipTest("node not available")

    def test_public_demo_matches_python_controller(self):
        scenarios = load_data("scenarios.json")
        js = run_js([[["POST", "/api/request", s["request"]], ["GET", "/api/state", None]] for s in scenarios])
        for scenario, (request, state) in zip(scenarios, js):
            with self.subTest(scenario=scenario["id"]):
                lab = Lab()
                expected = lab.request(scenario["request"])
                self.assertEqual(request["body"], expected)
                self.assertEqual(request["body"]["status"], scenario["expected"])
                # Same canonical digest: identical audit events, hashes included.
                self.assertEqual(state["body"]["events"], lab.snapshot()["events"])

        # Full DEMO-101 flow: request -> approve -> execute -> replay yields one receipt and a valid chain.
        lab = Lab()
        proposal = lab.request({"order_id": "DEMO-101", "intent": "refund"})
        lab.decide(proposal["id"], "approve", "human_reviewer")
        first, replay = lab.execute(proposal["id"]), lab.execute(proposal["id"])
        snapshot = lab.snapshot()
        ref = {"proposal_id": proposal["id"]}
        (req, decision, js_first, js_replay, state), = run_js([[
            ["POST", "/api/request", {"order_id": "DEMO-101", "intent": "refund"}],
            ["POST", "/api/decision", dict(ref, decision="approve")],
            ["POST", "/api/execute", ref], ["POST", "/api/execute", ref], ["GET", "/api/state", None]]])
        self.assertEqual(req["body"], proposal)
        self.assertEqual(decision["body"]["status"], "APPROVED")
        self.assertEqual(first, replay)
        self.assertEqual(js_first["body"], first)
        self.assertEqual(js_replay["body"], first)
        self.assertEqual(state["body"]["receipts"], snapshot["receipts"])
        self.assertEqual(len(snapshot["receipts"]), 1)
        self.assertTrue(snapshot["audit_chain_valid"])
        self.assertTrue(state["body"]["audit_chain_valid"])
        self.assertEqual(state["body"]["events"], snapshot["events"])

if __name__ == "__main__":
    unittest.main()
