"use strict";
// R36a / D33: requirement badge. Ported from PR #4 D24 (ea5fe51, tally) and extended with BLOQUEADO.
// Pure functions so the rule is tested once (tests/test_evidence_rules.py) and used by the Evidence view.
(() => {
 function tally(cases, id) {
  const applicable = cases.filter((c) => c.requirement_id === id && c.status !== "NO_APLICA");
  return {
   applicable: applicable.length,
   passed: applicable.filter((c) => c.status === "PASS" && String(c.evidence || "").trim()).length,
   failed: applicable.some((c) => c.status === "FAIL"),
   blocked: applicable.some((c) => c.status === "BLOQUEADO"),
  };
 }
 function badge(cases, id) {
  const n = tally(cases, id);
  if (n.failed) return "FAIL";
  if (n.blocked) return "BLOQUEADO";
  if (n.applicable && n.passed === n.applicable) return "PASS";
  return n.passed ? "PARCIAL" : "PENDIENTE";
 }
 (typeof window !== "undefined" ? window : globalThis).LabEvidenceRules = { tally, badge };
})();
