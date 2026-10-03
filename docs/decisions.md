# Decisions and sources

Updated 2026-10-03. Source IDs U01–U03 are defined in the active specification.

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
| D13 | Active spec is S01 0.2 | A later numbered spec may be planning-only | Current method, U03 | Assistant | ACTIVE; S02 remains BACKLOG |
| D14 | Model/provider budget and destination | Local model or approved remote service, compare before enabling | No provider/cost decision supplied | Marco | PENDING for EXP-A04 only |
| D15 | Pilot identity and users | Choose actual roles/resources with the business owner | No live pilot currently in scope | Marco | PENDING for EXP-M04/A10 only |

Engineering choices above are identified separately from user approvals. Silence never changes their authority. Routine reversible work under U01–U03 continues without repeated generic approvals.
