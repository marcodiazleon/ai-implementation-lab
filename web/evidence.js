"use strict";
// Evidence view (R27). Shows what scripts/verify.py recorded; it never recalculates a test result.
(() => {
 const el = (id) => document.getElementById(id);
 const repo = "https://github.com/marcodiazleon/ai-implementation-lab/blob/main/";
 const t = (es, en) => (LabI18n.language === "en" ? en : es);
 let evidence = null, cases = [], requirements = [], failed = false;

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

 // Never approved by default: FAIL wins, PASS needs recorded evidence, anything else is pending.
 function badge(id) {
  const own = cases.filter((c) => c.requirement_id === id);
  if (own.some((c) => c.status === "FAIL")) return "FAIL";
  if (own.some((c) => c.status === "PASS" && c.evidence.trim())) return "PASS";
  return "PENDIENTE";
 }

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
   + (state === "PENDIENTE" ? t(" · sin caso PASS con evidencia", " · no PASS case with evidence") : "");
  el("reqCases").replaceChildren(...own.map((c) => {
   const tr = document.createElement("tr");
   for (const value of [c.case_id, c.action, c.expected, c.status, c.test_id]) cell(tr, value);
   let link = c.evidence || "—";
   if (/^[\w.-]+(\/[\w.-]+)+$/.test(c.evidence) && !c.evidence.split("/").includes("..")) {
    link = document.createElement("a");
    Object.assign(link, { href: repo + c.evidence, textContent: c.evidence, target: "_blank", rel: "noopener noreferrer" });
   }
   cell(tr, link);
   return tr;
  }));
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
  const tests = evidence.tests || {};
  el("evGenerated").textContent = String(evidence.generated_utc || "—").slice(0, 16).replace("T", " ");
  el("evTests").textContent = [tests.run, tests.failures, tests.errors].join(" · ");
  el("evScenarios").textContent = String(evidence.scenario_evaluation?.cases?.length ?? "—");
  el("evResult").textContent = evidence.passed === true ? "PASS" : "FAIL";
  const source = document.createElement("small");
  source.textContent = "source " + String(evidence.source_id || "—").slice(0, 8);
  el("evCommit").replaceChildren(String(evidence.input_revision || "—").slice(0, 8)
   + (evidence.input_worktree_dirty ? t(" · árbol sucio", " · dirty tree") : ""), source);
  const picker = el("reqPicker"), selected = picker.value || "R02";
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
   const [e, csv, reqs] = await Promise.all([read("/api/evidence", "json"), read("/api/acceptance", "text"), read("/api/requirements", "json")]);
   evidence = e; cases = parseCsv(csv); requirements = reqs;
  } catch { failed = true; }
  render();
 }

 el("reqPicker").addEventListener("change", renderCases);
 window.addEventListener("languagechange", render);
 render();
 load();
})();
