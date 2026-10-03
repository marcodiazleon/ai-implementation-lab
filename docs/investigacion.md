# Technical sources and selected scope

Consulted 2026-10-03. These references support technical choices; they do not certify this implementation.

- [Python HTTP server documentation](https://docs.python.org/3/library/http.server.html): the standard-library server is a development convenience. Keep it on loopback and serve only named assets.
- [MCP 2025-11-25 tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools): tools have names, input schemas and structured protocol results. This demo exposes only two read-only operations.
- [MCP 2025-11-25 lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle): initialize the version/capabilities and complete initialization before ordinary tool calls.
- [Git hooks documentation](https://git-scm.com/docs/githooks): pre-commit can abort a commit with a nonzero exit; a local hook is not a server-side enforcement boundary.
- [Agent Skills specification](https://agentskills.io/specification): a skill is a directory with a SKILL.md describing when and how to perform a procedure.

The methodology in this sample is an original public explanation of the author's working practice. Private engineering books, course screenshots, client material and internal records are not included.

## Selection record — 2026-10-03 update

Purpose: satisfy CU01–CU07 with a locally inspectable example. The choice is evaluated against setup effort, transparent rules, data exposure and bounded verification.

| Option | Decision and alternative | Data / permissions / cost | Version and validation |
|---|---|---|---|
| Python standard library | Selected for current local scope; web framework deferred until authentication/hosting needs it | Synthetic files + loopback; no runtime provider billing | Actual local version and license in tools register; unit/HTTP tests |
| Deterministic planner | Selected baseline; one model proposed in EXP-A04 | No model input leaves the machine in current product | Seven fixed scenarios; model quality is not evaluated |
| Memory dictionaries | Selected for disposable sessions; SQLite proposed for durable state | No persistent customer data; restart resets | Local concurrency/retry tested; power loss recovery excluded |
| Original MCP subset | Optional read interface; direct CLI/HTTP remains sufficient for the demo | Local stdin/stdout, two synthetic tools | Pinned 2025-11-25; wire tests; external client remains future |
| Local hooks/checks | Selected; CI is a separate expansion | Staged files and source only; no model calls in hooks | Positive/negative hook tests and structural validator |

License, observed versions, removal and state per tool are in [tools-and-capabilities.md](tools-and-capabilities.md).
Research sources and reasoning for the 20 next items are in [the expansion study](INVESTIGACION_EXPANSION_2026-10-03.md). Their canonical delivery state is now [S02](../specs/002-expansion/spec.md).
Development assistant account cost, future provider prices/retention and native integration compatibility are not independently verified. They remain explicit branch-specific decisions.
