# Technical sources and selected scope

Consulted 2026-10-03. These references support technical choices; they do not certify this implementation.

- [Python HTTP server documentation](https://docs.python.org/3/library/http.server.html): the standard-library server is a development convenience. Keep it on loopback and serve only named assets.
- [MCP 2025-11-25 tools specification](https://modelcontextprotocol.io/specification/2025-11-25/server/tools): tools have names, input schemas and structured protocol results. This demo exposes only two read-only operations.
- [MCP 2025-11-25 lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle): initialize the version/capabilities and complete initialization before ordinary tool calls.
- [Git hooks documentation](https://git-scm.com/docs/githooks): pre-commit can abort a commit with a nonzero exit; a local hook is not a server-side enforcement boundary.
- [Agent Skills specification](https://agentskills.io/specification): a skill is a directory with a SKILL.md describing when and how to perform a procedure.

The methodology in this sample is an original public explanation of the author's working practice. Private engineering books, course screenshots, client material and internal records are not included.
