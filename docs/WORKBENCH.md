# Agent builder and MCP connections

U08 · S01 0.7 · R21–R24. This interface replaces the U07 role workbench; its lower-level executor and tests remain available as engineering examples.

## Create an agent
1. Open Agents from the sidebar. Choose Project Manager, Researcher, Implementer or Quality Reviewer as a starting template, or start blank.
2. Give the agent a name, role/assignment, instructions and work mode: plan, research, implementation or review.
3. Save. The server validates the fields and writes the definition atomically to `.local/agents.json`. Reloading retains it. Editing updates the same ID.
4. Choose Chat to use this agent in Demonstration. Connect your AI separately. Changing roles clears prior conversation context, while preserving the draft and request counter.
5. Download the JSON definition to reuse after reviewing its contents. The export describes text-only capabilities and implemented input/scope/output bounds; it does not install executable hooks in another client.

The store accepts up to 50 agents and a 4,000-character prompt. No arbitrary file paths, credentials fields or tools can be added. Obvious key patterns are rejected, but this is not comprehensive secret detection. The `.local` folder is ignored by Git and the staged publication guard rejects it. Exported files are the operator's responsibility. The four modes shape instructions; they do not grant research, code execution, product-testing or release privileges.

## Prepare multiple MCPs
Use the HTTP and stdio cards to prepare public connection settings. Name each profile, specify a URL or vendor-provided command and JSON arguments, then download the combined `mcpServers` JSON. Up to 20 profiles persist in this browser. Embedded URL credentials, query parameters and obvious credential arguments are rejected. No command or arbitrary endpoint is executed by the guide.

Import settings into a compatible client following its documentation. Authentication, OAuth, environment variables and supported transports depend on that client and server. This sample does not claim universal MCP execution. Changing a profile with the same name replaces its configuration.

## Built-in Context7
Open its connection panel, authorize access, then find a library ID and retrieve documentation using the two allowlisted tools. Queries require their own consent. Retrieved text is displayed; it is not forwarded automatically to the model.

The fixed destination is `https://mcp.context7.com/mcp`. The adapter handles initialization, discovery, JSON/SSE and text replies. Keys stay in memory; sessions expire after 30 idle minutes, pruned on the next request. Limits remain 20 tool attempts, 256 KiB response, 12,000 displayed characters and a 25-second socket timeout. Disconnect removes the local session but cannot retract an already sent request; remote DELETE is not implemented.

Context7's no-key initialization and both read tools were verified in U07. U08 preserves that adapter. OpenAI/Anthropic are tested with local doubles; live inference remains unverified. See [delivery report](../reports/STUDIO_REVIEW_2026-10-03.md).

Sources: [Context7](https://github.com/upstash/context7/blob/master/packages/mcp/README.md), [official MCP client guide](https://modelcontextprotocol.io/docs/develop/connect-local-servers).
