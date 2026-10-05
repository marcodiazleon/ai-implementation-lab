# Capability ledger

Current implementation: local synthetic example. Canonical tool details: [tools-and-capabilities.md](tools-and-capabilities.md).

| Capability | Evidence | Limit / next item |
|---|---|---|
| Method structure and traceability | SDD map, structured spec/tasks/cases, evidence/sdd-check.json, in-app evidence view (R27) | Internal structural review; owner acceptance separate |
| Local browser workflow | HTTP tests and browser reports; explicit reset and per-condition explanation (R28, R29) with UI-harness tests | Broader accessibility and mobile coverage recorded separately |
| Eligibility and scope | Tests and seven fixtures | Deterministic rules, not LLM quality |
| Approval sequencing | Positive/negative state tests | Simulated identity; EXP-M04 |
| Retry protection | Concurrent one-process receipt tests | No restart durability; EXP-M05 |
| Application hooks | Pre-hook failure and event-integrity checks | Unsigned chain; no durable post-hook transaction |
| Git guard | Actual blocked/accepted temporary commits | Limited patterns; bypassable; EXP-M08 |
| Data skill | Manual read plus validator/evaluation | Native assistant discovery unverified |
| Implementation-review skill | Manual read, traceability and diff review | Same implementing assistant, not independent QA |
| MCP | Unit and subprocess wire exchange | Live assistant-client interoperability EXP-M09 |
| Verification tooling | Per-case results, environment and source hashes | Windows local run; cross-platform CI still EXP-M07 |
| Runtime model | Optional OpenAI via operator-selected model | Offline transport validated; paid inference pending |
| Deployment | Loopback server + static public demo on GitHub Pages (browser-side rules) | No server-side public API or customer service; model/MCP features local only |
| Expansion | 20 items with requirements, dependencies and acceptance | Planning is not implementation |

See evidence/latest.json for current observed results and tests. Manual acceptance cases remain NO_PROBADO until their evidence is recorded.

## U05 — Menú y conversación

Menú ampliado y conversación opcional OpenAI API: [uso y límites](OPENAI_API.md). Sin integración del chat con las operaciones de devolución. La cobertura automatizada usa transporte simulado; conexión real pendiente.

## U07 — Agents and remote MCP

Four scoped roles with local templates and optional OpenAI generation; separate history and shared API budget. Context7 remote MCP discovery and both read tools verified live without a key. See [workbench limits](WORKBENCH.md) and [review](../reports/AGENTS_REVIEW_2026-10-03.md). Markdown and JSON downloads verified. Real model inference remains unverified.

## Current interface (U08)
Five sidebar views replace the previous top menu. Demonstration includes the conversation and expandable refund exercise. Agents creates persistent text-only roles; MCPs prepares multiple public configurations and retains Context7's real read client. Connect your AI supports OpenAI and Anthropic. Custom agents have no automatic tool execution or autonomous delegation. See WORKBENCH.md and OPENAI_API.md for current behavior; older workbench reports describe their historical delivery.
