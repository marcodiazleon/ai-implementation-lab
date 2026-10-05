# S01 implementation and maintenance plan

Version 0.11. Basis: spec.md 0.11. Scope: maintain the existing local example and complete SDD traceability.

## Components and contracts
| Component | Files | Contract / requirement |
|---|---|---|
| Entry points | run.py, src/lab/cli.py | serve/demo/evaluate/mcp; R11 |
| Domain | models.py, controller.py | proposal state, eligibility, scope, digests and receipt identity; R01–R06 |
| Application hooks | hooks.py | append before/after and hash consistency; R07 |
| HTTP | server.py | GET state/scenarios/named assets; POST request/decision/execute; R08 |
| MCP | mcp_server.py | pinned 2025-11-25 stdio subset, lookup_demo_order and read_demo_policy; R09 |
| View | web/ | render synthetic workflow and event results; R11/R13 |
| Data | data/ | DEMO orders/policy/scenarios; R02/R10 |
| Verification | tests/, scripts/verify.py, scripts/sdd_check.py | per-case evidence and document relationships; R10/R12/R14 |

Request fields: order_id and intent exactly. Decision fields: proposal_id and decision. Execution fields: proposal_id and optional boolean fail_connector. JSON bodies are limited to 4096 bytes in HTTP. Responses are domain status/receipt or explicit error reason. See architecture.md for state transitions and MCP exclusions.

## Data and failure handling
Single-process RLock serializes domain changes. Runtime dictionaries clear on restart. No schema migration is required.
Known pre-effect failure can retry; external uncertain outcomes are not modeled. Event writes and state writes are not a durable transaction. Do not promote the demo to real effects without EXP-M04/M05.
Records are synthetic; publication excludes credentials and private source. The scanner is limited, bypassable and supplemented by a human diff review.

## Tools and alternatives
Python standard library and Git support a small local example without package installation. Browser is the operator surface. MCP is an optional read interface; HTTP/CLI work without it.
Tool selection, actual versions, data destinations, costs and revocation are in docs/tools-and-capabilities.md. An LLM or extra agent is not required by this exercise.

## Work sequence
1. Read active spec, constitution, decisions and notebook; inspect Git and preserve local drafts.
2. Complete S01 use cases, source mapping and tasks before extending the application.
3. Define acceptance rows before collecting their observed results.
4. Enhance evidence tooling to record individual cases and check links/backlog.
5. Run relevant tests once; repair new failures and rerun affected checks.
6. Review docs, diff, privacy and browser behavior appropriate to changes.
7. Commit/publish the authorized sample update, verify remote SHA, record handoff.

## Responsibilities and concurrency
Marco owns purpose, business decisions and final acceptance. The implementing assistant owns this change and its verification. Internal review is labeled as such. Independent review is not inferred from multiple tools. One writer per shared artifact; no extra runtime agents or recurring automation are introduced.

## Verification and release
Commands: python scripts/sdd_check.py; python scripts/verify.py; python scripts/publication_check.py --staged.
Positive/negative tests target requirements, not screenshots. Evidence includes environment, input revision, per-case results and content hashes. UI checks supplement API tests.
Publish only explicitly staged sample files. No database, provider or model configuration changes. Owner acceptance remains separate from publication.

## Rollback and maintenance
For a bad source change, create a normal corrective/revert commit after inspection; preserve evidence and unrelated work. Stop the local server and start a known committed version in a separate checkout if necessary. Runtime session state is disposable and cannot be restored.
For a new feature, select its expansion task, resolve its listed dependencies, update its spec and acceptance first, then implement. Use docs/operations.md for handoff and support.

## U04 visual increment and product investigation
Before changing the view, extend R13 and cases C052/C053. Change web/index.html and web/style.css: black canvas, white text, personal header, compact introduction and two work panels with activity below. Keep existing IDs and event handlers. Add real anchor links and a keyboard skip link; use a single-column layout on narrow screens. No external fonts, scripts or dependencies.
Review the rendered desktop and narrow layout, focus visibility and existing approval/failure/retry flow using a separate synthetic server. Preserve the user's existing session. Record the specific viewport, result and source hash; no full accessibility certification.
Investigate the expanded product separately. A concept derived from another project is not a verified reusable component; publication contains only original synthetic examples and public research. Record both plans and the relation to existing S02 tasks before implementing a new capability.

## U05 — menu and optional OpenAI Q&A
Use existing HTML/CSS/JS with hash-based view routing. cloud.py owns fixed-host HTTPS transport and isolated expiring in-memory sessions; server.py exposes exact JSON-only /api/cloud/connect, /ask, /clear and /disconnect paths. HTTP requests remain loopback-only with Host/Origin validation. No external SDK/dependency, arbitrary endpoint, auth-token discovery or environment-key loading.
The connection form clears the key field after submitting; an opaque session token stays only in tab memory. The server holds credentials/transcript in memory and expires sessions on access. Cloud status is separate from demo receipts. Render model content with textContent. Tests inject a fake transport; live API use is NOT_TESTED until the operator supplies their own key and explicitly sends a question.
Portable app scripts locate their own root. Destination checks read versions and files only; no installation, credentials, database, account or service changes. Multi-project travel material is private and outside this public repo.

## U06 — interface language
Use a local Spanish/English dictionary and bind initial static text and accessibility attributes before app initialization. Dynamic views rerender from semantic state on language change. Store only the selected language in localStorage with failure handling. Do not translate user input, transcript content, IDs or exported evidence. Verify four views, error/success states, case state, draft and persistence; no model call is needed.

## U07 — agent workbench and documentation MCP
Use original repository-owned role manifests, one stateless agent executor, isolated optional model requests sharing the existing session budget but not chat history, and deterministic local deliverables. Hooks are executable Python checks; role prose is descriptive guidance, not the enforcement boundary. No background loops or arbitrary commands. Browser state keeps artifacts and drafts in memory; explicit downloads save Markdown/JSON.
Context7 uses a minimal fixed-host Streamable HTTP JSON-RPC client: initialization, initialized notification, tools/list, allowlisted tools/call. Support bounded JSON or SSE responses, sanitize provider errors, reject redirects, no arbitrary URL or local MCP process. API keys stay server-side in memory; expiry/disconnect revoke local sessions. No SDK/install or secrets lookup. Data sharing with OpenAI and Context7 are separate explicit actions.
All UI additions ship in Spanish and English. Verify protocol contracts with fake transports and browser workflow with synthetic inputs; a live read-only Context7 check uses public documentation only. OpenAI live inference remains operator-dependent.

## U08 implementation
Retain plain HTML/CSS/JS and domain IDs. Move chat into demo; place the seven-case example in an expandable panel. New sidebar persists its collapsed state only. Rewrite agent UI as a definition editor; local JSON storage uses an RLock and atomic replacement under .local/agents.json, excluded from Git. Chat resolves a saved ID server-side, isolates history when the role changes and exposes no tools. Anthropic uses Messages and model-check endpoints via a second fixed-host adapter; existing OpenAI contract stays backward compatible. MCP guide creates JSON profiles without executing them or storing keys; Context7 remains separate inside a details panel. Tests use temporary stores and provider doubles, not private data or paid inference.

## U09 implementation
Keep the original public shell; add scoped session styling and native keyboard-accessible dropdown chips. A local model catalog contains official IDs, effort support and descriptive tradeoffs. No discovery request occurs until the operator authorizes model access. cloud.py validates effort and applies it to native provider payloads; configure locks the session during access checks and commits only on success. The selected output limit remains explicit. Animation never modifies the user's textarea value or announces each character to assistive technology.

## U10 implementation
Server adds three exact GET routes behind the existing trusted() check: /api/evidence (evidence/latest.json), /api/acceptance (acceptance.csv as text/csv) and /api/requirements (rows generated by scripts/sdd_check.requirement_rows, the same regex the validator uses). No parameters or file paths come from the request. build_pages.py writes the same three files to _site/data/ and public-demo.js passes them through unchanged; spec.md is not published. web/evidence.js renders the view with a minimal CSV parser and no library; badge rule: FAIL if any case FAIL, PASS if at least one PASS case has evidence, otherwise PENDIENTE. The method-view public paragraph gains its English text. Tests cover routes, Host rejection, build output and requirement/CSV ID parity.

## U11 implementation
Controller gains two methods. reset() runs under the existing lock, clears proposals and receipts and replaces the AuditTrail; it returns the snapshot. explain() validates exactly amount, days_since_delivery and status (integers 0..100000, booleans rejected, status in delivered/shipped/returned/cancelled), builds a synthetic CUSTOM order in sample-store and evaluates NOT_DELIVERED, OUTSIDE_WINDOW and ABOVE_LIMIT in the same order as _eligible, with thresholds read from the policy; it reads no fixture and writes no proposal, receipt or event. server.py exposes POST /api/reset (body {}) and /api/explain behind trusted() and the existing body limit; RuleError answers 409 BLOCKED like the other routes. public-demo.js ports both routes; reset empties the existing objects in place. The UI uses a native dialog (Escape cancels), reuses the evidence download and the existing labels for reasons, and shows "Sin operaciones" whenever the log is empty. Tests: controller cases in test_lab.py, routes in test_http.py, Python/browser parity in test_parity.py and a Node DOM-stub harness for app.js in test_app_ui.py.

## U12 implementation
web/evidence.js computes the requirement badge from the committed cases only: FAIL if any case is FAIL; PASS only when every case other than NO_APLICA is PASS with evidence; PARCIAL when only some are; PENDIENTE otherwise. The case line shows how many applicable cases pass. A second Node vm harness in tests/test_app_ui.py runs evidence.js against synthetic cases for each outcome and against the committed acceptance.csv and spec requirements. The explanation status list becomes delivered/in_transit/returned/cancelled in the controller, the browser port, the form and the labels, so every fixture status can be explained. scripts/sdd_check.py compares the version headers of spec.md, plan.md and tasks.md with active_spec_version; other documents link to project-status.json instead of repeating the number. .github/workflows/verify.yml runs scripts/verify.py on ubuntu-latest and windows-latest for push and pull_request with contents: read and a 15-minute limit; pages.yml runs it before build_pages.py. A structural test reads both workflow files. The download walkthrough uses a real Chrome session on the local server and the static build and records file name, size and SHA-256.
