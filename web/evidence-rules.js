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
 // R49c / D41: the five project records as rows, with the state of THIS build computed by the server or the
 // static build (status.build_states). Pure: no DOM, so tests/test_u20.py runs it in Node with synthetic payloads.
 const short = (sha) => String(sha || "").slice(0, 7);
 function statusRows(status, evidence, lang) {
  const t = (es, en) => (lang === "en" ? en : es);
  if (!status || typeof status !== "object" || Array.isArray(status)) return { error: t("Estado del proyecto ilegible.", "Project status unreadable."), rows: [] };
  if (!evidence || typeof evidence !== "object" || !evidence.tests || typeof evidence.tests.run !== "number") {
   return { error: t("Evidencia ilegible: falta el resumen de la ejecución.", "Evidence unreadable: the run summary is missing."), rows: [] };
  }
  const states = status.build_states || {}, reasons = states.reasons || {};
  const scope = (v) => (v && typeof v === "object" ? t(v.es, v.en) : v ? String(v) : "");
  const thisBuild = (key, yes, no) => {
   if (states[key] === true) return yes;
   if (states[key] === false) return no;
   return t("esta revisión: sin determinar (", "this build: undetermined (") + (reasons[key] || t("sin Git", "no Git")) + ")";
  };
  const record = (key) => (status[key] && typeof status[key] === "object" ? status[key] : null);
  const review = record("independent_review"), acceptance = record("acceptance"), integration = record("integration"), deployment = record("deployment");
  const rows = [];
  rows.push({ key: "verification", label: t("Verificación automática", "Automated verification"),
   state: evidence.passed === true ? "PASS" : "FAIL",
   value: (evidence.passed === true ? "PASS" : "FAIL") + " · " + evidence.tests.run + t(" pruebas", " tests") + " · scripts/verify.py · "
    + String(evidence.generated_utc || "").slice(0, 10) + t(" · base ", " · baseline ") + short(evidence.input_revision)
    + (evidence.input_worktree_dirty ? t(" con cambios sin confirmar", " with uncommitted changes") : "") });
  rows.push({ key: "review", label: t("Revisión independiente", "Independent review"),
   state: review ? (states.independent_review === true ? "COVERED" : states.independent_review === false ? "OTHER_REVISION" : "UNKNOWN") : "NOT_RECORDED",
   value: !review ? t("No registrada", "Not recorded")
    : [review.status, review.by, review.date, t("revisión ", "revision ") + short(review.revision), scope(review.scope)].filter(Boolean).join(" · ") + " · "
     + thisBuild("independent_review", t("cubre esta revisión", "covers this build"), t("esta revisión no está revisada", "this build is not reviewed")) });
  rows.push({ key: "acceptance", label: t("Aceptación del dueño", "Owner acceptance"),
   state: acceptance ? (states.acceptance === true ? "COVERED" : states.acceptance === false ? "OTHER_REVISION" : "UNKNOWN") : "NOT_RECORDED",
   value: !acceptance ? t("No registrada", "Not recorded")
    : [acceptance.status, acceptance.by, acceptance.date, t("revisión ", "revision ") + short(acceptance.revision), scope(acceptance.scope)].filter(Boolean).join(" · ") + " · "
     + thisBuild("acceptance", t("mismo contenido: cubre esta revisión", "same content: covers this build"), t("esta revisión no está aceptada", "this build is not accepted")) });
  rows.push({ key: "integration", label: t("Integración", "Integration"),
   state: integration ? (states.integration === true ? "CONTAINED" : states.integration === false ? "NOT_CONTAINED" : "UNKNOWN") : "NOT_RECORDED",
   value: !integration ? t("No registrada", "Not recorded")
    : [integration.state, "main " + short(integration.main), integration.merged ? t("fusionada ", "merged ") + short(integration.merged) : "", integration.pull_request ? "PR #" + integration.pull_request : ""].filter(Boolean).join(" · ") + " · "
     + thisBuild("integration", t("esta revisión está contenida en main", "this build is contained in main"), t("esta revisión no está integrada", "this build is not integrated")) });
  rows.push({ key: "deployment", label: t("Despliegue", "Deployment"),
   state: deployment ? (states.deployment === true ? "COVERED" : states.deployment === false ? "OTHER_REVISION" : "UNKNOWN") : "NOT_RECORDED",
   value: !deployment ? t("No registrado", "Not recorded")
    : [deployment.state, t("Pages publica ", "Pages serves ") + short(deployment.revision), deployment.date, deployment.verified ? t("verificado por ", "verified by ") + deployment.verified.by + " " + (deployment.verified.date || "") : ""].filter(Boolean).join(" · ") + " · "
     + thisBuild("deployment", t("mismo contenido que lo publicado", "same content as the published site"), t("esta revisión no está publicada", "this build is not published")) });
  return { error: null, rows };
 }
 (typeof window !== "undefined" ? window : globalThis).LabEvidenceRules = { tally, badge, statusRows };
})();
