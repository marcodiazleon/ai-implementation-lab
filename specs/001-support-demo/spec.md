# S01 — Local after-sales example

Version: 0.10. Status: current specification for the existing demonstration.
Owner: Marco Díaz de León. Engineering: implementing assistant.
This version reconciles the existing example with the engineering method. It does not retrospectively approve the original implementation order.

## Need and sources
A recruiter or prospective client needs to inspect how Marco defines an integration, selects tools, organizes work and verifies a result. The deliverable is a public repository and a local runnable example, using original synthetic material.

| Source | Authority and scope |
|---|---|
| U01 | Owner's initial request: public engineering sample, working example, engineering-book structure, no private client/product material |
| U02 | Owner's editorial correction: concrete natural wording and faithful SDD application |
| U03 | Owner's current request: complete the method, document tool use, incorporate the 20 research proposals and update pending work |
| U04 | Owner's request: investigate useful interactive extensions and reuse opportunities; apply a black background, white text and a more personal visual structure now |
| U05 | Owner requests menu, optional OpenAI API connection/Q&A and source continuity to another PC using USB/shared folder; no private runtime or credentials transfer |
| U06 | Owner requests Spanish/English language selection throughout the current app |
| U07 | Owner requests functional internal PM, researcher, implementer and quality reviewer agents with hooks and responsibilities, plus MCP connection options starting with Context7. Both proposed additional roles confirmed. |
| U10 | Owner's request 2026-10-04: a technical visitor sees, inside the app, the requirement → case → test → evidence chain and the real verification state without reading CSV/JSON by hand; a requirement without a passing case is shown as pending |
| U11 | Owner's decision 2026-10-04: the visitor resets the sample session explicitly, with confirmation and an export option, and changing case never allows acting on the previous proposal (product plan F0 / EXP-M02); the visitor enters amount, days since delivery and status of a fictional order and sees every policy condition evaluated at once with its reason, without creating a proposal or receipt (product plan F1) |
| D01 | Engineering exercise design: fictional shop, delivered order, 14-day window, maximum 100 DEMO units; not a merchant-approved policy |
| D02–D07 | Reversible technical choices in docs/decisions.md; no runtime LLM, real refund or paid connector |

U01–U07 authorize the sample and its maintenance. D01 defines repeatable test fixtures within that sample; it is not evidence of an owner's answer to the earlier scenario-preference question. Changes to actual business rules require their own source.

## Actors, data and permissions
- Visitor: reads public documents and clones the repository.
- Local operator: runs the example and simulates a reviewer decision. No real identity authentication is provided.
- MCP client: may invoke two read-only synthetic tools; cannot approve or execute.
- Maintainer: edits requirements, code and evidence within the owner's task authorization.
- No customer accounts, multi-tenant service or runtime autonomous agent are included.

Allowed data: versioned DEMO order fixtures, fictional policy, proposals and receipts. Runtime state is in memory. Public output includes sanitized technical evidence and documentation. No real personal data or secrets are needed.

## Use cases

### CU01 — Read the method and run the example
Actor: visitor. Trigger: opens README.
Preconditions: Git and a supported Python interpreter for execution; public files need no login.
Flow: read the method map → inspect spec/plan/tasks → clone → run verification → launch loopback server → open browser.
Alternatives: no local Python means documentation remains readable; occupied port means choose another port.
Result: visitor can locate the requirement, its test and its result. Comprehension requires a human check, separate from link validation.

### CU02 — Look up an order
Actor: operator or read-only MCP client. Trigger: lookup with order_id.
Preconditions: loaded synthetic fixtures and active process; MCP initialization completed for that transport.
Flow: validate fields → enforce sample-store scope → return a copy of the order.
Errors: missing/wrong fields block; absent and foreign-workspace IDs both return ORDER_UNAVAILABLE.
Result: no proposal or receipt is created.

### CU03 — Request a refund proposal
Actor: operator. Trigger: refund request for an order.
Preconditions: order belongs to sample-store, delivered, within 14 days, amount at most 100 DEMO and not already compensated in this process.
Flow: validate request → evaluate policy → derive identity from order and policy → create or reuse proposal.
Alternatives: invalid tool, field, window, amount or status blocks; repeated identical request reuses the existing proposal and its status.
Result: eligible first request is PENDING_APPROVAL; caller cannot override the amount.

### CU04 — Approve or reject
Actor: simulated local reviewer. Trigger: decision on proposal_id.
Preconditions: proposal exists and is PENDING_APPROVAL.
Flow: controller checks simulated actor → validates decision → transitions to APPROVED or REJECTED → records outcome.
Errors: wrong actor, unknown proposal, invalid decision or repeated decision blocks.
Result: rejection cannot execute. HTTP supplies a fixed demo role; this demonstrates state sequencing, not authenticated authorization.

### CU05 — Execute and retry
Actor: operator. Trigger: execute approved proposal.
Preconditions: approval exists; order and policy digests still match.
Flow: check approval/current data → simulate connector → store local receipt → record result.
Alternatives: pre-effect simulated failure keeps approval and creates no receipt; retry succeeds. Repeated/concurrent execution returns the same receipt. A changed proposal cannot compensate the same order twice.
Errors: stale data or missing approval blocks. Post-effect external timeout and power-loss recovery are excluded.
Result: one simulated receipt within one process; no real payment or external action.

### CU06 — Inspect or export the session
Actor: operator. Trigger: view log or download JSON.
Preconditions: server running.
Flow: obtain defensive-copy snapshot → display events/receipts → export to a file chosen by the browser.
Alternatives: server unavailable shows an error. Restart clears runtime state.
Result: public-safe synthetic trace; hash consistency does not authenticate its author.

### CU07 — Verify and publish a bounded change
Actor: maintainer. Trigger: authorized change.
Preconditions: active spec selected, working tree inspected, changed requirement/task identified.
Flow: run relevant tests and SDD checks → inspect results/limits → check staged content → commit → publish only under existing publication authority.
Alternatives: test or publication guard fails → correct before publication; unrelated local drafts are preserved.
Result: commit-associated evidence and updated continuity. A commit is not owner acceptance.

### CU08 — Navigate the workspace
Actor: visitor. Trigger: menu selection. Flow: choose demonstration, conversation, API connection or engineering → matching view appears and menu marks it active. Back/forward and direct hashes restore the view. Offline demonstration remains available without a key.

### CU09 — Connect and ask a cloud model
Actor: local operator using their own API key. Trigger: explicit connection consent and submit.
Preconditions: OpenAI key, exact model ID and chosen output limit. Fixed HTTPS destination api.openai.com.
Flow: validate fields → verify model access without generating text → create opaque local session → operator submits question → send bounded conversation to Responses API with store=false, no tools → render plain text and usage.
Alternatives: missing consent, invalid model/key, rate limit, network failure or invalid response shows a sanitized error. No automatic retry or model fallback. One in-flight question per session; 20 requests per connection and 30-minute idle expiry. Clear history is local; disconnect removes local session. Disconnect during an in-flight call discards its result but cannot promise provider cancellation or billing reversal.
Result: user can ask and read answers. Cloud chat cannot operate the demo or read project files. No secrets/transcripts are written by this app to disk or logs.

## Requirements

| ID | Observable requirement | Source / decision status | Use cases | Acceptance |
|---|---|---|---|---|
| R01 | When lookup receives an unknown or foreign ID, return the same unavailable result; otherwise return an in-scope copy. | U01 + D01 exercise design | CU02 | Positive lookup and indistinguishable negative results |
| R02 | When a refund request is eligible, create/reuse its proposal; if fields, tool or eligibility fail, block without receipt. | U01 + D01 exercise design | CU03 | All seven fixtures; invalid fields and duplicate proposal |
| R03 | While approval is absent or rejected, block execution; reject invalid decision transitions. | U01 + D06 demo design | CU04–CU05 | Positive approved flow and negative actor/state cases |
| R04 | If order or policy differs from the approved proposal, block execution. | D01/D04 integrity design | CU05 | Policy and order changes rejected |
| R05 | When identical approved execution is retried in one process, return one receipt; prohibit a second compensation for that order. | D04 bounded retry design | CU05 | Concurrent calls and changed-policy resubmission |
| R06 | If the simulated connector fails before its effect, keep approval and create no receipt; allow a later explicit retry. | D04 exercise design | CU05 | Failure then retry |
| R07 | Record before/after outcomes and detect partial event edits; if the before hook fails, stop the attempted effect. | U01 + D07 hook design | CU03–CU06 | Event checks, defensive copy and pre-hook failure |
| R08 | Serve named routes on loopback; reject foreign Host/Origin, invalid JSON type and oversized bodies. | U01 privacy + D03 design | CU01–CU06 | HTTP positive and negative integration cases |
| R09 | After MCP initialization, expose only the two documented read tools; reject write tools and invalid arguments. | U01 + D05 protocol scope | CU02 | Subprocess wire exchange and protocol negatives |
| R10 | Validate synthetic fixtures and inspect staged bytes for the documented publication patterns. | U01 + D07 controls | CU07 | Invalid data/secret fixtures and actual Git hook |
| R11 | Provide readable purpose, startup steps, folder guide and limitations, with working local links. | U01 confirmed request | CU01 | Structural check plus separate visitor walkthrough |
| R12 | Maintain source → use case → requirement → task → test → evidence links and a method-equivalence map. | U02/U03 confirmed requests | CU01/CU07 | SDD validator and internal document review |
| R13 | Use descriptive copy and factual AI-assistance disclosure; render a black canvas, white text, clear personal identity, readable controls/focus and a responsive request/review/activity layout. | U02/U04 confirmed requests | CU01/CU06 | Editorial and desktop/narrow-width keyboard review |
| R14 | Record active spec, versions, responsibilities, changes, next action and the 20-item expansion backlog at each relevant delivery. | U03 confirmed request | CU07 | Continuity/backlog validation |

| R15 | Menu views, hashes and keyboard controls reach demo, chat, connection and method; original demo needs no key. A Spanish/English selector translates static and dynamic UI, updates document language and remembers only the language preference; switching does not reset the case, chat, draft or connection. | U05/U06 | CU08 | Browser navigation, language persistence and preserved state |
| R16 | Optional OpenAI connection and bounded Q&A require explicit consent, isolate sessions, sanitize errors, support local disconnect/history clearing and never expose keys in outputs. | U05 | CU09 | Transport/session/HTTP negatives and browser checks; live inference separately classified |
| R17 | Provide portable source/startup instructions and a read-only destination check without credentials or implicit installation. | U05 | CU01/CU07 | Portable check and clean-directory verification |

### CU11 — Run a scoped agent workflow
Local operator writes a brief, chooses a role and uses deterministic local mode or explicitly authorizes one OpenAI call. PM structures milestones; researcher separates supplied sources from missing evidence; implementer produces a downloadable implementation proposal; reviewer checks deliverables and unresolved tests. Previous outputs may be included only for the same brief. Each role runs input, permission, output and evidence hooks. Local template output is labeled; no autonomous shell/file changes or paid background run. The operator chooses each next step.

### CU12 — Connect a documentation MCP
Operator approves connection to the fixed Context7 HTTPS endpoint, optionally supplies a key, and checks initialization plus tool discovery. They may explicitly resolve a library or query its docs with a bounded question. Only resolve-library-id and query-docs are callable. Documentation is previewed; forwarding to an agent/OpenAI needs the separate agent consent. Disconnect, timeout, denied access, unsupported protocol and tool errors have explicit states. Untrusted docs cannot grant tools or change permissions.

| R18 | Four visible role contracts produce scoped deliverables in clearly labeled local or optional model mode; runs are explicit and previous artifacts match the brief. | U07 | CU11 | Role outputs; no-effect local mode; stale/invalid input and missing-consent cases |
| R19 | Enforce input/permission/output hooks, retain per-run evidence without secrets, export role artifacts and distinguish review from executed tests. | U07 | CU11 | Hook failure blocks output; evidence/export and bounds verified |
| R20 | Fixed-host Context7 MCP supports initialize, discovery and two read-only tools with explicit consent, bounded expiring sessions and safe error rendering. | U07 | CU12 | Mock protocol and HTTP negatives; live metadata/docs separately reported |

## Attributes and exclusions
- Privacy: demonstration uses fixtures only. Optional cloud chat transmits the bounded conversation and selected role instructions to OpenAI or Anthropic after consent; no automatic file/context upload. No public customer endpoint.
- Security: loopback and state-machine controls are tested. Real identity and durable audit remain expansion work.
- Performance: no service-level latency or throughput promise. Test-run durations are observations, not business thresholds.
- Cost: the demonstration has no model calls. Optional cloud chat uses the operator's API account; output-token/request limits are not a currency budget. Development subscription/usage is separate.
- Portability: Python 3.11+ is the intended range; actual verified environment is recorded per run. Other OS/version combinations are not inferred.
- Accessibility: semantic labels/live status exist; keyboard/mobile observations and broader assessment remain separately classified.
- Recovery: stop/restart resets synthetic session; receipts are not durable. No migrations or production backup are needed for disposable state.
- Cancel: close browser/stop local server; no background worker or paid request continues in the product.
- Excluded: real refunds, customer authentication, distributed transaction guarantees, commercial results and public server deployment. Cloud Q&A is separate from the deterministic demo.

## Acceptance
acceptance.csv contains precondition, action, expected, observed, status, evidence, product version, environment and authority per case. Automated PASS is bounded technical evidence. Owner comprehension and independent review, when requested, require their own observations.

The active build is S01 0.10. S02 is an expansion backlog; its higher number does not make it active or implemented.

### CU10 — Choose interface language
Operator selects Español or English. All five views, accessible names, scenario titles, result messages and connection notices update without reload or API calls. Default Spanish; valid stored preference restored; unavailable storage falls back to in-tab behavior. User/model text and technical evidence codes are preserved.

## U08 — Conversation-first workspace and agent creation

Authority: owner requests a collapsible left sidebar, conversation inside Demonstration as the primary view, an agent builder using the four roles as examples, a multiple-MCP configuration guide, and a provider-neutral connection guide including Claude. This supersedes the separate chat/workbench navigation in U05/U07. The existing deterministic exercise remains available inside Demonstration.

### CU13 — Create and use a scoped agent
Operator names a role, writes its prompt and selects a work mode (plan/research/implementation/review). Save a definition in the repository's ignored local area; edit or export it. The four built-in roles are templates. Select the saved role in the demonstration conversation and explicitly send a message using the configured provider. No creation-time provider/key is needed; no shell/file tools are granted to the agent.

### CU14 — Prepare MCP configurations
Operator selects a remote HTTP or local stdio guide, names a server and specifies its URL or command/argument list. Preview/download a client configuration. Multiple non-secret profiles can be kept in browser storage. These configurations are not connections. Context7 remains the verified built-in execution adapter; arbitrary commands and OAuth are not executed by this sample.

| R21 | Five sidebar destinations and a collapsible accessible menu; only ES/EN in the top bar. Demonstration embeds conversation first and optional deterministic exercise. Preserve existing hash aliases and drafts. | U08 | CU08 | Desktop/mobile navigation, collapse, keyboard and chat-in-demo |
| R22 | Create/edit/export custom roles from templates or blank input; persist bounded definitions in ignored repository-local storage with no provider/key fields, traversal or shell execution. Saved roles can guide the conversation. | U08 | CU13 | Round-trip/restart, malformed inputs, secret patterns and role use |
| R23 | Elegant multiple-MCP guide and valid configuration exports for HTTP/stdio, explicitly distinguishing configured from executable; keep bounded Context7 behavior. | U08 | CU14 | Multiple profiles, invalid config and export; no commands executed |
| R24 | Provider-neutral connection guide and bounded OpenAI/Anthropic sessions using fixed destinations, correct protocol adapters and isolated keys/history. No fallback or paid test without operator key. | U08 | CU09/CU13 | Provider routing, format, errors, context reset and authorization checks |

## U09 — Compact session composer
Source: owner requests Session instead of Demonstration, an animated invitation, no visible message label, and provider/model/effort/agent dropdowns below the message. Use original public UI code; no private Nucleus artifacts. Existing refund exercise and agent creator remain available.

### CU15 — Choose the working model in a session
Choose a provider, then a model from the documented compatible catalog or an exact custom ID. Select only supported effort levels. Connect with explicit API consent. Within the same provider, apply a new model/effort before sending; validate model access and clear history on model changes while preserving the request count. Changing providers closes the old connection and requires that provider's credentials. Failed changes retain the previous configuration and do not retry automatically. Catalog entries are not proof of account access. Speed descriptions are qualitative, not measured latency or paid priority service.

| R25 | Compact bilingual Session view with accessible hidden message label, animated invitation that pauses for typing/hidden page/reduced motion, and selectors below the composer. Preserve drafts and support narrow layouts. | U09 | CU15 | Desktop/mobile space, keyboard controls, reduced motion and draft preservation |
| R26 | Documented provider-specific model catalog and validated effort sent through the correct API field. Transactional same-provider configuration; no cross-provider key reuse, automatic inference or request budget reset. | U09 | CU15 | Wire payloads, unsupported settings, failed changes and isolation |

## U10 — Evidence view and traceability explorer
Source: U10 (owner, 2026-10-04); backlog items EXP-A08 and EXP-M07. Visitor flow extends CU01: open the Evidence view → read the run summary → select a requirement → follow its cases to tests and evidence files. The view reads the committed evidence/latest.json, acceptance.csv and a requirements list generated from this table; the browser recalculates nothing. The public build ships the same three files, not this spec.

- R27a: When the visitor opens the Evidence view, the system shall show generation date, source_id/commit, test counts (run/failures/errors), scenario count and `passed` read from evidence/latest.json, without recalculating anything in the browser.
- R27b: When the visitor selects a requirement R01–R27, the system shall list its acceptance.csv cases with status, test_id and a link to the evidence; if the requirement has no PASS case with evidence, it shall be marked PENDIENTE.
- R27c: While the data has not loaded, the view shall state "sin evidencia cargada" and show no default states.

| R27 | Evidence view shows the committed run summary and a requirement → case → test → evidence explorer; a requirement without a PASS case with evidence is PENDIENTE, never approved by default. | U10 | CU01 | HTTP/build data tests, requirement/CSV ID parity and browser check of the public build |

## U11 — Explicit session reset and per-condition explanation
Source: U11 (owner, 2026-10-04); product plan cuts F0 (EXP-M02) and F1 (docs/PLAN_PRODUCTO_Y_DISENO.md). F1 has no S02 row of its own; it is the first editable-request cut of plan U04 and reuses a minimal part of M10 only in that the rules are read from the same policy file.

R28 extends CU06: the visitor chooses Reset session → a confirmation offers Download and reset, Reset or Cancel → on confirmation proposals, receipts and events of the in-memory session are cleared. Stopping the server is no longer the only way to restart the sample.

### CU16 — Explain a fictional request
Actor: visitor. Trigger: submits amount, days since delivery and status of a fictional order.
Preconditions: none; no order fixture is read or changed.
Flow: validate the three fields → evaluate every policy condition in the fixed order delivered status, time window, amount → show each result with observed value, limit and reason, plus the overall verdict → optionally download the explanation as JSON.
Errors: a non-numeric, negative, boolean or out-of-range value, an unknown status, a missing or extra field returns INVALID_REQUEST and evaluates nothing.
Result: no proposal, receipt or audit event is created. The explanation shows that the requirement, not the code path, determines each outcome.

- R28a: When the visitor confirms the reset, the system shall clear proposals, receipts and events of the session and show "Sin operaciones", receipts 00 and no selected proposal.
- R28b: Before confirming, the system shall offer to export the current evidence; if the visitor cancels, the state shall not change.
- R28c: While a proposal is selected and the visitor changes case, approve, reject and execute shall stay disabled until the new case is analyzed.
- R29a: When the visitor submits a valid amount, days and status, the system shall return the complete list of policy conditions with an individual result (met / not met) and reason, plus an overall verdict, without creating a proposal, receipt or audit event.
- R29b: If a field is invalid (non-numeric, negative, > 100000, boolean, status outside delivered/shipped/returned/cancelled, missing or extra field), the system shall reject with INVALID_REQUEST and evaluate nothing.
- R29c: Acceptance case from the plan: delivered 20 days ago for 180 DEMO returns two simultaneous failures (OUTSIDE_WINDOW and ABOVE_LIMIT); changing to 10 days removes only the time-window failure.

| R28 | Explicit session reset with confirmation and prior export clears proposals, receipts and events; cancel changes nothing; changing case disables actions on the previous proposal. | U11 | CU06/CU03 | Controller, HTTP and browser-port reset tests; UI dialog and case-change checks; browser walkthrough |
| R29 | Per-condition explanation of a fictional request lists every policy condition with result and reason plus an overall verdict, creates no proposal, receipt or event, and rejects invalid input without evaluating. | U11 | CU16 | Plan case 180/20 and 180/10, eligible and not-delivered inputs, invalid inputs, HTTP 200/409, Python/browser parity and browser walkthrough |
