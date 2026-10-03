# Capability ledger

| Capability | Present evidence | Boundary |
|---|---|---|
| Business-to-implementation trace | Specification and acceptance CSV | Fictional stakeholder, no real commercial outcome |
| Local browser journey | HTTP integration tests and documented visual walkthrough | No production browser compatibility certification |
| Rules and scope | Workflow tests + seven scenario fixtures | Rule engine, not LLM evaluation |
| Approval sequence | Tests deny premature execution and rejected proposals | Simulated reviewer, not authenticated authorization |
| Retry control | Concurrent callers produce one in-memory receipt | No durable or distributed exactly-once claim |
| Application hooks | Controller tests cover event integrity and pre-hook failure | Hash chain is unsigned and can be recomputed |
| Git publication hook | Staged-byte tests and actual blocked/accepted commits in a temporary repository | Optional, bypassable and limited patterns |
| Data skill | Executable fixture validator + SKILL.md | Automatic discovery by assistant clients not verified |
| MCP | Unit and real subprocess stdio tests | Pinned protocol subset; no live assistant client validation |
| AI integration | Architecture seam and deterministic baseline | Model provider and LLM quality evaluation not implemented |
| Deployment | Local loopback server | No hosted application, customer pilot or security certification |

Consult evidence/latest.json for the latest actual test count, failures and source hashes. It is a generated observation, not an independent audit.
