import json
import shutil
import subprocess
import unittest
from src.lab.controller import Lab, ROOT, load_data

# Runs web/public-demo.js in a fresh Node vm context per case, with a minimal browser stub whose fetch reads the
# versioned fixtures from disk. Each case is a list of [method, path, body] calls; prints the JSON responses.
HARNESS = r"""
const fs = require("fs"), path = require("path"), vm = require("vm");
const root = process.argv[1], withRules = process.argv[2] !== "no-rules", cases = JSON.parse(fs.readFileSync(0, "utf8"));
const files = { "data/orders.json": "data/orders.json", "data/policy.json": "data/policy.json",
  "data/scenarios.json": "data/scenarios.json", "data/roles.json": "agents/roles.json" };
const source = fs.readFileSync(path.join(root, "web/public-demo.js"), "utf8");
const rules = fs.readFileSync(path.join(root, "web/sensitive-rules.js"), "utf8");
(async () => {
  const out = [];
  for (const calls of cases) {
    const ctx = { document: { documentElement: { classList: { add() {} } } }, location: { href: "http://localhost/" },
      crypto: globalThis.crypto, Response, URL, TextEncoder,
      fetch: async (name) => new Response(fs.readFileSync(path.join(root, files[name]))) };
    ctx.window = ctx;
    if (withRules) vm.runInNewContext(rules, ctx);   // the built page loads sensitive-rules.js before public-demo.js
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

def run_js(cases, rules=True):
    node = shutil.which("node")
    result = subprocess.run([node, "-e", HARNESS, str(ROOT)] + ([] if rules else ["no-rules"]), input=json.dumps(cases),
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


class PagesAgentSaveTests(unittest.TestCase):
    """C331 (R54h, D59): the in-tab agent save of the public build applies the shared credential rules."""

    def setUp(self):
        if not shutil.which("node"):
            self.skipTest("node not available")

    @staticmethod
    def formats():
        # Dummy, non-functional values assembled at runtime so that this file never matches the publication guard.
        return {
            "Anthropic key": "sk-" + "ant-" + "A" * 24,
            "OpenAI key": "sk-" + "proj-" + "B" * 24,
            "Context7-style key": "ctx7" + "sk-" + "C" * 20,
            "GitHub token": "gh" + "p_" + "D" * 36,
            "AWS access key id": "AK" + "IA" + "E" * 16,
            "Slack token": "xo" + "xb-" + "1" * 12,
            "Google API key": "AI" + "za" + "F" * 35,
            "private key block": "-----BEGIN " + "RSA PRIVATE KEY-----",
            "bearer token": "Bear" + "er " + "G" * 24,
            "credential assignment": 'api_' + 'key = "' + "H" * 20 + '"',
            "local personal path": "/Us" + "ers/" + "someone/",
        }

    @staticmethod
    def definition(**changes):
        body = {"id": "", "name": "Agente de revisión", "role": "Revisa borradores de texto",
                "prompt": "Eres un revisor de textos que señala errores y propone cambios claros.", "work_mode": "review"}
        body.update(changes)
        return ["POST", "/api/custom-agents/save", body]

    def test_pages_agent_save_applies_every_shared_format(self):
        from src.lab.sensitive import find_secrets_in
        formats = self.formats()
        self.assertEqual(len(formats), 11)
        calls = [self.definition(prompt="Eres un revisor. " + value + " y nada más que eso.") for value in formats.values()]
        calls += [self.definition(name="Nombre " + formats["GitHub token"]), self.definition(role="Rol con " + formats["Slack token"] + " dentro")]
        results = run_js([[call] for call in calls])
        for (label, value), (result,) in zip(formats.items(), results):
            with self.subTest(format=label):
                self.assertTrue(find_secrets_in(value), "the Python rules must name this format too")
                self.assertEqual((result["status"], result["body"]), (400, {"error": "AGENT_SENSITIVE_INPUT"}))
        for (result,) in results[len(formats):]:
            self.assertEqual((result["status"], result["body"]), (400, {"error": "AGENT_SENSITIVE_INPUT"}))

    def test_benign_definition_is_saved_and_missing_rules_fail_closed(self):
        saved = run_js([[self.definition()]])[0][0]
        self.assertEqual(saved["status"], 200)
        self.assertTrue(saved["body"]["id"].startswith("custom-"))
        refused = run_js([[self.definition()]], rules=False)[0][0]
        self.assertEqual((refused["status"], refused["body"]), (400, {"error": "AGENT_SENSITIVE_INPUT"}))
