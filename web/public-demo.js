"use strict";
// Public static build only (scripts/build_pages.py). Answers /api/* inside the browser with a port of
// src/lab/controller.py, so the GitHub Pages demo needs no server, keys or visitor data.
// The local server never serves this file; model and MCP connections stay local-only.
(() => {
 document.documentElement.classList.add("public-demo");
 const realFetch = window.fetch.bind(window);
 const json = (name) => realFetch("data/" + name).then((r) => r.json());
 const data = Promise.all(["orders.json", "policy.json", "scenarios.json", "roles.json"].map(json))
  .then(([orders, policy, scenarios, roles]) => ({ orders: Object.fromEntries(orders.map((r) => [r.id, r])), policy, scenarios, roles }));

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

 const routes = {
  "GET /api/state": async () => [200, { mode: "DETERMINISTIC_DEMO", model_calls: 0, external_requests: 0, real_effects: 0,
   proposals: copy(Object.values(proposals)), receipts: copy(Object.values(receipts)), events: copy(events),
   audit_chain_valid: await chainValid(),
   limitations: ["Browser-memory session", "Reviewer role is simulated, not real authentication", "No LLM quality or production readiness claim"] }],
  "GET /api/scenarios": async () => [200, (await data).scenarios],
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
 const files = { "/api/model-catalog": "model-catalog.json", "/api/evidence": "latest.json", "/api/acceptance": "acceptance.csv", "/api/requirements": "requirements.json" };
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
