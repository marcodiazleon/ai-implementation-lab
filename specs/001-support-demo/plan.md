# S01 implementation and maintenance plan

Version 1.1. Basis: spec.md 1.1. Scope: maintain the existing local example and complete SDD traceability.

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
Server adds three exact GET routes behind the existing trusted() check: /api/evidence (evidence/latest.json), /api/acceptance (acceptance.csv as text/csv) and /api/requirements (rows generated by scripts/sdd_check.requirement_rows, the same regex the validator uses). No parameters or file paths come from the request. build_pages.py writes the same three files to _site/data/ and public-demo.js passes them through unchanged; spec.md is not published. web/evidence.js renders the view with a minimal CSV parser and no library; badge rule: FAIL if any case FAIL, PASS if at least one PASS case has evidence, otherwise PENDIENTE (note 2026-10-12: superseded by R36a/D33, PASS only when every applicable case passed with evidence). The method-view public paragraph gains its English text. Tests cover routes, Host rejection, build output and requirement/CSV ID parity.

## U13 / R31 — Session restoration
Retain the existing cloud transport and agent definitions. Remove the exercise markup and app.js from the browser entry, keeping domain code and tests for historical reproducibility. Move connection markup into connectionDialog; studio routes only the five destinations and resolves the legacy connection hash to that dialog.
The static builder ships the existing reference catalog as model-catalog.json. The shim serves it; cloud.js recognizes the public preview and prevents credentials/provider submission. No static page is described as an inference backend.
Verification: SessionShellTests, existing build/provider/session checks, JS syntax checks, and a real browser pass. Existing evidence/latest.json is historical until regenerated for this source. Revert with an ordinary commit restoring the changed UI/build files; preserve unrelated branch work.

## U17 implementation
Presentation (R34): a compact block inside Session above the welcome heading, static bilingual markup; the README is rewritten in the same order. Tour (R35): a section at the top of How it is built with steps, expected results and controls; `src/lab/cli.py` gains a `tour` command that drives the existing controller in a fresh Lab and returns structured steps; no UI exercise returns. Evidence (R36): web/evidence.js exposes a pure badge function (ported from PR #4 D24 at ea5fe51 and extended with BLOQUEADO) and renders a status block from docs/project-status.json, served at GET /api/status and shipped as _site/data/status.json. Validator (R36c): sdd_check reads docs/id-registry.json and adds version, guide, NO_APLICA and uniqueness checks (version rule ported from PR #4 D26). CI (R39): .github/workflows/verify.yml becomes the only verification definition and is reused by pages.yml; scripts/check_evidence.py compares the committed fingerprint and test statuses. Documentation (R37): README, docs/INDEX.md, capabilities table, startup warning. Navigation and language (R38): labels, skip link, overflow and contrast checks.
Verification: unit and Node checks for every negative above, verify.py and sdd_check.py, a browser pass at 375/390/1360 in both languages, and CI on the candidate SHA. Revert with ordinary commits; PRs #4, #5 and #6 stay untouched.

## U18 implementation
CI (R40): the matrix is split into `verify-ubuntu` (Python 3.11 and 3.13) and `verify-windows` (Python 3.13) with unchanged member names; two gate jobs named `verify (ubuntu-latest)` and `verify (windows-latest)` need both, run with `if: always()` and call scripts/ci_gate.py, a pure function that passes only when every platform result is `success` and prints each one (D37). CLI (R41): ASCII separators and `errors="replace"` on stdout for the tour only. Evidence (R42, D38): scripts/check_evidence.py defines the source and record manifests; verify.py records both after rewriting acceptance.csv and stores a case map; check_committed and compare_statuses use them; `evidence_scope` leaves project-status. Links (R43, D39): build_pages.py and the server add `revision`, `revision_dirty` and `pins` (report path to the commit that added it) to the status data; web/evidence.js resolves every repository link through one function and rewrites anchors marked `data-repo-path`; CI checks out full history for the pins. Language (R44): footer markup carries `data-en`, and the build replaces whole elements. Tour (R45): a worked-result table in the tour and a test that compares it with `tour()`.
Verification: unit negatives for each rule, a subprocess encoding test, the build checks, verify.py, check_evidence before and after, a browser pass ES-EN-ES at 375/390/1360 and CI on the pushed SHA with the required check names. Revert with ordinary commits on this branch.

## U19 implementation
Digest (R46, D40): check_committed validates `source_id` and `record_id` before comparing maps; the file list is added after the unconditional error. Route (R47): a README section and matching INDEX and Spanish guide text with `git fetch`, `git checkout --detach` and `git rev-parse HEAD`, conditioned on the NOT_DEPLOYED record. Selection (R48): the requirement picker writes `#evidence/<ID>` with history.replaceState, so render reads the current choice. Verification: unit negatives, document checks, verify.py, check_evidence before and after, a browser pass and the commands in a fresh clone of the pushed branch.

## U20 implementation
Records (R49, D41): project-status keeps the keys `independent_review`, `acceptance`, `integration` and `deployment` as objects with a `revision`; scripts/revision.py adds `accepted_content`, `integrated` and `published_content` computed with `git rev-parse <sha>^{tree}` and `git merge-base --is-ancestor`; web/evidence-rules.js gains a pure `statusRows` view model tested in Node; web/evidence.js renders it and shows an error with a Retry button when a payload is missing or corrupt; sdd_check validates the recorded revisions. Interface (R50): CSS hit areas of 44 px for the primary controls without changing the identity; the orientation list becomes a disclosure that opens by default on wide screens; the skip link handler focuses the message box after routing; bilingual custom validity messages in i18n.js; English for the MCP guide notices. Matrix (R51, D42): specs/001-support-demo/case-kinds.json classifies every case (behavior, structure, document, manual; positive, negative or limit) and names the code of each requirement; scripts/requirement_matrix.py validates and writes docs/requirements-matrix.md; tests/test_u20.py adds the fail-closed demonstration guarded against recursion. Documentation (R52): README, INDEX and the Spanish guide; docs/visitor-test.md. Measurement (R53): a Playwright script records resource sizes and layout shift; a fresh clone reproduces the evidence.
Verification: unit and Node tests for every rule, verify.py twice with check_evidence between, the browser audit before and after with screenshots at 320/375/390/1360 in both languages, and CI on the pushed revision. Revert with ordinary commits; main and PRs #4–#6 untouched.

## U21 implementation
Secrets (R54, D45): src/lab/sensitive.py holds the named patterns and `find_secrets`; scripts/publication_check.py, src/lab/agents.py, src/lab/agent_store.py and the interface guards use it; (note 2026-10-12: superseded by D53 and the amended R54b, which scan every versioned candidate with Git; the walk below is only the fallback without Git) the worktree scan skips hidden tool directories other than .github, .githooks and .agents, and the staged scan inspects every staged blob. HTTP (R55, D46): src/lab/server.py gets a read timeout, a bounded number of concurrent handlers, a guard against deeply nested JSON and a fixed error envelope for unexpected exceptions; `handle_error` prints no exception text; scripts/build_pages.py injects the CSP meta element. Supply chain (R56, D47–D48): the workflows pin every action by commit SHA with the version in a comment; scripts/security_check.py applies the static rules, the stdlib inventory, the pin check and the secret scan, runs inside scripts/verify.py and in each CI job, and scripts/check_evidence.py rejects evidence without a passing result. Threat model and operation (R57–R58, D49): docs/threat-model.md, specs/001-support-demo/security-controls.json, docs/security-runbook.md, docs/supply-chain.md; tests/test_u21.py holds the positives, negatives and the drill; scripts/sandbox/run_isolated.sh is the validation procedure.
Verification: tests/test_u21.py plus the existing suite, verify.py twice with check_evidence between, the sandboxed run recorded in reports/U21_SECURITY_2026-10-12.md, and CI on the pushed revision. Revert with ordinary commits; PR #8's branch, main and PRs #4–#6 untouched.

