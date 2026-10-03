# S01 implementation and maintenance plan

Version 0.4. Basis: spec.md 0.4. Scope: maintain the existing local example and complete SDD traceability.

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
