# Capability ledger

Current implementation: the S01 version in [project-status.json](project-status.json). Canonical tool details: [tools-and-capabilities.md](tools-and-capabilities.md).

## Public, local, pending and limits (canonical table, U17 R37b)

| Area | Public demo, no account or key | Local lab | Pending | Limit |
|---|---|---|---|---|
| Presentation and tour | Session presentation; three-minute tour in How it is built | Same | Test with a new visitor (C170) | Fictional case only |
| Refund case | Described in the tour; not executed in the interface (U13) | `python run.py tour` and the test suite | Owner decision on a visible route (D35) | Simulated receipts; reviewer without real authentication; memory-only state |
| Session conversation | Model catalog and agent drafts; no replies | Conversation with OpenAI or Anthropic using your own key and consent | A recorded live provider call | Text only; no tools; provider charges apply locally |
| Agents | Drafts kept in the tab | Definitions kept in the ignored `.local` folder | — | No shell, file or deployment access |
| MCP | Configuration export only | Context7 read-only connection | Live assistant-client interoperability | Exported configuration is not a connection |
| Evidence | Committed run, cases and project records | Same, plus `python scripts/verify.py` | Owner acceptance; integration of PRs #4–#6 | Automated checks are not owner acceptance |
| Verification | — | Local run | CI result on the candidate revision | Limited publication guard patterns |

The rows below are the earlier ledger by increment; they keep their own scope.

| Capability | Evidence | Limit / next item |
|---|---|---|
| Method structure and traceability | SDD map, structured spec/tasks/cases, evidence/sdd-check.json, in-app evidence view (R27) | Internal structural review; owner acceptance separate |
| Local browser workflow | HTTP tests and browser reports | Broader accessibility and mobile coverage recorded separately |
| Eligibility and scope | Tests and seven fixtures | Deterministic rules, not LLM quality |
| Approval sequencing | Positive/negative state tests | Simulated identity; EXP-M04 |
| Retry protection | Concurrent one-process receipt tests | No restart durability; EXP-M05 |
| Application hooks | Pre-hook failure and event-integrity checks | Unsigned chain; no durable post-hook transaction |
| Git guard | Actual blocked/accepted temporary commits | Limited patterns; bypassable; EXP-M08 |
| Data skill | Manual read plus validator/evaluation | Native assistant discovery unverified |
| Implementation-review skill | Manual read, traceability and diff review | Same implementing assistant, not independent QA |
| MCP | Unit and subprocess wire exchange | Live assistant-client interoperability EXP-M09 |
| Verification tooling | Per-case results, environment and source hashes; one CI on Linux and Windows with a reproducibility check (D32) | Browser checks in CI and an injected-defect run still EXP-M07 |
| Runtime model | Optional OpenAI via operator-selected model | Offline transport validated; paid inference pending |
| Deployment | Loopback server + static public demo on GitHub Pages (browser-side rules) | No server-side public API or customer service; model/MCP features local only |
| Expansion | 20 items with requirements, dependencies and acceptance | Planning is not implementation |

See evidence/latest.json for current observed results and tests. Manual acceptance cases remain NO_PROBADO until their evidence is recorded.

## U05 — Menú y conversación

Menú ampliado y conversación opcional OpenAI API: [uso y límites](OPENAI_API.md). Sin integración del chat con las operaciones de devolución. La cobertura automatizada usa transporte simulado; conexión real pendiente.

## U07 — Agents and remote MCP

Four scoped roles with local templates and optional OpenAI generation; separate history and shared API budget. Context7 remote MCP discovery and both read tools verified live without a key. See [workbench limits](WORKBENCH.md) and [review](../reports/AGENTS_REVIEW_2026-10-03.md). Markdown and JSON downloads verified. Real model inference remains unverified.

## Interface at U08 (historical)
Five sidebar views replaced the previous top menu. Demonstration then included the conversation and an expandable refund exercise; U13 later removed the exercise from the interface. Agents creates persistent text-only roles; MCPs prepares multiple public configurations and retains Context7's real read client. Connect your AI supports OpenAI and Anthropic. Custom agents have no automatic tool execution or autonomous delegation. See WORKBENCH.md and OPENAI_API.md for current behavior; older workbench reports describe their historical delivery.
