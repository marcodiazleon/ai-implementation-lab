"use strict";
// Evidence view (R27, R36). Shows what scripts/verify.py and docs/project-status.json recorded; it never
// recalculates a test result. The badge rule lives in evidence-rules.js (D33).
(() => {
 const el = (id) => document.getElementById(id);
 const REPO = "https://github.com/marcodiazleon/ai-implementation-lab";
 const t = (es, en) => (LabI18n.language === "en" ? en : es);
 let evidence = null, cases = [], requirements = [], status = null, failed = false;

 // Minimal RFC 4180 reader: quoted fields, doubled quotes, commas and newlines inside quotes.
 function parseCsv(text) {
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
   const c = text[i];
   if (quoted) {
    if (c !== '"') field += c;
    else if (text[i + 1] === '"') { field += '"'; i++; }
    else quoted = false;
   } else if (c === '"') quoted = true;
   else if (c === ",") { row.push(field); field = ""; }
   else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
   else if (c !== "\r") field += c;
  }
  if (field || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows;
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i] ?? ""])));
 }

 // R43a / D39: a file opens at the revision this page was produced from, or a historical case at the
 // commit that recorded it. Only without a recorded revision does a link fall back to live main.
 const revisionFor = (caseId) => (caseId && status?.pins?.[caseId]) || status?.revision || "main";
 const fileUrl = (path, caseId, kind = "blob") => REPO + "/" + kind + "/" + revisionFor(caseId) + "/" + path;
 function pinLinks() {
  for (const a of document.querySelectorAll("a[data-repo-path]")) a.href = fileUrl(a.dataset.repoPath, null, a.dataset.repoKind || "blob");
 }

 const badge = (id) => LabEvidenceRules.badge(cases, id);
 const tally = (id) => LabEvidenceRules.tally(cases, id);

 function cell(row, value) {
  const td = document.createElement("td");
  if (value instanceof Node) td.append(value); else td.textContent = value;
  row.append(td);
 }

 function renderCases() {
  const id = el("reqPicker").value, req = requirements.find((r) => r.id === id), state = badge(id);
  const own = cases.filter((c) => c.requirement_id === id);
  el("reqBadge").textContent = state;
  el("reqBadge").dataset.state = state;
  el("reqSource").textContent = t("Fuente " + req.source + " · " + req.cu + " · " + own.length + " casos",
   "Source " + req.source + " · " + req.cu + " · " + own.length + " cases")
   + (state === "PENDIENTE" ? t(" · sin caso PASS con evidencia", " · no PASS case with evidence")
    : state === "PARCIAL" ? t(` · evidencia parcial: ${tally(id).passed} de ${tally(id).applicable} casos aplicables PASS`,
                              ` · partial evidence: ${tally(id).passed} of ${tally(id).applicable} applicable cases PASS`) : "");
  el("reqCases").replaceChildren(...own.map((c) => {
   const tr = document.createElement("tr");
   for (const value of [c.case_id, c.action, c.expected, c.status, c.test_id]) cell(tr, value);
   let link = c.evidence || "—";
   const file = /^[\w.-]+(\/[\w.-]+)+$/.test(c.evidence) && !c.evidence.split("/").includes("..");
   const run = /^https:\/\/github\.com\/marcodiazleon\/ai-implementation-lab\/actions\/runs\/\d+$/.test(c.evidence);
   if (file || run) {
    link = document.createElement("a");
    Object.assign(link, { href: run ? c.evidence : fileUrl(c.evidence, c.case_id), textContent: run ? "Actions run " + c.evidence.split("/").pop() : c.evidence,
     target: "_blank", rel: "noopener noreferrer" });
    if (file && status?.pins?.[c.case_id]) link.title = t("Registro histórico en ", "Historical record at ") + status.pins[c.case_id].slice(0, 7);
   }
   cell(tr, link);
   return tr;
  }));
 }

 // R36b: five separate records. Raw codes stay visible next to their reading.
 const READ = { OWNER_ACCEPTANCE_NOT_RECORDED: ["No registrada", "Not recorded"], NOT_INTEGRATED: ["No integrada en main", "Not integrated into main"],
  NOT_DEPLOYED: ["No publicada", "Not published"], LIMITED: ["Limitada", "Limited"], NOT_PERFORMED: ["No realizada", "Not performed"] };
 const read = (code) => (READ[code] ? t(READ[code][0], READ[code][1]) + " (" + code + ")" : String(code ?? "—"));
 function renderStatus() {
  const block = el("statusRecords");
  block.hidden = !(status && evidence);
  if (block.hidden) return;
  const tests = evidence.tests || {}, review = status.independent_review || {};
  const rows = [
   [t("Verificación automática", "Automated verification"), (evidence.passed === true ? "PASS" : "FAIL") + " · " + tests.run + t(" pruebas", " tests")
    + " · scripts/verify.py · " + String(evidence.generated_utc || "").slice(0, 10)],
   [t("Revisión independiente", "Independent review"), typeof review === "string" ? read(review)
    : [read(review.status), review.by, review.date, typeof review.scope === "object" ? t(review.scope.es, review.scope.en) : review.scope].filter(Boolean).join(" · ")],
   [t("Aceptación del dueño", "Owner acceptance"), read(status.acceptance)],
   [t("Integración", "Integration"), status.integration ? read(status.integration.state) + " · main " + String(status.integration.main || "").slice(0, 7) : "—"],
   [t("Despliegue", "Deployment"), status.deployment ? t("Pages publica ", "Pages serves ") + status.deployment.pages_source.replace(/([0-9a-f]{7})[0-9a-f]{33}/, "$1")
    + " · " + t("esta revisión: ", "this revision: ") + read(status.deployment.this_branch) : "—"],
  ];
  el("statusList").replaceChildren(...rows.flatMap(([k, v]) => {
   const dt = document.createElement("dt"), dd = document.createElement("dd");
   dt.textContent = k; dd.textContent = v; return [dt, dd];
  }));
  // R42c: baseline and fingerprints come from evidence/latest.json, compared with this checkout.
  const same = status.source_fingerprint && status.source_fingerprint === evidence.source_id
   && status.record_fingerprint && status.record_fingerprint === evidence.record_id;
  el("runDetail").textContent = t("Base de la ejecución: ", "Run baseline: ") + String(evidence.input_revision || "—").slice(0, 7)
   + (evidence.input_worktree_dirty ? t(" con cambios sin confirmar", " with uncommitted changes") : "")
   + t(". Huellas: fuentes ", ". Fingerprints: sources ") + String(evidence.source_id || "—").slice(0, 12)
   + t(", registros ", ", records ") + String(evidence.record_id || "—").slice(0, 12) + ". "
   + (same ? t("Coinciden con las fuentes y registros de esta revisión; la revisión entregada es el commit que contiene evidence/latest.json.",
               "They match the sources and records of this revision; the delivered revision is the commit that contains evidence/latest.json.")
           : t("No coinciden con esta revisión: trátala como evidencia histórica.",
               "They do not match this revision: treat it as historical evidence."));
  const rev = String(status.revision || "");
  const live = document.createElement("a");
  Object.assign(live, { href: REPO + "/tree/main", target: "_blank", rel: "noopener noreferrer",
   textContent: t("main en vivo (puede incluir cambios posteriores)", "live main (may include later changes)") });
  el("revisionDetail").replaceChildren(
   (rev ? t("Los enlaces a archivos abren la revisión ", "File links open revision ") + rev.slice(0, 7)
     + (status.revision_dirty ? t(", de la que se generó esta página con cambios sin confirmar que esos enlaces no incluyen", ", which this page was produced from with uncommitted changes those links do not include")
                              : t(", de la que se generó esta página", ", which this page was produced from"))
     + t("; los casos históricos abren el commit que los registró. ", "; historical cases open the commit that recorded them. ")
    : t("Sin revisión registrada: los enlaces abren main. ", "No recorded revision: links open main. ")),
   t("Navegación viva: ", "Live navigation: "), live);
 }

 function render() {
  const ready = !!evidence && requirements.length > 0;
  el("evidenceMetrics").hidden = el("evidenceExplorer").hidden = !ready;
  if (!ready) {
   el("evidenceStatus").textContent = failed
    ? t("Sin evidencia cargada: no se pudieron leer los datos.", "No evidence loaded: the data could not be read.")
    : t("Sin evidencia cargada.", "No evidence loaded.");
   return;
  }
  el("evidenceStatus").textContent = "";
  pinLinks();
  renderStatus();
  const tests = evidence.tests || {};
  el("evGenerated").textContent = String(evidence.generated_utc || "—").slice(0, 16).replace("T", " ");
  el("evTests").textContent = [tests.run, tests.failures, tests.errors].join(" · ");
  el("evScenarios").textContent = String(evidence.scenario_evaluation?.cases?.length ?? "—");
  el("evResult").textContent = evidence.passed === true ? "PASS" : "FAIL";
  const source = document.createElement("small");
  source.textContent = "source " + String(evidence.source_id || "—").slice(0, 8);
  el("evCommit").replaceChildren(String(evidence.input_revision || "—").slice(0, 8)
   + (evidence.input_worktree_dirty ? t(" · árbol sucio", " · dirty tree") : ""), source);
  const picker = el("reqPicker"), linked = (location.hash.match(/^#evidence\/(R\d+)$/) || [])[1];
  const selected = linked || picker.value || "R02";
  picker.replaceChildren(...requirements.map((r) => new Option(r.id + " — " + (r.text.length > 90 ? r.text.slice(0, 89) + "…" : r.text), r.id)));
  picker.value = requirements.some((r) => r.id === selected) ? selected : requirements[0].id;
  renderCases();
 }

 async function load() {
  try {
   const read = async (path, kind) => {
    const response = await fetch(path);
    if (!response.ok) throw new Error(path);
    return response[kind]();
   };
   const [e, csv, reqs, st] = await Promise.all([read("/api/evidence", "json"), read("/api/acceptance", "text"),
    read("/api/requirements", "json"), read("/api/status", "json")]);
   evidence = e; cases = parseCsv(csv); requirements = reqs; status = st;
  } catch { failed = true; }
  render();
 }

 el("reqPicker").addEventListener("change", renderCases);
 window.addEventListener("languagechange", render);
 // Tour links such as #evidence/R03 select that requirement (R35a).
 window.addEventListener("hashchange", () => { if (/^#evidence\/R\d+$/.test(location.hash) && requirements.length) render(); });
 render();
 load();
})();
