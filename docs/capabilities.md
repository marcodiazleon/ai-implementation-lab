# Capability ledger

Current implementation: local synthetic example. Canonical tool details: [tools-and-capabilities.md](tools-and-capabilities.md).

| Capability | Evidence | Limit / next item |
|---|---|---|
| Method structure and traceability | SDD map, structured spec/tasks/cases, evidence/sdd-check.json | Internal structural review; owner acceptance separate |
| Local browser workflow | HTTP tests and browser reports | Broader accessibility and mobile coverage recorded separately |
| Eligibility and scope | Tests and seven fixtures | Deterministic rules, not LLM quality |
| Approval sequencing | Positive/negative state tests | Simulated identity; EXP-M04 |
| Retry protection | Concurrent one-process receipt tests | No restart durability; EXP-M05 |
| Application hooks | Pre-hook failure and event-integrity checks | Unsigned chain; no durable post-hook transaction |
| Git guard | Actual blocked/accepted temporary commits | Limited patterns; bypassable; EXP-M08 |
| Data skill | Manual read plus validator/evaluation | Native assistant discovery unverified |
| Implementation-review skill | Manual read, traceability and diff review | Same implementing assistant, not independent QA |
| MCP | Unit and subprocess wire exchange | Live assistant-client interoperability EXP-M09 |
| Verification tooling | Per-case results, environment and source hashes | Windows local run; cross-platform CI still EXP-M07 |
| Runtime model | None | EXP-A04; model/cost selection pending |
| Deployment | Loopback server and public source repository | No public application server or customer service |
| Expansion | 20 items with requirements, dependencies and acceptance | Planning is not implementation |

See evidence/latest.json for current observed results and tests. Manual acceptance cases remain NO_PROBADO until their evidence is recorded.

## U05 — Menú y conversación

Menú de cuatro vistas y conversación opcional OpenAI API: [uso y límites](OPENAI_API.md). Sin integración del chat con las operaciones de devolución. La cobertura automatizada usa transporte simulado; conexión real pendiente.
