# S01 tasks

Version 1.0. Current spec: spec.md 1.0. Existing behavior is retained; this update completes method records and reproducible evidence.
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

| T24 | R15,R13 | Spanish/English UI and saved preference | U06,T21,T22 | Implementing assistant | Four views and dynamic states translate without resetting work; persistence verified | IMPLEMENTED; see language review |

| T25 | R18,R19 | Four role contracts and controlled executor | U07,T24 | Implementing assistant | Local and mock-model outputs plus hook negatives pass | IMPLEMENTED; validation limits in delivery review |
| T26 | R20 | Context7 MCP client and connection view | U07,T24 | Implementing assistant | Initialize/discovery/read tools and invalid/timeout cases verified | IMPLEMENTED; validation limits in delivery review |
| T27 | R18,R19,R20 | Bilingual workbench and evidence downloads | T25,T26 | Implementing assistant | Browser workflow and claims match observed evidence | IMPLEMENTED; validation limits in delivery review |

Task state describes work, not acceptance. Case states in acceptance.csv are authoritative for observed checks. Completed legacy behavior remains unchanged and its history is preserved. New expansion implementation uses S02 tasks after selecting the corresponding item.

| T28 | R21,R15 | Sidebar and conversation-first demo | U08,T27 | Implementing assistant | Bilingual routes, collapsible menu, preserved exercise | IMPLEMENTED; see U08 delivery report |
| T29 | R22,R19 | Persisted agent builder and conversation roles | U08,T25 | Implementing assistant | Create/edit/export/reload and isolated role context | IMPLEMENTED; see U08 delivery report |
| T30 | R24,R16 | Provider-neutral guide and Claude adapter | U08,T22 | Implementing assistant | Fixed provider routing and mock protocol checks | IMPLEMENTED; see U08 delivery report |
| T31 | R23,R20 | Multiple-MCP configuration guide | U08,T26 | Implementing assistant | Export works and configured/executable states are accurate | IMPLEMENTED; see U08 delivery report |

| T32 | R25,R21 | Compact Session and composer controls | U09,T28 | Implementing assistant | ES/EN desktop/mobile, animated prompt and draft checks | IMPLEMENTED; see U09 delivery report |
| T33 | R26,R24 | Model catalog and real effort configuration | U09,T30 | Implementing assistant | Payload, validation, failure and context tests | IMPLEMENTED; see U09 delivery report |
| T34 | R25,R26 | Current screenshots, guide and delivery evidence | T32,T33 | Implementing assistant | Public claims match observed behavior | IMPLEMENTED; see U09 delivery report |

| T35 | R27,R12 | U10 source, R27 EARS, task and case records; read-only evidence/acceptance/requirements data routes and public data files | U10,T15 | Implementing assistant | Spec, routes and build data exist; sdd_check passes with R27 | IMPLEMENTED; see U10 notebook entry |
| T36 | R27,R15 | Bilingual Evidence view: run metrics, requirement picker, case table and PENDIENTE badge | T35,T28 | Implementing assistant | Local and public build show metrics and R02 cases in a browser | IMPLEMENTED; see U10 notebook entry |
| T37 | R27 | Tests and acceptance cases for data routes, public build files and ID parity | T35 | Implementing assistant | C114–C120 mapped and passing in evidence/latest.json | IMPLEMENTED; see U10 notebook entry |

## U12 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T41 | R30,R21,R25 | Conversation-only Session and five destinations | U12,T28,T32 | Codex, directly authorized by Marco | Chat controls remain; exercise/log absent; dialog preserves draft | IMPLEMENTED; verification pending |
| T42 | R30,R16,R26 | Public model catalog and explicit local-only connection boundary | T41,T22,T33 | Codex | Same reference catalog; static credential submission blocked | IMPLEMENTED; verification pending |
| T43 | R30,R12,R14 | Regression checks, evidence classification and README | T41,T42 | Codex | Checks recorded by revision; historical results not reused as redesign acceptance | IMPLEMENTED; local 101 tests and static/local Chromium checks PASS; base CI successful; new increment CI pending |

## U13 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T44 | R11,R12 | Evaluation-only license and consistent visitor/contribution/security documentation | U13,T43 | Codex; authority Marco | Local evaluation allowed; reuse and external code changes reserved; platform limits explicit | IMPLEMENTED; C144 internal policy review recorded |
| T45 | R08,R14 | CODEOWNERS; least-privilege CI and verified Pages build; main protection and settings audit | U13,T44 | Codex for files; Marco for GitHub identity confirmation | Project build cannot use deploy permissions; main controls and limitations evidenced separately | PARTIAL; C145 main/collaborator/Actions/Pages controls verified; account-app audit pending; C146 local checks pass, branch CI pending |

| T46 | R11,R12,R14 | Six app-specific product documents and equivalence review against owner reference templates | U14,T44 | Codex; Marco supplies inaccessible references | Six documents map to canonical app source and SDD; template read and comparison recorded; no unsupported implementation claims | IMPLEMENTED; six references read and six app documents reviewed internally; evidence/product-document-references.json; owner acceptance pending |
