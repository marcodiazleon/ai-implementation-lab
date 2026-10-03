# S01 tasks

Version 0.4. Current spec: spec.md 0.4. Existing behavior is retained; this update completes method records and reproducible evidence.
Source: U01–U05 in the spec. One implementing assistant writes shared artifacts; Marco owns business decisions and final acceptance.

| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T01 | R01,R02 | Synthetic lookup and proposal controller | D01,D02 | Implementing assistant | Positive/negative contract and scenario cases pass | IMPLEMENTED |
| T02 | R03,R04 | Review transitions and stale-data check | T01 | Implementing assistant | Decision/state/digest cases pass | IMPLEMENTED |
| T03 | R05,R06 | Local receipt and retry behavior | T02 | Implementing assistant | Concurrent retry and failed-connector cases pass | IMPLEMENTED |
| T04 | R07 | Application hooks and defensive snapshots | T01 | Implementing assistant | Pre-hook failure and audit/copy cases pass | IMPLEMENTED |
| T05 | R08 | Loopback HTTP adapter | T01–T04 | Implementing assistant | Positive route and input/origin cases pass | IMPLEMENTED |
| T06 | R09 | Read-only MCP subset | T01 | Implementing assistant | Protocol and subprocess cases pass | IMPLEMENTED |
| T07 | R10 | Fixture validator and staged Git guard | T01 | Implementing assistant | Contract/pattern/staged/actual-hook cases pass | IMPLEMENTED |
| T08 | R11,R13 | UI, startup guide and plain copy | T05 | Implementing assistant | Browser observations and working links recorded | IMPLEMENTED |
| T12 | R13 | Editorial correction | U02 | Implementing assistant | Corrected UI/README and browser observation | COMPLETE; c4366a8 |
| T13 | R12 | Method version and equivalence map | U03, source reading | Implementing assistant | Book areas mapped to artifacts or scope exclusions | COMPLETE; current update |
| T14 | R01,R02,R03,R04,R05,R06,R07,R08,R09,R10,R11 | Use cases and requirement sources | T13, D01–D07 | Implementing assistant | Trigger/preconditions/flow/errors/result/source present | COMPLETE; current update |
| T15 | R12,R14 | Traceability and per-case evidence | T14 | Implementing assistant | Cases include expectations, actual run results, version/environment | IMPLEMENTED; verify current evidence |
| T16 | R11 | Owner/visitor comprehension and acceptance | T08,T15 | Marco / designated visitor | C045 observed and acceptance decision recorded | PENDING; no approval invented |
| T17 | R14 | 20-item expansion backlog | U03, research | Implementing assistant | All A01–A10/M01–M10 have requirement, dependency, owner and closure | COMPLETE; current update |
| T18 | R12,R14 | Delivery review and handoff | T13–T15,T17 | Implementing assistant | Structural and technical evidence, diff/privacy review and next task | IMPLEMENTED; see review report |
| T19 | R11,R13 | Black/white personal visual layout | U04,T08 | Implementing assistant | C052/C053 browser observations and unchanged workflow checks | IMPLEMENTED; see visual review |
| T20 | R14 | Product research and two bounded plans | U04,T17 | Implementing assistant | Primary-source findings, reuse limits and first useful increment | COMPLETE; see product plans |
| T21 | R15 | Menu and view routing | U05,T19 | Implementing assistant | Demo/chat/connection/method views work by mouse and keyboard | IMPLEMENTED; local tests passed; live API and destination pending |
| T22 | R16 | Optional API transport, sessions and Q&A | U05,T21 | Implementing assistant | Bounded consent-based flow and negative tests; live test status explicit | IMPLEMENTED; local tests passed; live API and destination pending |
| T23 | R17 | Portable startup and destination check | U05 | Implementing assistant | Relative paths and dependency audit work without modifying destination | IMPLEMENTED; local tests passed; live API and destination pending |

Task state describes work, not acceptance. Case states in acceptance.csv are authoritative for observed checks. Completed legacy behavior remains unchanged and its history is preserved. New expansion implementation uses S02 tasks after selecting the corresponding item.
