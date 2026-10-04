# Agents and documentation connections

Open **Agents** in the application. The same interface is available in Spanish and English; existing briefs and generated documents retain their original text when the interface language changes.

| Role | Responsibility | Deliverable |
|---|---|---|
| Project Manager | Define scope, dependencies and completion criteria | Milestone proposal |
| Researcher | Organize supplied evidence, distinguish assumptions and gaps | Research brief |
| Implementer | Describe interfaces, proposed files, tests and recovery | Technical proposal in Markdown |
| Quality Reviewer | Compare the brief with previous deliverables and flag missing evidence | Review notes and remaining questions |

## Run a brief

1. Write a public or fictional brief, choose a role and select local template or OpenAI.
2. Local mode returns a deterministic work template. It does not interpret the brief with a language model or perform independent research.
3. For model-generated work, configure your own OpenAI API connection, then authorize each role request. One click makes one request using that model and its output limit. The chat and agents share the 20-attempt connection budget; their context histories are separate. Incomplete or malformed output fails without retrying. Reasoning models may exhaust the configured output budget before producing a usable document.
4. Review the deliverable, then select another role. The latest output from each role for the same exact brief becomes context for the next request. Changing the brief excludes earlier outputs. Context is bounded; shorten or begin a fresh tab if it exceeds the limit.
5. Download individual Markdown documents and the JSON session record before reloading. Results are held in this tab, not persisted to a database. Download behavior can depend on browser settings.

## Hooks and evidence

The Python executor enforces input shape, role allowlist, brief length, context size, matching brief digests, explicit model consent and a structured output schema. It rejects obvious OpenAI key and private-key patterns; this is not a comprehensive data-loss prevention system. An output hash identifies each generated document. These checks establish format and bounded execution, not correctness of model statements. The reviewer cannot certify product tests or approve a release. No role gets shell, file-system or deployment tools.

Role definitions: [roles.json](../agents/roles.json). Executor: [agents.py](../src/lab/agents.py). Tests: [test_agents.py](../tests/test_agents.py).

## Context7

Open **MCP**, authorize connection, then choose a public library name and question. **Find library ID** runs `resolve-library-id`. Copy a returned ID into the field and choose **Retrieve documentation** to run `query-docs`. Each query needs its own consent. The researcher sees the retrieved text only when you select its checkbox in Agents; forwarding it to OpenAI requires the role request consent too.

The adapter uses the fixed destination `https://mcp.context7.com/mcp`, negotiates MCP, sends the initialized notification and discovers both allowed tools. JSON and SSE replies are supported. Arbitrary destinations, shell commands and extra tools are blocked. The optional key and remote session identifier remain in server memory. Local sessions expire after 30 idle minutes and are pruned on the next operation. Disconnect removes the local session; it cannot retract an already sent remote request. There is no remote session DELETE implementation. Tool attempts are capped at 20 per connection, responses at 256 KiB, displayed text at 12,000 characters and socket operations at 25 seconds. Only text content is consumed.

The public no-key connection and both read tools were exercised during this delivery. Future access depends on provider availability and limits. OpenAI model inference has only been exercised with an offline transport in this delivery; no paid inference or private credentials were used.

Provider material and prior artifacts are untrusted reference text. They do not grant tool access. The current output checker validates structure, not the truth of citations or resistance to all prompt injection. Human review remains necessary.

Protocol references: [Context7 official client README](https://github.com/upstash/context7/blob/master/packages/mcp/README.md), [MCP transport](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports), [MCP lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle).

## Next validation

Operator-funded OpenAI inference, long-form output quality, destination-computer startup, broad accessibility and durable session recovery remain separate checks. No changes to private product repositories or existing QA gates are implied by this showcase.
