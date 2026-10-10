"use strict";
// Public static build only (scripts/build_pages.py). Answers /api/* inside the browser with a port of
// src/lab/controller.py, so the GitHub Pages demo needs no server, keys or visitor data.
// The local server never serves this file; model and MCP connections stay local-only.
(() => {
 document.documentElement.classList.add("public-demo");
 const realFetch = window.fetch.bind(window);
 const json = (name) => realFetch("data/" + name).then((r) => r.json());
 const data = Promise.all(["orders.json", "policy.json", "scenarios.json", "roles.json", "business_cases.json"].map(json))
  .then(([orders, policy, scenarios, roles, businessCases]) => ({ orders: Object.fromEntries(orders.map((r) => [r.id, r])), policy, scenarios, roles, businessCases }));

 // Same canonical form as src/lab/hooks.py: sorted keys, no spaces, ASCII escapes.
 const canonical = (v) => Array.isArray(v) ? "[" + v.map(canonical).join(",") + "]"
  : v && typeof v === "object" ? "{" + Object.keys(v).sort().map((k) => JSON.stringify(k) + ":" + canonical(v[k])).join(",") + "}"
  : JSON.stringify(v);
 const digest = async (v) => {
  const text = canonical(v).replace(/[\u0080-￿]/g, (c) => "\\u" + c.charCodeAt(0).toString(16).padStart(4, "0"));
  const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(hash)].map((b) => b.toString(16).padStart(2, "0")).join("");
 };
 const copy = (v) => JSON.parse(JSON.stringify(v));
 class RuleError extends Error {}

 const proposals = {}, receipts = {}, events = [], custom = [];
 let orders, policy;
 async function audit(phase, action, outcome, reference = "") {
  const event = { sequence: events.length + 1, phase, action, outcome, reference,
   previous: events.length ? events[events.length - 1].hash : "GENESIS" };
  event.hash = await digest(event);
  events.push(event);
 }
 async function chainValid() {
  let previous = "GENESIS";
  for (const [i, original] of events.entries()) {
   const { hash, ...event } = original;
   if (event.sequence !== i + 1 || event.previous !== previous || await digest(event) !== hash) return false;
   previous = hash;
  }
  return true;
 }
 function order(id) {
  const row = orders[id];
  // Do not disclose whether a resource outside this workspace exists.
  if (!row || row.workspace !== "sample-store") throw new RuleError("ORDER_UNAVAILABLE");
  return row;
 }
 function eligible(row) {
  if (Object.values(receipts).some((r) => r.order_id === row.id)) throw new RuleError("ALREADY_COMPENSATED");
  if (row.status !== "delivered") throw new RuleError("NOT_DELIVERED");
  if (row.days_since_delivery > policy.window_days) throw new RuleError("OUTSIDE_WINDOW");
  if (row.amount > policy.max_refund) throw new RuleError("ABOVE_LIMIT");
 }

 async function request(body) {
  await audit("before", "request", "CHECKING");
  try {
   if (Object.keys(body || {}).sort().join() !== "intent,order_id" || !Object.values(body).every((v) => typeof v === "string")) throw new RuleError("INVALID_REQUEST");
   if (!["lookup", "refund"].includes(body.intent)) throw new RuleError("TOOL_NOT_ALLOWED");
   const row = order(body.order_id);
   let result;
   if (body.intent === "lookup") result = { status: "READ_ONLY", order: copy(row) };
   else {
    eligible(row);
    // Repeated identical proposals do not create new execution identities.
    const key = (await digest({ order: row, policy })).slice(0, 20);
    proposals[key] ??= { id: key, order_id: row.id, amount: row.amount, order_version: row.version,
     order_digest: await digest(row), policy_digest: await digest(policy), status: "PENDING_APPROVAL" };
    result = copy(proposals[key]);
   }
   await audit("after", "request", result.status, row.id);
   return [200, result];
  } catch (e) {
   if (!(e instanceof RuleError)) throw e;
   await audit("after", "request", e.message);
   return [200, { status: "BLOCKED", reason: e.message }];
  }
 }
 async function decide(body) {
  await audit("before", "decision", "CHECKING");
  if (!["approve", "reject"].includes(body.decision)) throw new RuleError("INVALID_DECISION");
  const p = proposals[body.proposal_id];
  if (!p) throw new RuleError("PROPOSAL_UNAVAILABLE");
  if (p.status !== "PENDING_APPROVAL") throw new RuleError("INVALID_TRANSITION");
  p.status = body.decision === "approve" ? "APPROVED" : "REJECTED";
  await audit("after", "decision", p.status, p.id);
  return [200, copy(p)];
 }
 async function execute(body) {
  await audit("before", "execute", "CHECKING");
  const p = proposals[body.proposal_id];
  if (!p) throw new RuleError("PROPOSAL_UNAVAILABLE");
  if (receipts[p.id]) { await audit("after", "execute", "REPLAY", p.id); return [200, copy(receipts[p.id])]; }
  if (p.status !== "APPROVED") throw new RuleError("APPROVAL_REQUIRED");
  const row = order(p.order_id);
  if (p.policy_digest !== await digest(policy) || p.order_version !== row.version || p.order_digest !== await digest(row)) throw new RuleError("STALE_PROPOSAL");
  eligible(row);
  if (body.fail_connector === true) throw new RuleError("SIMULATED_CONNECTOR_FAILURE");
  // Local receipt only, never a financial operation.
  receipts[p.id] = { id: "SIM-" + p.id, order_id: row.id, amount: p.amount, currency: "DEMO", status: "SIMULATED", real_effect: false };
  p.status = "SIMULATED";
  await audit("after", "execute", "SIMULATED", p.id);
  return [200, copy(receipts[p.id])];
 }
 // decide/execute record the rule outcome and answer 409, like src/lab/server.py.
 const ruled = (fn, action) => async (body) => {
  try { return await fn(body); } catch (e) {
   if (!(e instanceof RuleError)) throw e;
   await audit("after", action, e.message);
   return [409, { status: "BLOCKED", reason: e.message }];
  }
 };
 // Agent definitions live only in this tab's memory: nothing is stored or sent.
 function saveAgent(body) {
  const row = {};
  for (const k of ["id", "name", "role", "prompt", "work_mode"]) row[k] = typeof body[k] === "string" ? body[k].trim() : null;
  const valid = [["name", 2, 80], ["role", 3, 160], ["prompt", 20, 4000]].every(([k, lo, hi]) => row[k] && row[k].length >= lo && row[k].length <= hi)
   && ["plan", "research", "implementation", "review"].includes(row.work_mode) && row.id !== null;
  if (!valid) return [400, { error: "AGENT_DEFINITION_INVALID" }];
  if (/sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----/.test(JSON.stringify(row))) return [400, { error: "AGENT_SENSITIVE_INPUT" }];
  const index = custom.findIndex((x) => x.id === row.id);
  if (row.id && index < 0) return [404, { error: "AGENT_NOT_FOUND" }];
  if (index >= 0) custom[index] = row;
  else {
   if (custom.length >= 50) return [409, { error: "AGENT_STORE_FULL" }];
   row.id = "custom-" + crypto.randomUUID().replace(/-/g, "");
   custom.push(row);
  }
  return [200, copy(row)];
 }

 // Business case (R28, R29): port of src/lab/business_case.py; same field order and arithmetic.
 const TEXT_FIELDS = ["company", "problem", "users", "current_process", "constraints", "success"];
 const NUMBER_FIELDS = { monthly_volume: [1, 1000000], minutes_per_case: [0.1, 600] };
 const CHOICE_FIELDS = { data_sensitivity: ["none", "internal", "personal"], action_type: ["inform", "recommend", "execute"] };
 const DIAGNOSIS_FIELDS = [...TEXT_FIELDS, ...Object.keys(NUMBER_FIELDS), ...Object.keys(CHOICE_FIELDS)];
 const ESTIMATE_FIELDS = { monthly_volume: [1, 1000000], manual_minutes: [0.1, 600], assisted_minutes: [0, 600], review_rate: [0, 1],
  hourly_cost: [0, 100000], implementation_cost: [0, 10000000], monthly_operation_cost: [0, 1000000] };
 const SCENARIOS = [["conservative", 1.25, 0.10], ["base", 1.0, 0.0], ["optimistic", 0.8, -0.05]];
 const LOW_VOLUME_MINUTES = 600, PAYBACK_LIMIT_MONTHS = 12;
 const money = (v) => Math.floor(v * 100 + 0.5) / 100;
 const isNumber = (v) => typeof v === "number" && Number.isFinite(v);
 const isObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
 function diagnose(body) {
  if (!isObject(body) || Object.keys(body).some((k) => !DIAGNOSIS_FIELDS.includes(k))) return [400, { status: "INVALID_INPUT", fields: ["_shape"] }];
  const invalid = [], answers = {};
  for (const f of TEXT_FIELDS) {
   const v = body[f];
   if (v === undefined || v === null || (typeof v === "string" && !v.trim())) continue;
   if (typeof v !== "string" || v.trim().length > 500) invalid.push(f); else answers[f] = v.trim();
  }
  for (const [f, [lo, hi]] of Object.entries(NUMBER_FIELDS)) {
   const v = body[f];
   if (v === undefined || v === null) continue;
   if (!isNumber(v) || !(lo <= v && v <= hi)) invalid.push(f); else answers[f] = v;
  }
  for (const [f, options] of Object.entries(CHOICE_FIELDS)) {
   const v = body[f];
   if (v === undefined || v === null || v === "") continue;
   if (!options.includes(v)) invalid.push(f); else answers[f] = v;
  }
  if (invalid.length) return [400, { status: "INVALID_INPUT", fields: invalid }];
  const missing = DIAGNOSIS_FIELDS.filter((f) => !(f in answers));
  const action = answers.action_type;
  const level = { inform: "ASSIST", recommend: "PROPOSE_AND_APPROVE", execute: "PROPOSE_AND_APPROVE" }[action] ?? null;
  const risks = [];
  if (answers.data_sensitivity === "personal") risks.push("PERSONAL_DATA");
  if (action === "execute") risks.push("EXECUTION_NEEDS_APPROVAL");
  if ("monthly_volume" in answers && "minutes_per_case" in answers) {
   if (answers.monthly_volume * answers.minutes_per_case < LOW_VOLUME_MINUTES) risks.push("LOW_VOLUME");
  } else risks.push("UNMEASURED_BASELINE");
  return [200, { status: missing.length ? "BRIEF_INCOMPLETE" : "BRIEF_READY",
   confirmed: DIAGNOSIS_FIELDS.filter((f) => f in answers).map((f) => ({ field: f, value: answers[f] })),
   open_questions: missing, recommended_level: level, risks,
   first_increment: { ASSIST: "DRAFT_WITH_HUMAN_DECISION", PROPOSE_AND_APPROVE: "PROPOSAL_WITH_APPROVAL_GATE" }[level] ?? "DEFINE_ACTION_FIRST",
   estimate_inputs: Object.fromEntries(["monthly_volume", "minutes_per_case"].filter((k) => k in answers).map((k) => [k, answers[k]])) }];
 }
 function scenario(name, v, assistedFactor, reviewShift) {
  const assisted = v.assisted_minutes * assistedFactor;
  const review = Math.min(1, Math.max(0, v.review_rate + reviewShift));
  const minutesSaved = v.monthly_volume * (1 - review) * (v.manual_minutes - assisted);
  const hoursSaved = minutesSaved / 60;
  const gross = hoursSaved * v.hourly_cost;
  const net = gross - v.monthly_operation_cost;
  const payback = net > 0 ? v.implementation_cost / net : null;
  return { scenario: name, assisted_minutes: money(assisted), review_rate: money(review), hours_saved_per_month: money(hoursSaved),
   gross_benefit_per_month: money(gross), net_benefit_per_month: money(net), payback_months: payback === null ? null : money(payback),
   first_year_net: money(net * 12 - v.implementation_cost) };
 }
 function estimate(body) {
  const keys = Object.keys(ESTIMATE_FIELDS);
  if (!isObject(body) || Object.keys(body).length !== keys.length || !keys.every((k) => k in body)) return [400, { status: "INVALID_INPUT", fields: ["_shape"] }];
  const invalid = keys.filter((f) => !isNumber(body[f]) || !(ESTIMATE_FIELDS[f][0] <= body[f] && body[f] <= ESTIMATE_FIELDS[f][1]));
  if (invalid.length) return [400, { status: "INVALID_INPUT", fields: invalid }];
  const rows = SCENARIOS.map(([n, a, r]) => scenario(n, body, a, r)), base = rows[1].payback_months;
  return [200, { status: "ESTIMATE", kind: "ESTIMATE_NOT_OBSERVED", currency: "DEMO", observed_savings: 0, inputs: copy(body), scenarios: rows,
   recommendation: base !== null && base <= PAYBACK_LIMIT_MONTHS ? "PILOT" : "REVISIT_SCOPE", payback_limit_months: PAYBACK_LIMIT_MONTHS,
   factors: SCENARIOS.map(([n, a, r]) => ({ scenario: n, assisted_factor: a, review_shift: r })) }];
 }

 const routes = {
  "GET /api/state": async () => [200, { mode: "DETERMINISTIC_DEMO", model_calls: 0, external_requests: 0, real_effects: 0,
   proposals: copy(Object.values(proposals)), receipts: copy(Object.values(receipts)), events: copy(events),
   audit_chain_valid: await chainValid(),
   limitations: ["Browser-memory session", "Reviewer role is simulated, not real authentication", "No LLM quality or production readiness claim"] }],
  "GET /api/scenarios": async () => [200, (await data).scenarios],
  "GET /api/business/cases": async () => [200, (await data).businessCases],
  "POST /api/business/diagnose": async (body) => diagnose(body),
  "POST /api/business/estimate": async (body) => estimate(body),
  "GET /api/agents": async () => [200, Object.entries((await data).roles).map(([id, v]) => ({ id, name: v.name, mission: v.mission,
   obligations: v.obligations, tools: ["local_artifact"], hooks: ["input", "permission", "output", "evidence"], can_execute_code: false }))],
  "GET /api/custom-agents": async () => [200, copy(custom)],
  "GET /api/model-catalog": async () => [200, { checked_on: "", kind: "public_demo", models: [] }],
  "POST /api/custom-agents/save": saveAgent,
  "POST /api/request": request,
  "POST /api/decision": ruled(decide, "decision"),
  "POST /api/execute": ruled(execute, "execute"),
 };
 // Evidence view data: the committed files written by scripts/build_pages.py, returned unchanged.
 const files = { "/api/evidence": "latest.json", "/api/acceptance": "acceptance.csv", "/api/requirements": "requirements.json" };
 let queue = Promise.resolve();
 window.fetch = (input, init = {}) => {
  const url = new URL(typeof input === "string" ? input : input.url, location.href);
  const at = url.pathname.indexOf("/api/");
  if (at < 0) return realFetch(input, init);
  const file = files[url.pathname.slice(at)];
  if (file && (init.method || "GET") === "GET") return realFetch("data/" + file);
  const route = routes[(init.method || "GET") + " " + url.pathname.slice(at)];
  const run = async () => {
   ({ orders, policy } = await data);
   const [status, body] = route ? await route(init.body ? JSON.parse(init.body) : {}) : [403, { error: "PUBLIC_DEMO_DISABLED" }];
   return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
  };
  // ponytail: one global queue stands in for the controller's RLock; fine for one visitor per tab.
  return (queue = queue.then(run, run));
 };
})();
