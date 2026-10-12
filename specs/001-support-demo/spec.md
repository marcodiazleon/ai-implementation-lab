# S01 — AI conversation workspace and historical engineering sample

Version: 1.1. Status: current specification; U13 supersedes the visible after-sales exercise; U17 adds the presentation, tour and evidence-status increment; U18 corrects it after the second independent review; U19 closes the findings of the review of U18; U21 adds the security increment (R54–R58) and U22 the engineering book (R59), both on stacked branches under review; U20 raises every area to the owner's 9/10 target after acceptance of fb7ecf6.
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
| U20 | Marco's request relayed by Codex, 2026-10-12, after owner acceptance of fb7ecf6 and merge 166ea91: reach 9/10 in every area (technical, tests, SDD, docs, first minute, visual, tour, accessibility and responsive, honesty, professional value) on a new branch from main with a new draft pull request; same limits as U17–U19; the acceptance of fb7ecf6 is not extended to this increment |
| U22 | Marco via Codex 2026-10-12: architecture diagrams and an engineering book that consolidate the existing records into a reading route for the code of a16a4e6; documentation only, no acceptance, no score change, no publication |
| U21 | Marco's request relayed by Codex, 2026-10-12, after the U20 candidate 86051b5: raise security toward 9/10 in each area on a new branch from that revision with a separate draft pull request (stacked on PR #8); scope is the static demo, the loopback Python server with synthetic data and the optional cloud/MCP adapters with fixed destinations and text-only agents; no merge, deployment, installations, paid API, real credentials, private data or account settings; the preliminary security note of 7/10 came from sources, not from an executed audit; Codex's 175-item checklist (58 direct, 47 adaptable, 16 environment, 54 future) is a classification, not compliance, and stays outside this repository |
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
Scope note 2026-10-12: written for U05; superseded by U13 (five destinations, with the connection inside Session). Kept as history.
Actor: visitor. Trigger: menu selection. Flow: choose demonstration, conversation, API connection or engineering → matching view appears and menu marks it active. Back/forward and direct hashes restore the view. Offline demonstration remains available without a key.

### CU09 — Connect and ask a cloud model
Scope note 2026-10-12: written for U05 with OpenAI only; U08 added Anthropic (api.anthropic.com) with the same rules. Kept as history.
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

| R21 | Five sidebar destinations and a collapsible accessible menu; only ES/EN in the top bar. Demonstration embeds conversation first and optional deterministic exercise (scope note 2026-10-12: the exercise was removed from the interface by U13; see D29, D35). Preserve existing hash aliases and drafts. | U08 | CU08 | Desktop/mobile navigation, collapse, keyboard and chat-in-demo |
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

## U20 — Nine in every area after the accepted delivery
Source: U20 (Marco via Codex, 2026-10-12). Constraints: U13, U17, U18 and U19 stay in force; black identity and typography kept; no new providers, dependencies, permissions, paid inference or private data; PRs #4–#6 untouched; no merge or deployment by the implementer. Use cases CU19 and CU20 apply.

### CU21 — Read what is true about this build
A visitor or reviewer opens Session or Evidence and learns which revision they are looking at, whether its content was verified, reviewed, accepted by the owner, integrated and published, and what is pending, without a statement that another revision's status applies to this one.

- R49a: docs/project-status.json shall record, as separate objects with a 40-character revision each, the independent review, the owner acceptance (bounded to the accepted revision and scope), the integration (main revision and merged revision) and the deployment (published revision, run and URL); no object shall copy a fingerprint or the run baseline.
- R49b: The status payload of the build and the local server shall state, computed from Git, whether this build has the same content as the accepted revision, whether it is contained in the recorded main revision, and whether it has the same content as the published revision; when Git cannot answer, the payload shall say so instead of guessing.
- R49c: The Evidence view shall present the five records with those computed states, naming the accepted or published revision when this build differs; a missing record shall read as not recorded; a corrupt or missing payload shall produce a visible error with a retry control that has an accessible name.
- R49d: sdd_check shall reject a recorded revision that is not 40 lowercase hexadecimal characters or, when Git is available, that is not in the history of the checkout; a missing record object shall be rejected.
- R49e: Before any metric, badge or record is rendered, the Evidence view shall validate the payload shape and result: `tests` with non-negative integer `run`, `failures` and `errors`, boolean `passed` consistent with those counts, `test_results` as an array of unique non-empty test ids with a status inside the runner's enumeration (PASS, FAIL, NO_PROBADO) whose FAIL and NO_PROBADO rows agree with the counts, requirements as an array of rows with an id and text, acceptance rows with the case, requirement, status and test columns, and a status object with records; any violation shall produce the visible bilingual error with the retry control, never a PASS.
- R49f: The computed states shall describe the files the build serves: when tracked files of the checkout are modified or served directories hold untracked files, the content states (review, acceptance, deployment) shall be false with the reason naming the files, while the commit's containment in main is reported separately; two commits with the same tree are the same content by definition (D43).
- R50a: Every primary control (navigation links, menu toggle, brand link, language selector, session selectors, send button, connection and agent buttons, form checkboxes through their label, disclosure summaries) shall have a hit area of at least 44 by 44 CSS pixels at 320, 375, 390, 768 and 1360 pixels in both languages, without overlap or page-level horizontal scroll; links inside prose are exempt.
- R50b: At 375 pixels the presentation block shall end within one viewport of 760 pixels, keeping name, contribution, AI attribution, the tour action and the scope line; the secondary orientation list may collapse behind a disclosure.
- R50c: Keyboard: the skip link shall move focus to the message box; every focusable control shall show a visible focus indicator; Escape shall close the connection dialog and return focus to its opener; the page shall reflow without horizontal scroll at 320 pixels (equivalent to 400 % zoom at 1280); reduced motion shall remove the typing animation and transitions.
- R50d: Language, navigation and dialog use shall preserve the message draft, the selected provider and model, and the selected requirement.
- R50e: Native form validation messages in the connection and agent forms shall follow the page language; every notice of the MCP guide shall exist in both languages.
- R51a: A requirement matrix generated from acceptance.csv and a reviewed classification shall list, for every active requirement, the observable behavior, the code location, at least one positive case, at least one negative or limit case and the exact evidence of this revision; the generator shall fail when a requirement in the public or local offline scope lacks a behavior-level positive or a negative case, when a classified case does not exist, or when a cited code symbol is absent.
- R51b: Cases that only inspect text or markup shall be marked as structural in the classification and shall not count as the behavior-level positive of a requirement.
- R51d: The matrix generator shall reject a requirement whose code list is empty or malformed; shall derive from the tests mapped in acceptance.csv (the test function uses names imported from src or scripts) a floor that forbids classifying such a requirement as document or measurement, and a structure classification for such a case, unless an override with reason, authority and date is recorded; overrides shall be listed in the generated document and in the validator output, never silent (D44).
- R51c: An offline fail-closed demonstration shall inject a domain defect into a temporary copy, run scripts/verify.py there and show exit 1, the failed case recorded, check_evidence rejecting the run and the status drift reported.
- R52a: README, docs/INDEX.md and docs/START_HERE_ES.md shall describe the published route and the candidate route in terms that stay true on main and on a branch, reference project-status for the published revision instead of quoting it, and include a minimal troubleshooting list (Python version, busy port, rewritten evidence, console encoding).
- R52b: Session's scope line shall not name as pending something recorded as done, and shall point to Evidence for the state of each revision.
- R52c: A bilingual script for a visitor test (30 seconds and 3 minutes, questions, answer record and defect log) shall exist; C170 stays pending until a real visitor runs it.
- R53a: Payload size per view and layout shift of the public build shall be measured with the browser's performance entries and recorded without a synthetic score.
- R53c: Every subprocess started by the tests shall read its output with an explicit UTF-8 decoding that replaces undecodable bytes and shall start Python children with UTF-8 mode, so the suite gives the same result under a cp1252 console, under PYTHONUTF8=1 and under a parent started with -X utf8 without environment variables; a missing output shall be reported, not raised.
- R53b: Reproduction from a clean clone of the candidate revision shall pass check_evidence before and after verify.

| R49 | Separate verification, review, acceptance, integration and deployment records, with states computed against this build | U20 | CU21 | Git computations on synthetic repositories, view-model negatives in Node, sdd_check negatives, build payload check |
| R50 | Touch targets, compact first screen, keyboard, reflow, reduced motion, state preservation and bilingual form errors | U20 | CU19 | Browser audit at five widths in both languages, keyboard and dialog checks, i18n structure checks |
| R51 | Semantic requirement matrix with positives, negatives, code and evidence; structural cases marked; offline fail-closed demonstration | U20 | CU20 | Matrix generator positives and negatives; injected-defect run |
| R52 | Documentation true on main and on a branch, troubleshooting, honest scope line, visitor script | U20 | CU19/CU21 | Document checks, browser reading, route walk |
| R53 | Measured payload and layout shift; clean-clone reproduction | U20 | CU20 | Browser performance entries, fresh clone run |

## U21 — Security toward nine in every area
Source: U21 (Marco via Codex, 2026-10-12). Constraints: U13 and U17–U20 stay in force; identity, Session, the five destinations, draft, tour, languages and responsive behavior preserved; no new providers or dependencies; the U20 candidate 86051b5 stays available for the pending human tests; no state or evidence is transferred from other projects. Use cases CU20 and CU21 apply.

### CU22 — Operate the lab inside its security boundaries
A local operator pastes a provider key, converses, creates agents, exports definitions and configurations and stops the server; a reviewer reads which data the lab holds, where it goes, how long it stays and how it is deleted, which requests the server accepts and refuses, which external code the build runs, and which controls are verified, partial, untested or future. Nothing of this authorizes a public deployment of the server.

- R54a: One definition of sensitive patterns (provider keys of OpenAI and Anthropic, GitHub tokens, AWS, Slack and Google key formats, private key blocks, bearer tokens, credential assignments and personal paths) shall be shared by the publication guard, the agent executor, the agent store and the interface guards; its limits (named formats, no entropy analysis, bypassable local hook) shall be documented.
- R54b (amended after the review of 26fb88d): The publication guard shall inspect staged blobs, reject staged symlinks and private files (`.env` variants, `.local`, key and certificate files, SSH key names) and, in worktree mode with Git available, scan every versioned candidate (tracked files and untracked files that are not ignored, hidden directories included), excluding only untracked ignored files such as caches and build output; without Git it shall fall back to a walk that skips hidden tool directories other than `.github`, `.githooks` and `.agents`, and the documentation shall say that this fallback is narrower. A tracked hidden file with a named format shall fail the gate without the hook; a sanitized tree shall pass.
- R54c (amended): Credentials and authorization headers shall never appear in HTTP responses, in the server's standard error output, in exports or in committed artifacts; session tokens are returned by design in the connect responses and accepted in the session fields, and shall appear nowhere else (error responses, state, standard error, artifacts); an unexpected exception shall produce a fixed error code without its message.
- R54d: The interface shall clear the key field before the request is sent, keep no key in browser storage and render model, MCP and error text as text nodes only.
- R54g (after the reviews of 26fb88d and ebd38ed): The interface guards over exports and saved configurations, the agent executor and the agent store shall apply the same named formats as src/lab/sensitive.py (provider prefixes, GitHub, AWS, Slack, Google, private key blocks, bearer tokens, credential assignments with or without digits, quoted with double or single quotes, personal paths) by walking every string value of objects and arrays as raw text in addition to the serialized form, never by evaluating anything, on every export route including the static build that has no backend, and on both transport branches of the MCP configuration guard; a Node check shall run the same dummies through both implementations, and a browser check shall exercise the real export form on the static and the local builds.
- R54e: Disconnecting, expiry and server shutdown shall discard the key and the history of cloud and MCP sessions from the process memory references; the documentation shall state that absolute erasure of process memory and protection against other local processes are not provided.
- R54f: docs/threat-model.md shall carry a data inventory (keys, prompts, history, `.local`, browser profiles, exports, third parties) with flow, retention and deletion per store.
- R55a (amended after the review of 26fb88d): The local server shall bound the number of connections handled at once before a handler thread is created or any byte is read (the excess gets 503 on the socket and is closed), shall bound the inactivity between bytes and the total time allowed to deliver the request line, the headers and the body, enforced inside every read so that a continuous trickle within a single line or within the body cannot hold a handler past the deadline either, shall refuse with fixed codes (408, 503) and serve again once capacity is free; limits per route (method, fields, body size, content type, Host and Origin) stay as recorded.
- R55b: Malformed requests (incomplete or slow body, oversized body, invalid Content-Length, non-object or deeply nested JSON, wrong content type, unknown fields, unknown route, foreign Origin or Host, invalid, expired or revoked session) shall be refused with fixed codes and shall not stop the server.
- R55c: Remote responses (providers and MCP) that are malformed, oversized, of an unexpected status or without text shall be refused with sanitized codes and no retry; destinations stay fixed and no redirect or operator URL is followed.
- R55d: docs/threat-model.md shall carry an endpoint matrix with method, accepted fields, limits, authority (real or simulated) and error codes for every route the server defines; a route missing from the matrix shall fail a test.
- R55e: The public build shall carry a Content-Security-Policy meta element equivalent to the local server policy, and the documentation shall distinguish the headers the local server sends from the ones GitHub Pages delivers; Host and Origin checks shall be described as a same-origin boundary, not as authentication against local processes.
- R56a: Every external GitHub Action shall be pinned to a full commit SHA of its official upstream with the version in a comment, with `persist-credentials: false` on every checkout, minimal permissions and the required check names unchanged; a floating tag shall fail the security check.
- R56b: A runtime and build inventory (Python standard library modules, Node usage, GitHub Actions) shall be computed from the sources: a third-party Python import or a package manifest shall fail the check until recorded as a decision.
- R56c: A standard-library static check shall reject dangerous constructs (`eval`, `exec`, `compile`, `pickle`, `marshal`, `shelve`, `os.system`, `subprocess` with a shell, `subprocess` inside the server package) and any network host outside the fixed destinations; its scope (named rules, not a general SAST) shall be documented.
- R56d: The security check shall run in `scripts/verify.py` and in every CI matrix job; committed evidence without a passing security check shall be rejected by `scripts/check_evidence.py`, and a failing check shall make `verify.py` exit 1; no silent exclusion or filter.
- R56e: Analysis tools not executed in CI (external SAST, dependency audit, secret scanners) shall be recorded as NO_PROBADO with coverage, local evidence when available and a concrete plan; CI results never authorize publication.
- R57a: docs/threat-model.md shall name assets, actors and trust boundaries (browser, local server, runtime, Git and GitHub, Pages, providers, MCP) and the mitigation and limit of each boundary.
- R57b: specs/001-support-demo/security-controls.json shall map each control to code, positive and negative cases, evidence and a state (VERIFICADO, PARCIAL, NO_PROBADO, FUTURO) consistent with the acceptance records; the catalog shall be evaluated separately from Codex's checklist and shall not count future controls as passed.
- R57c: Untrusted content from the operator, the model or MCP shall not widen tools, destinations or permissions and shall not trigger shell or file reads: fake transports shall show the destination, the tool set and the hooks unchanged under injected instructions.
- R57d: Consent, data minimization, budgets and session limits shall be demonstrated with fake transports: no provider call without consent, request bodies with message, context and agent prompt only, counted attempts and capacity.
- R58a: docs/security-runbook.md shall define detection, containment, revocation, recovery and follow-up, a patch policy, a private reporting channel through the existing GitHub profile without inventing addresses, severities with owner and deadlines, and a rollback through ordinary commits.
- R58b: A synthetic incident drill with an identifier shall be documented and its technical steps executed against fakes; it shall not be presented as a real incident.
- R58c: Owner- or provider-dependent controls (MFA, branch protection, private vulnerability reporting, hosting settings) shall stay pending until read-only evidence exists; nothing shall be enabled by the implementer.
- R58d: Logs, evidence and reports shall carry no secrets or personal data; the evidence hash is integrity, not a signature.
- R58e (amended after the reviews of 26fb88d and ebd38ed): The validation of this increment shall run under a documented sandbox whose script confines the filesystem with a minimal root (toolchain read-only; a synthetic /etc built from an allowlist with a stated reason per entry and no link to host-private files; the disposable copy and scratch writable on the size-limited tmpfs only, with no writable host path exposed to the payload and the results copied out by the script after the payload through an allowlist of names; no home, credentials, host temporary directory or original target path visible), isolates the network with loopback only, empties the environment to an allowlist, and applies mandatory, fail-closed process, memory, CPU, file-size and time limits that also cover the copy and the probes (the probes run inside those limits); every probe shall validate its own output format and the memory probe shall require the kill signal of the cgroup, not any failure and the run shall abort before the payload when any control is not demonstrated, including a probe that proves an external dummy path and the original target path are not reachable; when a control cannot be demonstrated the run is recorded as not executed, never as passed, and earlier runs under a weaker runner are kept as reported and superseded.
- R58f (added after the third review of 8a079ea): The sandbox shall keep three trust levels. The process that owns the host export directory and promotes results shall run outside the payload's PID namespace, invisible to it; no process visible in the payload's namespace shall hold a descriptor to a path outside the new root, and the script shall verify this before the payload; the supervisor inside the namespace shall hold no host resource, shall not be dumpable and shall not be readable through /proc or ptrace from the payload; the payload shall run in a nested user and mount namespace so the read-only, nosuid and nodev flags of the toolchain are locked by the kernel against remount, with no_new_privs set, and the script shall verify from an identical nested namespace that the remount, the supervisor's descriptors and the supervisor's memory are refused before the payload. Promotion shall start only after the PID namespace ended and the cgroup holds no process but the runner's own, and shall accept only plain relative names from the allowlist, opened without following links, that are regular files with one link within per-file and cumulative size limits, created exclusively at the destination and rechecked for identity and size after the copy; any anomaly refuses the whole promotion. Negative cases shall cover each refusal with dummy payloads and a positive case shall promote a sanitized result intact; when these conditions cannot be demonstrated the runner aborts before the payload and the run is recorded as not executed.

| R54 | Shared sensitive-pattern definition, publication guard over staged blobs and artifacts, no credentials in responses, logs, storage or exports, session data discarded | U21 | CU22 | Dummy non-functional fixtures assembled at runtime; staged and worktree guard; HTTP and stderr negatives; interface structure; browser check |
| R55 | Read timeout, concurrency cap, fixed error codes, remote response limits, endpoint matrix, CSP in the public build | U21 | CU22 | Isolated server with fake transports; slow, incomplete, oversized and nested bodies; foreign origins; session states; matrix check |
| R56 | Actions pinned by commit SHA, stdlib-only inventory, static rules, security gate in verify and CI, declared analysis coverage | U21 | CU22 | Workflow and inventory checks; negatives on temporary copies; nested fail-closed run; local ruff evidence |
| R57 | Threat model, control catalog with states, untrusted content cannot widen tools or destinations, consent and budgets | U21 | CU22 | Catalog consistency check; fake-transport injections; document checks |
| R58 | Runbook, synthetic drill, pending owner evidence, clean artifacts, sandboxed validation | U21 | CU22 | Document checks; drill against fakes; artifact scan; sandbox report |
| R59 | Engineering book and architecture diagrams that consolidate the records for the code of a16a4e6 with exact references; documentation only, not acceptance | U22 | CU23 | Link, textual-equivalent and SHA checks over docs/book; sdd_check and verify under the isolated runner |

## U22 — Architecture diagrams and the engineering book
Source: U22 (Marco via Codex, 2026-10-12), after the fourth review of a16a4e6 (8.5/10 provisional, no go). Constraints: U13 and U17–U21 stay in force; documentation only on a new branch from a16a4e6, stacked on PR #9; no merge, publication, installation, paid API or new dependency; documentation is not acceptance and raises no score; diagrams represent the delivered code with exact references, never promises; owner evidence, external analysis and human tests stay pending.

Amendment 2026-10-12 (second Codex review of 55197be, 8.5/10 provisional, not ready by B3): mobile-first presentation of every diagram (R59g), no new tools, no network change, C327 kept NO_PROBADO.

Amendment 2026-10-12 (third Codex review of 35a1ef3, not approved by a new P2): the vertical layout of the browser component diagram introduced arrows (studio→workbench, cloud→evidence, workbench→sensitive-rules, evidence→i18n) that correspond to no load, call or dependency in the code; a semantic arrow is never used to order boxes (R59h), and a structural case derives the admissible arrows from the source.
Amendment 2026-10-12 (Codex review of afd6e04, 8/10 provisional, not ready): B1 current guides reconciled with a classification of every discrepancy; B2 guard coverage and the Context7 copy bounded; B3 visual evidence of the render. Authorized as bounded documentary corrections on PR #10.

### CU23 — Understand the whole application from one reading route
A visitor understands the context in one minute; a reviewer locates frontend, backend, adapters, state, evidence and CI in three minutes; a person about to change the code follows the code walk, the method and the validation procedure; the owner reads the decisions with their recorded reasons and the contradictions found between older documents and the code. Errors: a diagram arrow without code behind it, a reason attributed to a person without a record, a second register that contradicts the first.

- R59a: docs/book/ shall hold a navigable engineering book in Spanish with English navigation and summaries: purpose and scope, architecture (context and component diagrams with trust boundaries, in-memory state, local persistence, published data and information flows), code walk with sequence diagrams for the tour and evidence, the local question with optional connection and consent, and agents and MCP (configure versus connect), method and SDD, decisions, validation and operation with limits; one entry page linked from README, docs/INDEX.md and docs/START_HERE_ES.md.
- R59b: Every diagram shall be editable source in the repository (Mermaid inside the Markdown), rendered without a CDN or a new dependency, followed by a textual equivalent that does not depend on color, and every arrow shall represent behavior that exists at the described revision with a file and line reference; Pages never executes Python or inference, configuring an MCP profile never implies a connection, and a role or prompt never grants authority.
- R59c: The decision register of the book shall reuse the existing IDs and, for each decision, give the problem, the decision, the recorded reason, the alternatives, the trade-offs and consequences, the requirement and the code, test or evidence named by the record; where the record is silent it shall say "no registrado", and an inferred explanation shall be marked as such and attributed to nobody.
- R59d: The book shall name its version and the exact SHA it describes, distinguish implemented, optional, simulated and future, distinguish the candidate from the published revision, list the contradictions found between documents and code without correcting history, and state which of its own checks were executed and which are reported.
- R59e (added after the review of afd6e04): Every discrepancy the book lists shall be classified as historical (kept with a dated scope notice), current and correctable (the current guide corrected with a dated amendment, the historical entry kept), a real owner decision (left pending and named) or a technical pending item (recorded as such in the records, never patched silently in a documentation change); current guides shall not keep a false description of the delivered code; the Pages in-tab agent save, which checks two formats while the local store and the export guards use the shared patterns, shall be recorded as a coverage gap pending a code decision, and the interface copy shall describe the Context7 result as read manually, not as forwarded to an agent.
- R59g (added after the second review of 55197be): Every diagram shall be presented for a 390 px viewport without zooming: vertical orientation for flowcharts, short labels in the nodes with the details in the textual equivalent, sequences split into fragments of at most three participants with short messages; a structural case shall check these bounds; the visual reading by a person and C327 stay NO_PROBADO until external evidence exists.
- R59h (added after the third review of 35a1ef3): Every arrow of the browser component diagram shall correspond to a script loaded by web/index.html (or injected by scripts/build_pages.py for the public build) or to a module reading a global that another module defines; vertical order shall be obtained with invisible Mermaid links or separate fragments, never with a semantic arrow; a structural case shall derive the admissible arrows from the source and compare them with the diagram.
- R59f (added after the review of afd6e04): The render of every diagram shall be evidenced with captures taken from GitHub's rendering of the exact SHA at a desktop and a mobile viewport, stored in the repository with the SHA and viewport named, without installing a renderer, a CDN or a dependency; legibility and the one-minute and three-minute human readings stay NO_PROBADO until a person records them.

