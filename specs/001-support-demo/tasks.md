# S01 tasks

Version 0.11. Current spec: spec.md 0.11. Existing behavior is retained; this update completes method records and reproducible evidence.
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

| T38 | R28,R29 | U11 source, R28/R29 EARS and CU16; Lab.reset() and Lab.explain() in the controller; POST /api/reset and /api/explain behind trusted(); same routes in public-demo.js | U11,T05,T35 | Implementing assistant | Spec, controller, server and browser port exist; sdd_check passes with R28/R29 | IMPLEMENTED; see U11 notebook entry |
| T39 | R28,R29,R15 | Reset button and confirmation dialog with export; disabled actions after case change; bilingual "Analyze your own request" panel with per-condition list, verdict and JSON download | T38,T24 | Implementing assistant | Local and public build show reset and explanation in ES/EN in a browser | IMPLEMENTED; see U11 notebook entry |
| T40 | R28,R29 | Controller, HTTP, parity and UI-harness tests; acceptance cases C121+ | T38,T39 | Implementing assistant | Cases mapped and passing in evidence/latest.json | IMPLEMENTED; see U11 notebook entry |

| T41 | R27 | U12 badge rule in the Evidence view (FAIL, PASS only when every applicable case passes, PARCIAL, PENDIENTE) and the count of passing cases; Node harness tests on synthetic and committed cases | U12,T36 | Implementing assistant | C139 and C140 mapped and passing; no requirement with a NO_PROBADO case shows PASS | IMPLEMENTED; see U12 notebook entry |
| T42 | R29 | One order-status vocabulary: explain accepts delivered/in_transit/returned/cancelled in the controller, browser port, form and labels | U12,T38 | Implementing assistant | C124 and C141 pass; no "shipped" left in src/ or web/ | IMPLEMENTED; see U12 notebook entry |
| T43 | R14,R12 | Version headers of spec, plan and tasks aligned with project-status.json; sdd_check fails on a mismatch; README, D13, sdd-adoption and roadmap link to project-status.json instead of repeating a number | U12 | Implementing assistant | C142 passes; sdd_check passes | IMPLEMENTED; see U12 notebook entry |
| T44 | R30 | .github/workflows/verify.yml (push and pull_request, ubuntu-latest and windows-latest, contents: read, 15-minute limit) and a verify.py step before the Pages build | U12,T15 | Implementing assistant | C143 passes; C144 records a green GitHub Actions run on both systems | IMPLEMENTED; run 37361481399 green on both systems |
| T45 | R28,R29 | Real browser walkthrough of "Descargar y reiniciar" and "Descargar explicación" on the local server and the static build, with file name, size and SHA-256 | U12,T39 | Implementing assistant | C145 and C146 recorded; C147 (published URL) stays NO_PROBADO until the merge | IMPLEMENTED; C145/C146 PASS, C147 NO_PROBADO until merge |
| T46 | R12 | Review brief for the external reviewer versioned in reports/ | U12 | Implementing assistant | reports/BRIEF_REVISION_OPENAI_2026-10-05.md exists in the branch | IMPLEMENTED; see U12 notebook entry |
