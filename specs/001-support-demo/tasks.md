# S01 tasks

Version 1.1. Current spec: spec.md 1.1. Existing behavior is retained; this update completes method records and reproducible evidence.
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

## U13 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T47 | R31,R21,R25 | Conversation-only Session and five destinations | U13,T28,T32 | Codex, directly authorized by Marco | Chat controls remain; exercise/log absent; dialog preserves draft | IMPLEMENTED; verification pending |
| T48 | R31,R16,R26 | Public model catalog and explicit local-only connection boundary | T47,T22,T33 | Codex | Same reference catalog; static credential submission blocked | IMPLEMENTED; verification pending |
| T49 | R31,R12,R14 | Regression checks, evidence classification and README | T47,T48 | Codex | Checks recorded by revision; historical results not reused as redesign acceptance | IMPLEMENTED; CI/browser pending |

## U17 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T57 | R34,R36,R39 | U17 source, R34–R39, CU19–CU20, ID registry, remap of carried PR #5 IDs, decisions D32–D36 and cases before implementation | U17,T47 | Implementing assistant | sdd_check passes with the registry | IMPLEMENTED |
| T58 | R34,R38 | Session presentation block and README rewrite with a screenshot of this revision's public build | T57 | Implementing assistant | Presentation checks pass; README within 700 words | IMPLEMENTED; C183–C185, C171 |
| T59 | R35 | Tour section in How it is built and `run.py tour` | T57 | Implementing assistant | Tour CLI and HTML checks pass | IMPLEMENTED; C186–C188, C172 |
| T60 | R36 | Badge semantics, status route and view, validator negatives | T57 | Implementing assistant | Node badge and sdd_check negatives pass | IMPLEMENTED; C178–C182, C189–C192, C173 |
| T61 | R39 | Single reusable CI and evidence reproducibility check | T60 | Implementing assistant | Workflow and drift checks pass; CI green on candidate SHA | IMPLEMENTED; C193–C195; CI green on 2be5cee (C175, run 38181150428) |
| T62 | R37 | INDEX, historical register, canonical table, traceability example, verify warning, guide versions | T58–T61 | Implementing assistant | Document checks pass | IMPLEMENTED; C198–C199 |
| T63 | R38,R34,R35,R36 | Browser pass at 375/390/1360 in ES/EN, contrast measurements, screenshots | T58–T62 | Implementing assistant | Measurements recorded; no page overflow | IMPLEMENTED; C174, C196–C197; reports/U17_BROWSER_CHECK_2026-10-11.md |

## U18 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T64 | R40,R41,R42,R43,R44,R45 | U18 source, R40–R45, decisions D37–D39 and cases C200–C214 before implementation | U18,T57 | Implementing assistant | sdd_check passes | IMPLEMENTED |
| T65 | R40 | Gate jobs with the required names and scripts/ci_gate.py | T64 | Implementing assistant | Gate negatives pass; CI shows both required names on the candidate SHA | IMPLEMENTED; C200–C202 |
| T66 | R41,R45 | ASCII tour output, encoding tolerance, worked result in the tour | T64 | Implementing assistant | Subprocess encoding test and worked-result parity pass | IMPLEMENTED; C203, C213 |
| T67 | R42 | Source and record manifests, case-level drift, project-status without fingerprint copy | T64 | Implementing assistant | Manifest negatives pass; check_evidence passes before and after verify | IMPLEMENTED; C204–C207 |
| T68 | R43 | Revision, pins and resolved links in the build, server and view; README warning | T64,T67 | Implementing assistant | Link inventory and README checks pass; links resolve on the pushed SHA | IMPLEMENTED; C208–C209, C214 |
| T69 | R44 | Bilingual footer and notices; current Spanish guide; browser pass ES-EN-ES | T64 | Implementing assistant | Markup and guide checks pass; browser pass recorded | IMPLEMENTED; C210–C212 |

## U19 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T70 | R46 | Unconditional digest check with negatives and positive | U19,T67 | Implementing assistant | Corrupt, invalid and missing digests rejected; intact passes | IMPLEMENTED; C215–C216 |
| T71 | R47 | Candidate review route in README, INDEX and Spanish guide | U19,T68 | Implementing assistant | Document checks pass; commands work in a fresh clone | IMPLEMENTED; C217–C218, C221 |
| T72 | R48 | Requirement selection kept in the address and across languages | U19,T60 | Implementing assistant | Handler check and browser pass | IMPLEMENTED; C219–C220 |

## U20 delivery
| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T73 | R49–R53 | U20 source, CU21, R49–R53, D41–D42 and cases C222–C241 before implementation | U20,T70 | Implementing assistant | sdd_check passes | IMPLEMENTED |
| T74 | R49 | Record objects, Git-computed states, view model, error state, sdd_check revision checks | T73 | Implementing assistant | Node and Python negatives pass; payload consistent with Git | IMPLEMENTED; C222–C227 |
| T75 | R50 | Hit areas, compact first screen, skip link, focus, reflow, motion, state preservation, bilingual validation | T73 | Implementing assistant | Browser audit after shows no primary control under 44 px and no overflow | IMPLEMENTED; C228–C232 |
| T76 | R51 | Case classification, matrix generator and document, fail-closed demonstration | T73 | Implementing assistant | Generator passes on the records and fails on its negatives | IMPLEMENTED; C233–C236 |
| T77 | R52 | README, INDEX, Spanish guide, scope line, visitor script | T74 | Implementing assistant | Document checks pass; routes walked | IMPLEMENTED; C237–C238 |
| T78 | R53 | Payload and layout-shift measurement; clean-clone reproduction | T75 | Implementing assistant | Measurements recorded for the pushed revision | IMPLEMENTED; C239–C240 |
| T79 | R49,R51,R53 | Findings of the independent review of 3f2c7ea: payload validation, dirty-build policy, classification floors and overrides, subprocess encoding, documentation precision | T74–T78 | Implementing assistant | Node, Python and browser negatives pass; suite identical under the three console configurations | IMPLEMENTED; C260–C268 |

## U21 delivery

| ID | Requirement | Deliverable | Dependencies | Responsible | Done when | State |
|---|---|---|---|---|---|---|
| T80 | R54–R58 | U21 source, CU22, R54–R58, D45–D49 and cases C270–C306 before implementation | U21,T79 | Implementing assistant | sdd_check passes | IMPLEMENTED |
| T81 | R54 | Shared sensitive patterns, publication guard over staged blobs, private files and artifacts, fixed error envelope, interface guards, data inventory | T80 | Implementing assistant | Dummy fixtures rejected, sanitized tree passes, no credential in responses, stderr or exports | IMPLEMENTED; C270–C279 |
| T82 | R55 | Read timeout, concurrency cap, nested-JSON guard, remote response negatives, endpoint matrix, CSP in the public build | T80 | Implementing assistant | Isolated server refuses and recovers; matrix covers every route | IMPLEMENTED; C280–C289 |
| T83 | R56 | Actions pinned by SHA, security check (static rules, inventory, pins, secrets) in verify and CI, fail-closed gate, declared coverage | T80 | Implementing assistant | Negatives fail the check; evidence without the check is rejected; CI green on the final revision | IMPLEMENTED; C290–C297 |
| T84 | R57 | Threat model, control catalog with states, untrusted-content and consent demonstrations | T81–T83 | Implementing assistant | Catalog consistent with the records; fake-transport negatives pass | IMPLEMENTED; C298–C301 |
| T85 | R58 | Runbook, synthetic drill, pending owner evidence, artifact scan, sandbox script and report | T84 | Implementing assistant | Drill steps pass against fakes; sandbox controls demonstrated in the report | IMPLEMENTED; C302–C306 |
| T86 | R54,R55,R58 | Findings of the independent review of 26fb88d: filesystem confinement and fail-closed probes of the sandbox, connection cap before the thread with deadlines, interface guards aligned with the shared formats, worktree guard over every versioned candidate, document claims corrected | T81–T85 | Implementing assistant | Negatives fail on the previous behavior and pass on the fix; validation rerun under the corrected runner; earlier runs marked superseded | IMPLEMENTED; C307–C312 |
| T89 | R59 | Architecture diagrams and the engineering book (docs/book/): context, components, three sequences, method, decisions, validation, operation and limits; links from README, INDEX and the Spanish guide; cases for links, textual alternatives and the described SHA. Amended after the review of afd6e04: discrepancies classified and current guides reconciled with dated amendments (R59e), the Pages save guard gap recorded as pending, the Context7 copy corrected, render captures at the exact SHA (R59f); after the second review: every diagram re-laid for a 390 px viewport, vertical, short labels, sequences in fragments of at most three participants (R59g); after the third review: the browser component diagram redrawn with only real loads and global uses, ordered by invisible links (R59h) | T88 | Implementing assistant | Links resolve, every diagram has a textual equivalent, the SHA is named; every listed discrepancy carries a class; captures exist with SHA and viewport; sdd_check and verify pass under the isolated runner; Codex reviews the diagrams against the code | IMPLEMENTED; C322–C329 |
| T90 | R34 | Visible name form of U23 in web/index.html (title, sidebar, h1, footer) and the two assertions of tests/test_u17.py that name it; evidence regenerated by the existing flow | T58 | Implementing assistant | C330 passes; C183 still passes; sdd_check and verify pass under the isolated runner | IMPLEMENTED; C330 |
| T91 | R54 | Pages in-tab agent save uses LabSensitive (R54h) with fail-closed behavior; Node harness loads the shared rules; C331 checks every shared format, the benign case and the missing-rules case; the records that declared the gap are amended with dated notes (SC-02 limit, capabilities, C326, the book) | T90 | Implementing assistant | C331 passes; C326 passes with its test renamed; sdd_check and verify pass under the isolated runner | IMPLEMENTED; C331 |
| T88 | R58 | Third review of 8a079ea (V1): trusted stage outside the PID namespace owns the export, no host descriptor in the namespace, non-dumpable supervisor, nested namespace with locked flags and no_new_privs for the payload, promotion after every process ended with safe opens, limits and rechecks; dummy-payload negatives and a positive | T87 | Implementing assistant | Each dummy payload refused as recorded; the positive promoted intact; suites, browser checks and verify.py rerun under the new runner | IMPLEMENTED; C318–C321 |
| T87 | R54,R55,R58 | Residuals of the second review (ebd38ed): synthetic /etc and no writable host path in the sandbox, memory probe by kill signal, probes inside the limits; deadline enforced inside every read; typed traversal of values in every guard with the real export form checked | T86 | Implementing assistant | Negatives fail on the previous behavior and pass on the fix; validation rerun under the corrected runner | IMPLEMENTED; C313–C317 |


## 2026-10-13 maintenance closure
R14/R49/R52 (existing T17/T73/T77 responsibilities): reconcile current status, integration/deployment records, book index and specification metadata; current identity and ES/EN preserved. Existing behavior tests and evidence check validate the bounded change. No new feature or expansion delivery; PR #4/#5/#6/#11 closed with branches retained. Owner/live/environment/manual cases remain pending.

R49 closeout verification: stale record coverage must be described as coverage of the recorded revision, not a claim that a newly deployed build is globally unpublished or unmerged. Clarify the existing ES/EN status copy and its negative assertions; preserve states, historical records and manual cases.
