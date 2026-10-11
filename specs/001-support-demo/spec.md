# S01 — AI conversation workspace and historical engineering sample

Version: 1.1. Status: current specification; U13 supersedes the visible after-sales exercise; U17 adds the presentation, tour and evidence-status increment; U18 corrects it after the second independent review; U19 closes the findings of the review of U18.
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
| U17 | Marco's request relayed by Codex, 2026-10-11: improve the repository as a presentation for clients and recruiters (first minute, three-minute tour, coherent evidence and status, documentation by depth, navigation, mobile and languages), keeping U13 Session and its five destinations; implementation and verification on a working branch only, no merge or deployment |
| U18 | Second independent review of PR #7 at f0f088b by Codex, authorized by Marco, 2026-10-11 (7.5/10, not ready to merge): required check names, CLI encoding, Spanish guide, evidence scope, revision links, footer language and tour close; same branch, no merge, deployment or permission change |
| U19 | Second independent review verdict on PR #7 at 5c4292d by Codex, authorized by Marco, 2026-10-11 (8/10 as a presentation, not ready to merge): a corrupt fingerprint digest passed with correct per-file maps, the candidate had no review route, and changing language reset the selected requirement; same branch and limits |
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

The active build is the S01 version selected in docs/project-status.json. S02 is an expansion backlog; its higher number does not make it active or implemented.

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

## U13 — Conversation-only Session (Marco, 2026-10-05)
Marco explicitly requires Session to be a conversation interface, with provider, its models, effort/speed description, message input and replies. Navigation has exactly five destinations: Session, Agents, MCPs, How it is built, Evidence. API configuration belongs to Session. The after-sales panels, approval controls, receipts and operation log are removed from the visible application. Their controller, CLI and previous results remain historical engineering evidence, not current UI acceptance.

CU17: visitor opens Session → chooses provider/model/effort/agent → prepares a message → opens connection settings. The local backend supports explicit consent and existing provider sessions; the static public preview permits interface exploration and agent authoring, labels its lack of a live inference backend, disables credential entry and never simulates a model reply. MCP configuration is not claimed as an active tool connection.

R31a: When Session opens, show the conversation and its composer controls; show no refund exercise, receipt counter or operation log.
R31b: When the visitor changes provider, show that provider's reference models and compatible effort choices in both the local and static UI; do not imply account access or measured speed.
R31c: When connection settings are requested, open a labeled dialog within Session; preserve the message draft and the five navigation destinations. In the static build, explain the local-backend requirement and block credential submission.
R31d: While evidence from a prior source revision is displayed, identify it as historical; keep current redesign cases untested until their own checks run.

| R31 | Conversation-only Session, five destinations, provider/model controls, in-session API dialog and truthful local/static behavior | U13 | CU17 | Shell/build regression checks; browser navigation and local live API classified separately |

This source supersedes the visible exercise portion of R11/R13/R21/R25 and the static refund presentation decision D19. It preserves R16/R22/R24/R26 provider, role, consent and session boundaries. Cloud hosting, new arbitrary MCP execution and paid inference are not introduced by this UI change.

## U17 — Presentation, guided tour and coherent evidence status
Source: U17 (Marco via Codex, 2026-10-11). Constraint: U13 stays in force. Session remains the entry and a conversation, navigation keeps exactly five destinations, and the refund case is not shown as a visible exercise. The case remains reachable as local CLI and test evidence, as the constitution's U13 correction allows. IDs reserved by open pull requests are listed in docs/id-registry.json and are not reused here.

### CU19 — Understand the work in the first minute and follow a three-minute tour
A visitor opens the public demo. Session shows who Marco is, what he contributes and what is pending, above the composer. The visitor opens the tour in How it is built, follows each step with its expected result, checks the evidence of a requirement and reads how to contact Marco. No account, key or model is needed. A local operator can run the deterministic refund walkthrough with `python run.py tour`.

### CU20 — Review the state of the evidence technically
A reviewer opens Evidence, reads which records exist (automated verification, independent review, owner acceptance, integration, deployment), the run baseline and the source fingerprint, selects a requirement and sees whether its cases are complete, partial, blocked, failed or pending.

- R34a: When Session opens, the first screen shall show Marco's name, his positioning, his individual contribution (problem definition, scope, acceptance criteria, coordination and verification) separated from the AI-assisted code, and a visible link to the three-minute tour, above the composer.
- R34b: The presentation shall state what the public demo does without account, key or model, what requires the local lab, and what is pending.
- R34c: The README shall follow the same order (who, contribution, what it demonstrates, first action) in at most 700 words excluding code blocks and tables, and its main screenshot shall come from the public build of the same revision.
- R35a: How it is built shall open with a three-minute tour whose steps each name the action, the expected result and the control demonstrated, and close with capabilities and contact; every step shall work without account, key or model.
- R35b: When the operator runs `python run.py tour`, the system shall run, in a fresh in-memory lab, analysis of an eligible order, execution without approval, approval, simulated connector failure, retry and repeat, and print the simulated receipt count after each step as 0, 0, 0, 0, 1, 1 with the same receipt on repeat; the proposal shall be described as simulated, never as proposed by AI.
- R35c: Moving between the tour, Evidence and Session shall not clear the Session message draft.
- R36a: The requirement badge shall be FAIL if any applicable case failed; otherwise BLOQUEADO if any is blocked; PASS only when every applicable case passed with evidence; PARCIAL with "n of m" when only some did; PENDIENTE when none did. NO_APLICA cases are excluded and require a stated reason.
- R36b: The Evidence view shall show, from docs/project-status.json, the separate states of automated verification, independent review, owner acceptance, integration and deployment, plus the run baseline commit, whether the tree had uncommitted changes, and the source fingerprint; it shall state that the delivered revision is the commit that contains the evidence file.
- R36c: sdd_check shall reject a NO_APLICA case without reason, a version header that differs from project-status, a guide that cites another S01 version outside the provenance form, a duplicated ID and an ID reserved by another open pull request.
- R37a: The README shall offer three routes (30 seconds, three minutes, technical review) without duplicated links; docs/INDEX.md shall index specification, architecture, decisions, tests and evidence, and list historical reports with date and version without calling them current.
- R37b: docs/capabilities.md shall hold the canonical public/local/pending/limits table, docs/INDEX.md one complete need → requirement → task → code → test → evidence example, and the startup check and README shall warn that scripts/verify.py rewrites the versioned evidence files.
- R38a: Navigation shall keep five destinations with visible text labels; at 375, 390 and 1360 pixels the document shall not scroll horizontally; the skip link shall target an existing landmark; headings shall start with one h1 per view.
- R38b: New human copy shall exist in Spanish and English with technical IDs preserved; contrast ratios of the real color pairs used for text shall be measured and recorded, without a global WCAG claim.
- R39a: One verification workflow shall run scripts/verify.py on Ubuntu with Python 3.11 and 3.13 and on Windows with Python 3.13 for pushes, pull requests and manual runs; the Pages workflow shall reuse it and give Pages permissions only to its deploy job, on main.
- R39b: The committed evidence shall be reproducible: before and after verification, CI shall check that the source fingerprint in evidence/latest.json matches the checked-out sources and that every test status matches the committed one, and fail otherwise. The published site ships the committed evidence (D21).

| R34 | First-minute presentation in Session and README: who, contribution separated from AI-assisted code, demo/local/pending and the first action | U17 | CU19 | HTML/build checks, README length and screenshot source, browser check; human 30-second test |
| R35 | Three-minute tour compatible with U13: in-app steps with expected results and controls, local `run.py tour` for the deterministic case, draft preserved | U17 | CU19 | Tour CLI receipts and blocks, HTML/i18n checks, browser walkthrough |
| R36 | Coherent evidence status: badge semantics with counts, separate verification/review/acceptance/integration/deployment states, baseline and fingerprint, validator negatives | U17 | CU20 | Badge negatives in Node, status route and build data, sdd_check negatives, browser check |
| R37 | Documentation by depth: three routes, index and historical register, canonical table, traceability example and verify rewrite warning | U17 | CU19/CU20 | Document structure and link checks |
| R38 | Five labeled destinations, no horizontal overflow at 375/390/1360, skip link and headings, ES/EN for new copy, measured contrast | U17 | CU19/CU20 | HTML structure tests, browser measurements, contrast script |
| R39 | Single reusable CI and reproducible committed evidence | U17 | CU20 | Workflow structure tests, fingerprint and status drift negatives, CI run on the candidate SHA |

## U18 — Corrections after the second independent review
Source: U18 (Codex review of f0f088b, authorized by Marco, 2026-10-11). Constraint: U13 and U17 stay in force; Session remains a conversation with five destinations, no visible refund exercise and no sixth destination. Branch protection, permissions and deployment are not changed. Use cases CU19 and CU20 apply.

- R40a: The verification workflow shall emit check runs named exactly `verify (ubuntu-latest)` and `verify (windows-latest)`, the names required on main. Each shall depend on every matrix member, run even when a member failed, was skipped or was cancelled, state the result of each platform and succeed only when every member succeeded.
- R41a: When `python run.py tour` writes to a stream encoded as UTF-8 or cp1252, in Spanish or English, it shall exit 0 without a traceback and print the same steps, results, receipt counts and controls; its separators are ASCII and a character the stream cannot encode is replaced, never raised. Domain logic does not change.
- R42a: Committed evidence shall carry two fingerprints over disjoint file sets that never contain a fingerprint: sources (src, tests, scripts, data, web, agents, .github/workflows, run.py) and records (specs, with acceptance.csv read without its run-environment column, docs/project-status.json, docs/id-registry.json).
- R42b: Before verification, CI shall reject sources or records that differ from the committed fingerprints and name the files; after verification, it shall reject test-status drift, state-count drift and any case whose requirement, test, expected result or status changed, even when every count is identical.
- R42c: docs/project-status.json shall not repeat the run baseline or a fingerprint; the Evidence view reads them from evidence/latest.json and states run baseline, fingerprints and how the delivered revision is identified.
- R43a: The public build and the local server shall record the Git revision they were built from. Every evidence, test and document link in the interface shall open its file at that revision, or, for a historical record, at a fixed commit (the SHA in its version field or the commit that added its report). Links to the live main branch are labeled as such.
- R43b: While docs/project-status.json records this branch as not deployed, the README shall say next to its first action that the public URL serves another revision and does not include this delivery.
- R44a: The footer and the public and local notices shall exist in Spanish and English in the source and in the public build, and follow language changes in both directions.
- R44b: docs/START_HERE_ES.md shall describe the current Session, tour, CLI and public/local/pending boundary, and mark the historical review and the former in-app refund steps as historical.
- R45a: The tour shall state that its three minutes exclude installation and close with a worked result that equals the output of `python run.py tour` (results and receipt counts per step), presented as deterministic local output, not as a model reply.

| R40 | Required check names emitted by gate jobs that depend on the full matrix and report each platform | U18 | CU20 | Gate negatives for failure, skipped, cancelled and missing; workflow structure; CI run with the required names on the candidate SHA |
| R41 | Encoding-tolerant CLI tour with identical content in UTF-8 and cp1252 | U18 | CU19 | Subprocess runs with both encodings in both languages |
| R42 | Bounded evidence manifest: source and record fingerprints without cycles, case-level drift, no duplicated status data | U18 | CU20 | Negatives for role, expected result, case-test mapping, status, registry ID and swapped statuses with equal counts |
| R43 | Links pinned to the build revision or a fixed historical commit; live main labeled; README publication warning | U18 | CU19/CU20 | Build revision and pins, link inventory, README warning, link resolution on the pushed SHA |
| R44 | Bilingual footer and notices; current Spanish guide | U18 | CU19 | Build and source markup, browser ES-EN-ES pass, guide content checks |
| R45 | Tour close with a worked result that equals the CLI output; installation outside the three minutes | U18 | CU19 | HTML against tour() in both languages |

## U19 — Findings of the review of U18
Source: U19 (Codex verdict on 5c4292d, authorized by Marco, 2026-10-11). Constraints of U13, U17 and U18 stay in force. Use cases CU19 and CU20 apply.

- R46a: check_committed shall report an error whenever `source_id` or `record_id` in evidence/latest.json is missing, is not a 64-character lowercase hexadecimal digest, or differs from the fingerprint of the checked-out files, whether or not the per-file maps differ; it shall also list the differing files when there are any. Intact evidence passes.
- R47a: While docs/project-status.json records this branch as not deployed, the README, docs/INDEX.md and docs/START_HERE_ES.md shall distinguish the published URL from the candidate under review, and give the commands to fetch the candidate branch, check out the reported commit and compare `git rev-parse HEAD` with the SHA reported in the PR #7 delivery. No SHA is written before its commit exists.
- R48a: When the reviewer selects a requirement in Evidence, the address shall change to `#evidence/<ID>` and the selection shall survive a language change; a requirement linked from the tour stays selected until another one is chosen.

| R46 | Fingerprint digests checked unconditionally, besides the per-file maps | U19 | CU20 | Negatives with correct maps and a corrupt, invalid or missing digest for each fingerprint; intact positive |
| R47 | Published route and candidate route told apart, with fetch, checkout and SHA comparison | U19 | CU19/CU20 | README, INDEX and Spanish guide checks; commands followed in a fresh clone |
| R48 | Selected requirement kept in the address and across language changes | U19 | CU20 | Handler check; browser R03, R11, EN, ES |
