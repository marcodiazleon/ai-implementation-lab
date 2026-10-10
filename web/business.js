"use strict";
// Business case view (R28, R29). Calls /api/business/*; the browser formats results and computes nothing.
(() => {
 const el = (id) => document.getElementById(id);
 const t = (es, en) => (LabI18n.language === "en" ? en : es);
 const pick = (pair) => t(pair[0], pair[1]);
 let cases = [], brief = null, result = null, notice = null;

 const FIELDS = {
  company: ["Empresa o área", "Company or area", "¿Qué empresa o área tiene el problema?", "Which company or area has the problem?"],
  problem: ["Problema", "Problem", "¿Qué problema concreto hay que resolver?", "What concrete problem needs solving?"],
  users: ["Quién hace el trabajo hoy", "Who does the work today", "¿Quién hace hoy este trabajo?", "Who does this work today?"],
  current_process: ["Proceso y sistemas actuales", "Current process and systems", "¿Cómo se hace hoy y con qué sistemas?", "How is it done today and with which systems?"],
  monthly_volume: ["Casos al mes", "Cases per month", "¿Cuántos casos hay al mes? Medirlo antes de estimar.", "How many cases per month? Measure it before estimating."],
  minutes_per_case: ["Minutos por caso", "Minutes per case", "¿Cuántos minutos toma cada caso hoy? Medirlo antes de estimar.", "How many minutes does each case take today? Measure it before estimating."],
  constraints: ["Restricciones", "Constraints", "¿Qué restricciones legales, técnicas o de aprobación existen?", "What legal, technical or approval constraints exist?"],
  success: ["Cómo se ve el éxito", "What success looks like", "¿Qué resultado medible definiría el éxito?", "What measurable result would define success?"],
  data_sensitivity: ["Datos involucrados", "Data involved", "¿Qué tipo de datos se tocan?", "What kind of data is involved?"],
  action_type: ["Qué debe hacer la IA", "What the AI should do", "¿La IA solo informa, recomienda o ejecuta?", "Should the AI inform, recommend or execute?"],
 };
 const VALUES = { none: ["Sin datos sensibles", "No sensitive data"], internal: ["Datos internos", "Internal data"], personal: ["Datos personales", "Personal data"],
  inform: ["Informar o redactar", "Inform or draft"], recommend: ["Recomendar una decisión", "Recommend a decision"], execute: ["Ejecutar una acción", "Execute an action"] };
 const LEVELS = {
  ASSIST: ["Asistir: la IA redacta o consulta y una persona decide.", "Assist: the AI drafts or looks up and a person decides."],
  PROPOSE_AND_APPROVE: ["Proponer y aprobar: la IA prepara la acción y una persona la aprueba antes de cualquier efecto.", "Propose and approve: the AI prepares the action and a person approves it before any effect."],
 };
 const RISKS = {
  PERSONAL_DATA: ["Datos personales: seudonimizar antes de enviarlos a un modelo y confirmar la base legal.", "Personal data: pseudonymize before sending to a model and confirm the legal basis."],
  EXECUTION_NEEDS_APPROVAL: ["Acción con efecto real: aprobación humana obligatoria y registro de cada intento.", "Action with real effect: mandatory human approval and a log of every attempt."],
  LOW_VOLUME: ["Volumen bajo: menos de 10 horas de trabajo al mes; puede no compensar automatizar.", "Low volume: under 10 hours of work per month; automation may not pay off."],
  UNMEASURED_BASELINE: ["Sin línea base medida: falta el volumen o el tiempo por caso; cualquier ahorro sería una suposición.", "No measured baseline: volume or time per case is missing; any saving would be a guess."],
 };
 const INCREMENTS = {
  DRAFT_WITH_HUMAN_DECISION: ["Un asistente que prepara borradores con fuentes; la persona revisa y envía.", "An assistant that prepares drafts with sources; the person reviews and sends."],
  PROPOSAL_WITH_APPROVAL_GATE: ["Un flujo que propone la acción, espera aprobación y evita duplicados al reintentar.", "A flow that proposes the action, waits for approval and avoids duplicates on retry."],
  DEFINE_ACTION_FIRST: ["Primero definir qué debe hacer la IA; sin eso no se puede acotar un incremento.", "First define what the AI should do; without it no increment can be scoped."],
 };
 const SCENARIOS = { conservative: ["Conservador", "Conservative"], base: ["Base", "Base"], optimistic: ["Optimista", "Optimistic"] };
 const ESTIMATE_INPUTS = { monthly_volume: "bcEVolume", manual_minutes: "bcEManual", assisted_minutes: "bcEAssisted", review_rate: "bcEReview",
  hourly_cost: "bcEHourly", implementation_cost: "bcEImpl", monthly_operation_cost: "bcEOp" };
 const ESTIMATE_LABELS = { monthly_volume: ["Casos al mes", "Cases per month"], manual_minutes: ["Minutos manuales", "Manual minutes"],
  assisted_minutes: ["Minutos asistidos", "Assisted minutes"], review_rate: ["Casos a mano", "Manual share"], hourly_cost: ["Costo por hora", "Cost per hour"],
  implementation_cost: ["Implantación", "Implementation"], monthly_operation_cost: ["Operación mensual", "Monthly operation"] };
 const DIAGNOSIS_INPUTS = { company: "bcCompany", problem: "bcProblem", users: "bcUsers", current_process: "bcCurrent", monthly_volume: "bcVolume",
  minutes_per_case: "bcMinutes", constraints: "bcConstraints", success: "bcSuccess", data_sensitivity: "bcSensitivity", action_type: "bcAction" };

 const number = (value) => new Intl.NumberFormat(LabI18n.language === "en" ? "en-US" : "es-MX", { maximumFractionDigits: 2 }).format(value);
 const node = (tag, text, cls) => { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (cls) n.className = cls; return n; };
 const list = (items) => { const ul = node("ul"); ul.append(...items.map((i) => node("li", i))); return ul; };
 const readNumber = (id) => (el(id).value.trim() === "" ? null : Number(el(id).value));
 const shown = (field, value) => (VALUES[value] ? pick(VALUES[value]) : typeof value === "number" ? number(value) : value);

 async function post(path, body) {
  const response = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  return response.json();
 }

 function renderBrief() {
  const out = el("bcBrief");
  if (!brief) { out.replaceChildren(); return; }
  if (brief.status === "INVALID_INPUT") {
   out.replaceChildren(node("p", t("Revisa estos campos: ", "Check these fields: ") + brief.fields.map((f) => FIELDS[f] ? pick(FIELDS[f]) : f).join(", "), "result blocked"));
   return;
  }
  const ready = brief.status === "BRIEF_READY";
  const badge = node("span", ready ? t("BRIEF LISTO", "BRIEF READY") : t("BORRADOR · FALTA INFORMACIÓN", "DRAFT · INFORMATION MISSING"), "badge");
  badge.dataset.state = ready ? "PASS" : "PENDIENTE";
  const parts = [badge, node("h3", t("Lo que se confirmó", "What was confirmed")),
   list(brief.confirmed.map((c) => pick(FIELDS[c.field]) + ": " + shown(c.field, c.value))),
   node("h3", t("Preguntas abiertas", "Open questions")),
   brief.open_questions.length ? list(brief.open_questions.map((f) => t(FIELDS[f][2], FIELDS[f][3]))) : node("p", t("Ninguna.", "None."), "muted"),
   node("h3", t("Nivel de automatización recomendado", "Recommended automation level")),
   node("p", brief.recommended_level ? pick(LEVELS[brief.recommended_level]) : t("Pendiente: falta saber qué debe hacer la IA.", "Pending: it is not yet known what the AI should do.")),
   node("h3", t("Riesgos y controles", "Risks and controls")),
   brief.risks.length ? list(brief.risks.map((r) => pick(RISKS[r]))) : node("p", t("Ninguno identificado con estas respuestas.", "None identified from these answers."), "muted"),
   node("h3", t("Primer incremento", "First increment")), node("p", pick(INCREMENTS[brief.first_increment]))];
  if (brief.recommended_level === "PROPOSE_AND_APPROVE") {
   const link = node("a", t("Ver este tipo de incremento funcionando en la demo de devoluciones", "See this kind of increment working in the refund demo"));
   link.href = "#workspace";
   const paragraph = node("p"); paragraph.append(link); parts.push(paragraph);
  }
  parts.push(node("p", t("Las respuestas que faltan quedan como preguntas abiertas; no se convierten en requisitos.", "Missing answers stay as open questions; they never become requirements."), "muted"));
  out.replaceChildren(...parts);
 }

 function renderEstimate() {
  const verdict = el("bcVerdict"), wrap = el("bcTableWrap"), note = el("bcEstimateNote");
  verdict.hidden = wrap.hidden = note.hidden = !result;
  el("bcDownload").disabled = !(result && result.status === "ESTIMATE") && !(brief && brief.status !== "INVALID_INPUT");
  if (!result) return;
  if (result.status === "INVALID_INPUT") {
   verdict.textContent = t("Revisa estos campos: ", "Check these fields: ") + result.fields.map((f) => ESTIMATE_LABELS[f] ? pick(ESTIMATE_LABELS[f]) : f).join(", ");
   verdict.classList.add("blocked"); wrap.hidden = note.hidden = true; return;
  }
  const base = result.scenarios[1];
  const pilot = result.recommendation === "PILOT";
  verdict.classList.toggle("blocked", !pilot);
  verdict.textContent = pilot
   ? t("Recomendación: hacer un piloto. El escenario base recupera la implantación en " + number(base.payback_months) + " meses (umbral: " + result.payback_limit_months + ").",
       "Recommendation: run a pilot. The base scenario pays back the implementation in " + number(base.payback_months) + " months (threshold: " + result.payback_limit_months + ").")
   : t("Recomendación: replantear el alcance antes de construir. El escenario base no recupera la implantación en " + result.payback_limit_months + " meses.",
       "Recommendation: revisit the scope before building. The base scenario does not pay back the implementation within " + result.payback_limit_months + " months.");
  el("bcScenarios").replaceChildren(...result.scenarios.map((s) => {
   const tr = node("tr");
   tr.append(node("th", pick(SCENARIOS[s.scenario])), node("td", number(s.hours_saved_per_month) + " h"),
    node("td", number(s.net_benefit_per_month) + " DEMO"),
    node("td", s.payback_months === null ? t("No se recupera", "Does not pay back") : number(s.payback_months) + t(" meses", " months")),
    node("td", number(s.first_year_net) + " DEMO"));
   tr.firstChild.scope = "row";
   return tr;
  }));
  note.textContent = t("Estimación a partir de supuestos, en unidades DEMO ficticias. Ahorro observado: 0. No es un resultado obtenido.",
   "Estimate from assumptions, in fictional DEMO units. Observed savings: 0. This is not an achieved result.");
 }

 function render() {
  for (const option of el("bcPreset").options) {
   const row = cases.find((c) => c.id === option.value);
   if (row) option.textContent = pick([row.title.es, row.title.en]);
  }
  renderBrief(); renderEstimate();
  if (notice) { el("bcBrief").replaceChildren(node("p", pick(notice), "result blocked")); }
 }

 function fill(row) {
  for (const [field, id] of Object.entries(DIAGNOSIS_INPUTS)) {
   const value = row ? row.diagnosis[field] : null;
   el(id).value = value === null || value === undefined ? "" : String(value);
  }
  for (const [field, id] of Object.entries(ESTIMATE_INPUTS)) {
   const value = row ? row.estimate[field] : null;
   el(id).value = value === null || value === undefined ? "" : String(field === "review_rate" ? Math.round(value * 100) : value);
  }
  brief = result = notice = null; render();
 }

 async function run(fn) {
  try { notice = null; await fn(); }
  catch { notice = ["No se pudo calcular: comprueba que el servidor local siga activo.", "Could not calculate: check that the local server is still running."]; }
  render();
 }

 el("bcPreset").addEventListener("change", () => fill(cases.find((c) => c.id === el("bcPreset").value)));
 el("bcDiagForm").addEventListener("submit", (event) => {
  event.preventDefault();
  run(async () => {
   const body = {};
   for (const [field, id] of Object.entries(DIAGNOSIS_INPUTS)) {
    body[field] = ["monthly_volume", "minutes_per_case"].includes(field) ? readNumber(id) : el(id).value;
   }
   brief = await post("/api/business/diagnose", body);
   // Carry measured figures into the estimate; never invent the missing ones.
   for (const [field, id] of [["monthly_volume", "bcEVolume"], ["minutes_per_case", "bcEManual"]]) {
    if (brief.estimate_inputs && field in brief.estimate_inputs) el(id).value = String(brief.estimate_inputs[field]);
   }
  });
 });
 el("bcEstForm").addEventListener("submit", (event) => {
  event.preventDefault();
  run(async () => {
   const body = {};
   for (const [field, id] of Object.entries(ESTIMATE_INPUTS)) {
    const value = readNumber(id);
    body[field] = field === "review_rate" && value !== null ? value / 100 : value;
   }
   result = await post("/api/business/estimate", body);
  });
 });
 el("bcDownload").addEventListener("click", () => {
  const lines = ["# " + t("Caso de negocio", "Business case"), ""];
  if (brief && brief.status !== "INVALID_INPUT") {
   lines.push("## " + t("Diagnóstico", "Diagnosis"), "", t("Estado: ", "Status: ") + brief.status, "");
   for (const c of brief.confirmed) lines.push("- " + pick(FIELDS[c.field]) + ": " + shown(c.field, c.value));
   lines.push("", "### " + t("Preguntas abiertas", "Open questions"), "", ...(brief.open_questions.length ? brief.open_questions.map((f) => "- " + t(FIELDS[f][2], FIELDS[f][3])) : ["- " + t("Ninguna.", "None.")]));
   lines.push("", "### " + t("Riesgos y controles", "Risks and controls"), "", ...brief.risks.map((r) => "- " + pick(RISKS[r])));
   lines.push("", "### " + t("Primer incremento", "First increment"), "", pick(INCREMENTS[brief.first_increment]), "");
  }
  if (result && result.status === "ESTIMATE") {
   lines.push("## " + t("Estimación (DEMO, supuestos)", "Estimate (DEMO, assumptions)"), "", el("bcVerdict").textContent, "",
    "| " + [t("Escenario", "Scenario"), t("Horas/mes", "Hours/month"), t("Neto/mes", "Net/month"), t("Recuperación", "Payback"), t("Neto año 1", "Year-one net")].join(" | ") + " |",
    "|---|---|---|---|---|");
   for (const s of result.scenarios) lines.push("| " + [pick(SCENARIOS[s.scenario]), number(s.hours_saved_per_month), number(s.net_benefit_per_month),
    s.payback_months === null ? t("No se recupera", "Does not pay back") : number(s.payback_months), number(s.first_year_net)].join(" | ") + " |");
   lines.push("", el("bcEstimateNote").textContent);
  }
  const url = URL.createObjectURL(new Blob([lines.join("\n") + "\n"], { type: "text/markdown" }));
  const a = node("a"); a.href = url; a.download = t("caso-de-negocio.md", "business-case.md");
  document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 10000);
 });
 window.addEventListener("languagechange", render);

 (async () => {
  try {
   const response = await fetch("/api/business/cases");
   if (!response.ok) throw new Error("cases");
   cases = await response.json();
   el("bcPreset").append(...cases.map((c) => new Option(pick([c.title.es, c.title.en]), c.id)));
   el("bcPreset").value = cases[0].id; fill(cases[0]);
  } catch { notice = ["No se pudieron cargar los ejemplos. Puedes usar el formulario en blanco.", "The examples could not be loaded. You can use the blank form."]; render(); }
 })();
})();
