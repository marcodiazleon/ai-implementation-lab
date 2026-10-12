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
 // R49e: the payload must have the shape and the internal consistency the view relies on, before anything is
 // rendered. Returns null or a bilingual error naming the field; a PASS can never come out of a bad payload.
 const isCount = (v) => Number.isInteger(v) && v >= 0;
 function validatePayload(evidence, cases, requirements, status, lang) {
  const t = (es, en) => (lang === "en" ? en : es);
  const bad = (field, es, en) => t("Evidencia inválida: ", "Invalid evidence: ") + field + " — " + t(es, en);
  if (!evidence || typeof evidence !== "object" || Array.isArray(evidence)) return bad("latest.json", "no es un objeto", "is not an object");
  const tests = evidence.tests;
  if (!tests || typeof tests !== "object" || Array.isArray(tests)) return bad("tests", "falta el resumen de la ejecución", "the run summary is missing");
  for (const key of ["run", "failures", "errors"]) {
   if (!isCount(tests[key])) return bad("tests." + key, "debe ser un entero no negativo", "must be a non-negative integer");
  }
  if (tests.run === 0) return bad("tests.run", "ninguna prueba ejecutada", "no test was run");
  if (typeof evidence.passed !== "boolean") return bad("passed", "debe ser verdadero o falso", "must be true or false");
  if (evidence.passed && (tests.failures > 0 || tests.errors > 0)) return bad("passed", "verdadero con fallos o errores registrados", "true with recorded failures or errors");
  // The runner (scripts/verify.py CaseResult) records exactly these statuses, once per test.
  const STATUSES = ["PASS", "FAIL", "NO_PROBADO"];
  if (!Array.isArray(evidence.test_results) || evidence.test_results.some((r) => !r || typeof r.test_id !== "string" || !r.test_id.trim() || typeof r.status !== "string")) {
   return bad("test_results", "debe ser una lista de pruebas con identificador y estado", "must be a list of tests with an id and a status");
  }
  const unknown = evidence.test_results.find((r) => !STATUSES.includes(r.status));
  if (unknown) return bad("test_results[" + unknown.test_id + "].status", "estado fuera de PASS, FAIL o NO_PROBADO: " + unknown.status, "status outside PASS, FAIL or NO_PROBADO: " + unknown.status);
  if (new Set(evidence.test_results.map((r) => r.test_id)).size !== evidence.test_results.length) return bad("test_results", "identificadores de prueba repetidos", "repeated test ids");
  if (evidence.test_results.length !== tests.run) return bad("test_results", "su número no coincide con tests.run", "its length does not match tests.run");
  const failRows = evidence.test_results.filter((r) => r.status === "FAIL").length, skippedRows = evidence.test_results.filter((r) => r.status === "NO_PROBADO").length;
  if ((tests.failures + tests.errors === 0) !== (failRows === 0)) return bad("test_results", "las filas FAIL no coinciden con failures y errors", "FAIL rows do not match failures and errors");
  if (isCount(tests.skipped) && skippedRows !== tests.skipped) return bad("test_results", "las filas NO_PROBADO no coinciden con tests.skipped", "NO_PROBADO rows do not match tests.skipped");
  if (evidence.passed && failRows) return bad("passed", "verdadero con una prueba FAIL", "true with a FAIL test");
  if (!Array.isArray(requirements) || requirements.length === 0 || requirements.some((r) => !r || typeof r.id !== "string" || !/^R\d+$/.test(r.id) || typeof r.text !== "string")) {
   return bad("requirements", "cada fila necesita id y texto", "each row needs an id and a text");
  }
  if (!Array.isArray(cases) || cases.length === 0) return bad("acceptance.csv", "sin filas", "has no rows");
  for (const column of ["case_id", "requirement_id", "status", "test_id", "expected"]) {
   if (cases.some((c) => typeof c[column] !== "string")) return bad("acceptance.csv", "falta la columna " + column, "column " + column + " is missing");
  }
  if (!status || typeof status !== "object" || Array.isArray(status)) return bad("status.json", "no es un objeto", "is not an object");
  for (const key of ["acceptance", "integration", "deployment", "independent_review"]) {
   if (!(key in status)) return bad("status." + key, "registro ausente", "record missing");
  }
  return null;
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
   if (states[key] === true) return yes + (reasons[key] ? " (" + reasons[key] + ")" : "");
   if (states[key] === false) return no + (reasons[key] ? " (" + reasons[key] + ")" : "");
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
 (typeof window !== "undefined" ? window : globalThis).LabEvidenceRules = { tally, badge, statusRows, validatePayload };
})();
