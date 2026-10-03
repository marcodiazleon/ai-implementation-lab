# How I work: from business question to bounded implementation

## My role
I work across business, product, experience and technology. I define the opportunity, make the workflow tangible, clarify constraints and coordinate implementation. I use AI-assisted development as a delivery capability; I do not present this sample as evidence that I personally hand-wrote every line or operated a production system.

For this exercise, the stakeholder wants consistent after-sales handling. The implementation question is: can a proposed action remain understandable and controlled from request through retry?

## My delivery loop
1. **Recover context.** Read the current state and existing evidence before changing anything.
2. **Define an outcome.** Describe the problem, intended user, success signal and excluded work.
3. **Investigate only material uncertainty.** Prefer primary documentation and small experiments.
4. **Make the agreement testable.** Write a small specification and acceptance cases.
5. **Build a vertical slice.** Deliver one complete user journey before multiplying features.
6. **Challenge it.** Include denied actions, stale data, failures and repeated requests.
7. **Deliver evidence and limits.** Separate implementation, tests, review and production approval.
8. **Choose the next increment.** Change the specification when the requirement changes; do not restart the whole process for every fix.

## Capability layers
| Layer | Purpose | Example in this repository |
|---|---|---|
| 00 — Programming foundations | Understand boundaries and contracts | Typed domain object; small controller; explicit request fields |
| 01 — AI | Decide where reasoning adds value | Model integration is deferred; deterministic baseline makes comparisons possible |
| 02 — Execution harness | Control how actions happen | CLI, loopback server, lifecycle hooks, test runner |
| 03 — Skills and tools | Reuse bounded procedures and interfaces | Data-quality skill and read-only MCP tools |
| 04 — Specification-driven delivery | Connect intent to checks | Requirement IDs, acceptance CSV and evidence |
| 05 — Coordination | Separate responsibilities | Planner, reviewer and connector are conceptual roles, not claimed independent agents |
| Across all layers — Judgment | Evaluate value, cost and risk | No real refund, no live model, no invented business results |

## How I organize the work
- **README** is the front door, not a dump of internal notes.
- **docs/** explains durable concepts, decisions and limitations.
- **specs/001-support-demo/** contains the agreement for one bounded slice.
- **src/** contains reusable logic; **web/** presents it.
- **data/** contains only intentionally synthetic fixtures, never credentials or customer exports.
- **tests/** challenges behavior, including failure paths.
- **scripts/** contains runnable repeatable checks.
- **evidence/** holds machine-readable observations; **reports/** interprets them without inflating their scope.
- **.agents/skills/** contains task-specific instructions; **AGENTS.md** points to the shared constraints.
- **.githooks/** contains optional Git checks. Application hooks remain in the application.

## A client engagement would add
Discovery with actual operators, a baseline metric, data classification, identity and permission design, connector ownership, a limited pilot, deployment and recovery plans, training and an acceptance decision by the business owner.

Those activities require client context. The sample supplies no fictional ROI, customer references, compliance badges or claimed production outcomes.
