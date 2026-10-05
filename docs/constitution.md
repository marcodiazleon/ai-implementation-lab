# Project constitution

Version 0.2, 2026-10-03. Owner: Marco Díaz de León.
Purpose: a public example of implementation work for clients and recruiters. Current runtime scope: local synthetic after-sales demonstration plus separate opt-in OpenAI text Q&A.

## Authority and data
The owner's requests authorize the sample, its SDD documentation and publication in this repository. U05 additionally authorizes an optional OpenAI API connection using an operator-supplied key and explicit in-app consent. No key is read automatically; no paid inference is run by the developer. Live customer operations and other external communications remain outside scope.
Use original synthetic fixtures. Keep private source, customer records, credentials and local session state outside Git.
The exercise's policy thresholds are engineering examples, not approved commercial rules.

## Engineering rules
1. Select the active specification explicitly from docs/project-status.json.
2. Define the use case, requirement source, task and expected check before the next behavioral change.
3. Maintain requirement/code/test relationships when scope changes; update only affected artifacts.
4. Record observed PASS/FAIL/NO_PROBADO and the tested version. Publication and acceptance have separate records.
5. Use the smallest toolset that serves the use case. Document purpose, alternatives, data destination, cost, permission, test and removal.
6. Preserve offline deterministic execution. A future model proposes through the same controlled interface.
7. Keep real effect authorization in the executor. A role name, prompt or skill is not access control.
8. Assign one writer per shared artifact and state. Independent review must be explicitly identified.
9. Preserve failures, source history and local drafts. Do not rewrite history to imply prior SDD compliance.
10. Use direct descriptive language. State observed behavior and limits without slogans or fabricated business outcomes.
11. Close each change with evidence, known issues, responsible owner and the next task.
12. No automatic scheduled work is created by a maintenance note.

## Proportionality
A small wording fix needs a requirement reference, changed text and appropriate verification, not a new project interview. New identity, storage, provider or external effect requires the corresponding design and checks first.
The existing folder structure is retained through an equivalence map. Product agents, cloud deployment, real payments and multi-PC support remain separate future scopes.

U08 authorizes an additional opt-in Anthropic adapter and repository-local user agent definitions excluded from publication. Creation does not grant execution tools. MCP guides may prepare arbitrary client configurations, but only the existing Context7 adapter executes in this sample.

## U12 scope correction — 2026-10-05
Primary visible product: conversation-only Session, Agents, MCP configuration, method and evidence. The synthetic after-sales example is retained as historical code/CLI evidence, not a current UI. API connection settings belong to Session. Static publication is an interface preview; live text inference uses the existing local backend and explicit operator consent. This supersedes earlier visible-demo scope without granting new cloud infrastructure or arbitrary tool execution.
