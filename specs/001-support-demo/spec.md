# S01 — Local after-sales example

Version: 0.2. Status: current specification for the existing demonstration.
Owner: Marco Díaz de León. Engineering: implementing assistant.
This version reconciles the existing example with the engineering method. It does not retrospectively approve the original implementation order.

## Need and sources
A recruiter or prospective client needs to inspect how Marco defines an integration, selects tools, organizes work and verifies a result. The deliverable is a public repository and a local runnable example, using original synthetic material.

| Source | Authority and scope |
|---|---|
| U01 | Owner's initial request: public engineering sample, working example, engineering-book structure, no private client/product material |
| U02 | Owner's editorial correction: concrete natural wording and faithful SDD application |
| U03 | Owner's current request: complete the method, document tool use, incorporate the 20 research proposals and update pending work |
| D01 | Engineering exercise design: fictional shop, delivered order, 14-day window, maximum 100 DEMO units; not a merchant-approved policy |
| D02–D07 | Reversible technical choices in docs/decisions.md; no runtime LLM, real refund or paid connector |

U01–U03 authorize the sample and its maintenance. D01 defines repeatable test fixtures within that sample; it is not evidence of an owner's answer to the earlier scenario-preference question. Changes to actual business rules require their own source.

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
| R13 | Use concrete descriptive copy, retain factual AI-assistance disclosure and remove rejected slogans from current presentation. | U02 confirmed request | CU01/CU06 | Editorial/browser review |
| R14 | Record active spec, versions, responsibilities, changes, next action and the 20-item expansion backlog at each relevant delivery. | U03 confirmed request | CU07 | Continuity/backlog validation |

## Attributes and exclusions
- Privacy: fixtures only; no external runtime network requests. No public customer endpoint.
- Security: loopback and state-machine controls are tested. Real identity and durable audit remain expansion work.
- Performance: no service-level latency or throughput promise. Test-run durations are observations, not business thresholds.
- Cost: no model calls in the product; local computing still consumes resources. Development subscription/usage is not measured here.
- Portability: Python 3.11+ is the intended range; actual verified environment is recorded per run. Other OS/version combinations are not inferred.
- Accessibility: semantic labels/live status exist; keyboard/mobile observations and broader assessment remain separately classified.
- Recovery: stop/restart resets synthetic session; receipts are not durable. No migrations or production backup are needed for disposable state.
- Cancel: close browser/stop local server; no background worker or paid request continues in the product.
- Excluded: live model, real refunds, authentication, distributed transaction guarantees, commercial results and public server deployment.

## Acceptance
acceptance.csv contains precondition, action, expected, observed, status, evidence, product version, environment and authority per case. Automated PASS is bounded technical evidence. Owner comprehension and independent review, when requested, require their own observations.

The active build is S01 0.2. S02 is an expansion backlog; its higher number does not make it active or implemented.
