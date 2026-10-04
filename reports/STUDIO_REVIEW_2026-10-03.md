# U08 delivery review

S01 0.7 · source U08 · requirements R21–R24 · tasks T28–T31.

## Delivered
- Expandable sidebar, five views and language-only header.
- Conversation-first Demonstration with the refund exercise in a disclosure panel.
- Four agent templates, validated persistent custom definitions, editing and JSON export; selection in chat.
- Fixed OpenAI and Claude/Anthropic adapters with provider-aware consent and guide.
- Multiple HTTP/stdio MCP configuration profiles, browser persistence and JSON export; existing Context7 read client retained.

## Observed browser checks
Windows Codex browser, local test server with injected provider doubles and an isolated test-agent store. No real keys or paid inference used.

- C091: sidebar navigation, collapse/expand and Spanish/English rendering observed. Conversation is first; refund example remains below it.
- C092: created a fictional review agent, saved, reloaded and reopened its fields; selected it in chat and observed the mock provider receive its role. Downloaded definition was parsed. Changing agent cleared visible messages and completed the local clear request.
- C093: prepared HTTP and stdio profiles and downloaded a JSON containing both. A credential-bearing URL was rejected without changing the two saved entries. Profiles survived reload. Configuration labels explicitly state not connected.
- C094: provider selection changed destination and consent wording; both OpenAI and Claude mock sessions connected and returned text. Access check, costs, model ID and session limits are explained in the UI.

Automated validation: 83 tests and seven synthetic scenarios passed before the final documentation pass; evidence/latest.json is authoritative for the final run. JavaScript syntax checks cover the changed browser modules. The existing Context7 adapter was not changed or re-exercised against the live service in U08; U07 contains the earlier live no-key evidence.

## Limits and handoff
Real OpenAI/Claude inference, response quality, arbitrary MCP execution, destination-computer startup, broad accessibility and independent review remain unverified. Owner acceptance is not inferred from these checks. Custom roles are text-only; their prompts cannot grant filesystem or shell access. MCP profiles are exported configuration, not live connections. Localhost requires a running server and is not a publicly hosted application.

No private product source, customer data, secrets or existing QA state was incorporated. Custom definitions are ignored by Git and rejected by the staged publication guard. Exported definitions require operator review before sharing.

Final run: 83/83 tests and 7/7 scenarios PASS. An earlier final run encountered Windows socket error 10053 in the external-origin negative case; the unchanged repeat passed. The interruption is recorded rather than hidden. A 390 x 844 viewport also showed usable collapsed navigation; Enter expanded the menu and the Agents route opened. Temporary viewport override was reset.
