import json
import shutil
import subprocess
import unittest
from src.lab.controller import ROOT

# Runs web/public-demo.js and web/app.js together in one Node vm context with a minimal DOM stub, then drives the
# real click/submit handlers. Checks UI state transitions only; layout, focus rings and i18n need a real browser.
HARNESS = r"""
const fs = require("fs"), path = require("path"), vm = require("vm");
const root = process.argv[1];
const files = { "data/orders.json": "data/orders.json", "data/policy.json": "data/policy.json",
  "data/scenarios.json": "data/scenarios.json", "data/roles.json": "agents/roles.json" };
let focused = null;
const el = (tag, id) => ({ tag, id, hidden: false, disabled: false, checked: false, value: "", textContent: "", className: "",
  open: false, children: [], options: [], listeners: {}, dataset: {}, classList: { toggle() {}, remove() {}, add() {} },
  setAttribute() {}, click() {}, focus() { focused = this.id; },
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); },
  append(...nodes) { for (const n of nodes) { this.children.push(n); if (n.tag === "option") { this.options.push(n); if (!this.value) this.value = n.value; } } },
  replaceChildren(...nodes) { this.children = nodes; },
  showModal() { this.open = true; },
  close() { if (this.open) { this.open = false; for (const fn of this.listeners.close || []) fn(); } } });
const nodes = {};
const ctx = { location: { href: "http://localhost/" }, crypto: globalThis.crypto, Response, URL, TextEncoder, Blob, setTimeout,
  addEventListener() {},
  document: { documentElement: { classList: { add() {} } }, createElement: (tag) => el(tag),
    getElementById: (id) => (nodes[id] ||= el("div", id)) },
  LabI18n: { t: (s, v = {}) => String(s).replace(/\{(\w+)\}/g, (m, n) => String(v[n] ?? m)),
    bind(node, s, v = {}) { node.textContent = this.t(s, v); } },
  fetch: async (name) => new Response(fs.readFileSync(path.join(root, files[name]))) };
ctx.window = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(root, "web/public-demo.js"), "utf8"), ctx);
vm.runInContext(fs.readFileSync(path.join(root, "web/app.js"), "utf8"), ctx);
const $ = (id) => ctx.document.getElementById(id);
const view = () => ({ result: $("result").textContent, chain: $("chain").textContent, receipts: $("receiptCount").textContent,
  decisionHidden: $("decisionBox").hidden, disabled: ["approve", "reject", "execute"].map((id) => $(id).disabled) });
const state = async () => (await ctx.fetch("/api/state")).json();
const explain = async (amount, days, status) => {
  Object.assign($("explainAmount"), { value: amount }); Object.assign($("explainDays"), { value: days }); $("explainStatus").value = status;
  await $("explainForm").onsubmit({ preventDefault() {} });
  return { verdict: $("verdict").textContent, items: $("conditions").children.map((li) => [li.className, li.children[1].textContent]),
    exportDisabled: $("exportExplain").disabled };
};
(async () => {
  for (let i = 0; i < 200 && !$("scenario").options.length; i++) await new Promise((r) => setTimeout(r, 5));
  await new Promise((r) => setTimeout(r, 20));
  const out = { initial: view() };
  $("scenario").value = "eligible"; $("scenario").onchange(); await $("propose").onclick();
  out.proposed = view();
  await $("approve").onclick(); await $("execute").onclick();
  out.executed = view();
  $("scenario").value = "late"; $("scenario").onchange();
  out.changed = view();
  $("resetSession").onclick(); out.dialogOpened = $("resetDialog").open;
  $("resetCancel").onclick();
  out.cancelled = { ...view(), open: $("resetDialog").open, proposals: (await state()).proposals.length };
  $("resetSession").onclick(); await $("resetConfirm").onclick();
  const after = await state();
  out.reset = { ...view(), open: $("resetDialog").open, focused, proposals: after.proposals.length, events: after.events.length };
  out.explainPlan = await explain("180", "20", "delivered");
  out.explainTen = await explain("180", "10", "delivered");
  out.explainInvalid = await explain("-1", "10", "delivered");
  out.eventsAfterExplain = (await state()).events.length;
  process.stdout.write(JSON.stringify(out));
})().catch((e) => { console.error(e); process.exit(1); });
"""

class AppUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        node = shutil.which("node")
        if not node:
            raise unittest.SkipTest("node not available")
        result = subprocess.run([node, "-e", HARNESS, str(ROOT)], capture_output=True, text=True, encoding="utf-8", timeout=60)
        if result.returncode:
            raise AssertionError("node harness failed: " + result.stderr)
        cls.out = json.loads(result.stdout)

    def test_case_change_disables_actions_on_previous_proposal(self):
        self.assertEqual(self.out["initial"]["disabled"], [True, True, True])
        self.assertFalse(self.out["proposed"]["decisionHidden"])
        self.assertEqual(self.out["proposed"]["disabled"], [False, False, False])
        self.assertEqual(self.out["executed"]["receipts"], "01")
        self.assertTrue(self.out["changed"]["decisionHidden"])
        self.assertEqual(self.out["changed"]["disabled"], [True, True, True])

    def test_reset_dialog_cancel_keeps_state_and_confirm_clears_it(self):
        self.assertTrue(self.out["dialogOpened"])
        cancelled, reset = self.out["cancelled"], self.out["reset"]
        self.assertEqual((cancelled["open"], cancelled["receipts"], cancelled["proposals"]), (False, "01", 1))
        self.assertEqual(cancelled["chain"], "CADENA COHERENTE")
        self.assertEqual((reset["open"], reset["receipts"], reset["chain"], reset["result"]), (False, "00", "Sin operaciones", "Sesión reiniciada."))
        self.assertEqual((reset["proposals"], reset["events"], reset["decisionHidden"]), (0, 0, True))
        self.assertEqual(reset["disabled"], [True, True, True])
        self.assertEqual(reset["focused"], "resetSession")

    def test_explain_form_lists_each_condition_without_events(self):
        plan, ten, invalid = self.out["explainPlan"], self.out["explainTen"], self.out["explainInvalid"]
        self.assertEqual([c for c, _ in plan["items"]], ["ok", "fail", "fail"])
        self.assertIn("Fuera del plazo permitido.", plan["items"][1][1])
        self.assertIn("Importe por encima del límite.", plan["items"][2][1])
        self.assertEqual((plan["verdict"], plan["exportDisabled"]), ("No elegible", False))
        self.assertEqual([c for c, _ in ten["items"]], ["ok", "ok", "fail"])
        self.assertEqual((invalid["items"], invalid["verdict"], invalid["exportDisabled"]), ([], "La solicitud no es válida.", True))
        self.assertEqual(self.out["eventsAfterExplain"], 0)

if __name__ == "__main__":
    unittest.main()
