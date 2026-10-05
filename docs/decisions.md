# Decisions and sources

Updated 2026-10-04. Source IDs U01–U03 are defined in the active specification.

| ID | Decision / question | Alternatives and reason | Source / authority | Owner | State / revisit |
|---|---|---|---|---|---|
| D01 | Fictional shop, 14 days, 100 DEMO | One concrete workflow makes positive and negative cases inspectable; another synthetic domain is possible | Engineering exercise under U01; scenario preference unanswered | Marco for domain changes; assistant for fixtures | IMPLEMENTED_EXERCISE, not commercial-policy approval |
| D02 | Deterministic runtime | Model could add language interpretation, but no current CU requires it | Engineering choice under U01 | Assistant | IMPLEMENTED; compare models in EXP-A04 |
| D03 | Python standard library and loopback | Framework/cloud increase setup; reconsider for authenticated hosting | U01, research and local checks | Assistant | TESTED_LOCALLY |
| D04 | In-memory state | SQLite adds durable recovery; unnecessary for a disposable session, required for persistent workflows | U01 exercise scope | Assistant | IMPLEMENTED_WITH_LIMITS; EXP-M05 |
| D05 | Two read-only MCP tools | HTTP/CLI remains available without MCP | U01 asks to show tool integration | Assistant | WIRE_TESTED; live-client check EXP-M09 |
| D06 | Simulated reviewer role | Real identity belongs to pilot scope | U01 local demonstration | Assistant | IMPLEMENTED_WITH_LIMITS; EXP-M04 |
| D07 | Application hooks and local Git guard | Manual checks alone are less repeatable; local hooks are bypassable | U01 engineering demonstration | Assistant | TESTED_WITH_LIMITS; EXP-M08 |
| D08 | Reuse license not yet selected | Public inspection is available; licensing is an owner decision | No license grant recorded | Marco | PENDING; blocks a reusable licensed package, not this review |
| D09 | Complete SDD against current book | Reconcile existing work rather than regenerate the project | U02/U03 confirmed requests | Assistant | CURRENT_MAINTENANCE_SCOPE |
| D10 | Incorporate all 20 expansion proposals | One canonical backlog with dependencies and closure criteria | U03 confirmed request | Assistant | DOCUMENTED; implementation states are separate |
| D11 | Course layers 00–05 | Chapter 13 and corrected chapter 01 supersede older chapter-10 wording | Current method-source reconciliation | Assistant | RESOLVED_FOR_THIS_PROJECT; original book not edited |
| D12 | Plain descriptive presentation | Replace slogan-like framing with task and result | U02 confirmed correction | Assistant | IMPLEMENTED; owner comprehension untested |
| D13 | Active spec is S01 0.4 | A later numbered spec may be planning-only | Current method, U03 | Assistant | ACTIVE; S02 remains BACKLOG |
| D14 | Model/provider budget and destination | Local model or approved remote service, compare before enabling | No provider/cost decision supplied | Marco | PENDING for EXP-A04 only |
| D15 | Pilot identity and users | Choose actual roles/resources with the business owner | No live pilot currently in scope | Marco | PENDING for EXP-M04/A10 only |
| D19 | Public publication: static GitHub Pages build with rules running in the browser; chat, API-key and MCP views hidden in public; no visitor data | A hosted Python server would need hosting, identity and cost decisions; the browser port reuses the fixtures | Owner request 2026-10-04 | Marco | RESOLVED; parity checked by C113 |
| D20 | PR lock against main: the owner opens pull requests manually; the assistant only pushes branches | Assistant-opened PRs would bypass the owner's review step | Owner 2026-10-04 | Marco | RESOLVED |
| D21 | Evidence view data: requirements exposed as JSON generated from the spec table (same regex as sdd_check.py); latest.json and acceptance.csv served unchanged; spec.md not published in the static build | Publishing spec.md and parsing Markdown in the browser; recalculating states client-side | Owner U10 2026-10-04 | Marco | RESOLVED; C116, C118, C119 |

Engineering choices above are identified separately from user approvals. Silence never changes their authority. Routine reversible work under U01–U03 continues without repeated generic approvals.

## D16 — U04 product and visual direction
2026-10-03. Marco requested a black/white visual redesign and research into a more useful interactive product. Apply the visual change to S01 now; new product functions remain proposals under S02. Compare extending request analysis with a bounded commercial workflow. Reuse generic concepts and original synthetic demonstrations; no private product code, customer data or unverified integration claim is included.

## D17 — U05 optional API and portability
2026-10-03. Add four menu views and an independent OpenAI API conversation using an operator-supplied key and exact model. Reimplement a generic connection form; do not import private product code. Fixed endpoint, explicit consent, bounded sessions and no automatic retries. Keep the deterministic exercise and S02 planner backlog separate. USB/shared-folder transfer uses source comparison and local prerequisites; credentials and destination runtime require local setup.

## D18 — U06 interface language
Use a local dictionary, Spanish default and a single localStorage language preference. Language switching is a view operation, never a model call. Keep user/model text and exported technical codes unchanged.

## D-U07 — Four roles, operator-controlled execution

Source U07 requests both Implementer and Quality Reviewer, alongside PM and Researcher. Deliver all four with local template and optional single-call model execution. Use explicit Context7 read queries instead of model-directed tools. Share API request budget, separate chat history, and preserve brief digests. Review remains a proposal, not test execution. Source contracts and bounded adapters are original showcase code.

## U08 — workspace and adapters
The owner requested a sidebar and conversation-first home, agent creation, multi-MCP guidance and support beyond OpenAI. The implementation keeps two fixed provider adapters and separates configuration generation from executable connections. Custom definitions persist outside tracked sources. Existing U07 executor tests remain, while the public interface uses the new creator. Scope is a local text-only showcase; no private product code or customer data was copied.

## U09 — compact session controls
Replace the U08 oversized chat toolbar with four native keyboard-accessible selector chips inside the composer. Keep provider credentials in the dedicated connection page. Use a versioned public catalog instead of claiming to list account entitlements. Apply effort through native API parameters and reject unverified combinations server-side. Require a separate connection when changing providers. Reset history for model changes; retain it for effort changes. Speed hints are qualitative and do not enable premium latency tiers.

## D24 — Conversation is the primary experience
Source: Marco, 2026-10-05, U12. Replace visible refund panels with the existing chat; five destinations only. API settings open within Session. This supersedes D19's public refund presentation. Existing deterministic examples and their results are retained as history. The static preview cannot claim live cloud chat; provider inference remains on the existing local backend until a hosted backend is separately supplied. D20's manual PR opening remains unchanged.

## D25 — U13 evaluation rights and integrity (2026-10-05)
Marco permits documentation/source review and the download necessary to install Python and run the demo locally. No general reuse, redistribution, source modification or external code contribution is granted. LICENSE.md supersedes D08's pending reuse-license decision with bounded evaluation rights; GitHub platform rights remain.
Use protected main and least-privilege CI/deployment instead of claiming that a notice blocks downloads or malicious input. Administrative controls await GitHub Confirm access and remain BLOCKED; collaborator/Actions settings are NOT VERIFIED. CODEOWNERS is review routing only. The amended Pages workflow must pass its build before a separate deploy job receives Pages/OIDC privileges. This supersedes workflow permission placement, not D20: owner opens PRs and controls integration. No merge/deployment authorized by this record.
