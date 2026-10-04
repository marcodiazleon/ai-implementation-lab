# Tools and capabilities

Reviewed 2026-10-03. This register describes this repository and the current work session, not other installations.

## Selection by use case
| Capability | Purpose / CU | Version or source | State and evidence | Data, access, cost and removal |
|---|---|---|---|---|
| Python standard library | Domain, HTTP, CLI and verification; CU01–CU07 | Intended 3.11+; local check 3.12.14 | LOCAL_EXECUTION, evidence/latest.json | Synthetic local files and loopback; no product model billing; stop process to disable |
| Git | Track/review/publish sample; CU07 | Local 2.55.0.windows.5 | LOCAL_EXECUTION and publication records | Only explicitly staged sample files uploaded; credentials handled outside repo; remove remote configuration to stop publishing |
| Browser | Operator view and UI review; CU01/CU03–CU06 | Current in-app browser; exact engine version not recorded | Observed walkthrough; reports/VALIDATION.md | Loopback synthetic pages; no personal browser data needed; close tab/server |
| HTTP adapter | GUI-to-controller interface | Repository source/version hashes | Positive/negative integration tests | 127.0.0.1 only, no real authentication; stop server |
| MCP adapter | Two read queries; CU02 | Protocol 2025-11-25, server 0.1.0 | Unit + subprocess wire tests | Local stdin/stdout, synthetic data, no remote authentication or credential; stop process/disconnect client |
| Data-quality skill | Validate fixture contracts; CU07 | Repository SKILL.md | Manually read and procedure executed in this update; automatic discovery not established | Local validator and scenario evaluator; no external data |
| Implementation-review skill | Trace changed requirements to evidence; CU07 | Repository SKILL.md | Manually read and applied in this update; not an independent reviewer | Read spec/code/evidence; no extra permissions |
| Application hooks | Record before/after; CU03–CU06 | src/lab/hooks.py | Positive path, tamper detection and pre-hook failure tests | In-memory synchronous events; no model call; no independent timeout; post-effect failure is a documented limitation |
| Git pre-commit hook | Inspect staged bytes; CU07 | .githooks/pre-commit | Blocked/accepted commits tested in temporary repo; local core.hooksPath configured | Local staged files; Python process has no hook-specific timeout; bypassable; unset repo-local core.hooksPath to disable |
| SDD validator | Check references, mapping and backlog; CU07 | scripts/sdd_check.py | evidence/sdd-check.json | Local documents only; no external connection |
| Development assistant | Requirements, implementation and review work | Current configured session; product does not inherit its model | Manual project-rule reads and tool outputs; model identifier/usage not independently measured | File/shell/browser permissions governed by executor; CWD alone grants no access; account cost not quantified |
| Notion connector | Read owner's engineering method for adoption | Current index and relevant chapters, read 2026-10-03 | Source consultation recorded in adoption map | Read-only; private source text and IDs excluded from this repository |
| GitHub CLI | Publish authorized sample | Available current installation; exact version not recorded in this register | Publication records / matching remote commit | GitHub destination and staged public artifacts only; no new account scopes requested |

Manual skill use is a supported fallback. It is not claimed as native discovery. CLAUDE.md is a portable adapter file; this task did not start a Claude session or test its import. No runner-level AI hooks are claimed.

## Commands by task
| Task | Invocation | Expected output |
|---|---|---|
| Recover context | Read project-status → constitution → active spec/plan/tasks → notebook; inspect git status | Known scope, preserved changes, next task |
| Validate fixtures | python scripts/validate_data.py | Contract result |
| Evaluate scenarios | python run.py evaluate | Seven expected/observed statuses |
| Verify SDD | python scripts/sdd_check.py | Mapping and link findings |
| Verify code and evidence | python scripts/verify.py | Individual tests, environment, acceptance updates and source hashes |
| Inspect publication | python scripts/publication_check.py --staged | Limited staged-pattern findings |
| Run interface | python run.py serve --port 8765 | Loopback URL; Ctrl+C stops |
| Run MCP | python run.py mcp | JSON-RPC on stdin/stdout; not a chat console |
| Review a change | Follow .agents/skills/implementation-review/SKILL.md manually if not discovered | Requirement, observation, evidence and unresolved limits |

Commands were used in this project; alternate Python launcher names may differ. The environment record identifies what was actually tested.

## Future model and connectors
EXP-A04 requires a provider/model decision, input classification, endpoint, retention assessment, permission scope and cost ceiling before any paid/external call. Compare a single model with the deterministic baseline; do not select multiple agents by default.
EXP-A06 requires an allowlisted public/sandbox endpoint. EXP-M09 adds live-client interoperability. Cancellation, revocation, errors and rate limits are acceptance conditions, not implied by MCP.

## Licenses and alternatives
Python: PSF License v2 with incorporated components' notices; Python is not bundled by this repository. [Official license](https://docs.python.org/3/license.html).
Git: external versioning tool; review its distributed license when packaging. No Git distribution is included.
MCP: original subset implementation here, not a vendored SDK. No third-party Python package dependency.
Browser, assistant, Notion and GitHub remain external services/tools under their applicable account terms; account billing is not audited here.
The repository's reuse license remains an owner decision (D08). No dependency-license choice grants a license to this sample.

Alternative stack: a web framework could help future authentication/deployment, but adds packages and operations to the local CU. [Python HTTP documentation](https://docs.python.org/3/library/http.server.html) describes the development-server limitations. A future model or database is selected against its use case rather than added to fill a catalog.

## Product agent contract
Current product: no autonomous reasoning agent. The planner is a deterministic controller function.
Future EXP-A04 contract: human-triggered request → schema-validated proposal; data from approved synthetic context; no direct execution tool; explicit budget/timeout/cancellation; stop on invalid output, budget exhaustion or revoked access. Model and thresholds are unresolved branch-specific decisions, not blockers for the existing demo.

## U05 — OpenAI API

Adaptador opcional HTTPS a api.openai.com con Responses; sin SDK adicional, clave de sesión y modelo elegido por el operador. Referencia: [alcance y pruebas](OPENAI_API.md). El doble de pruebas no es una respuesta real del proveedor.

## U07 tool additions

| Tool | Purpose | Access | Verification |
|---|---|---|---|
| Four role executor | Generate plans and review proposals | Supplied brief and artifacts; no shell/files | Local and mock-provider tests plus browser workflow |
| Context7 remote MCP | Read library documentation | Fixed remote URL, optional memory-only key, two tools | Live discovery and both queries; offline negative tests |

[Contracts, limits and protocol references](WORKBENCH.md). Each external operation requires UI consent. No automatic provider fallback.

## U08 implemented scope
Agent builder: local validated JSON definitions, four starting templates, text-only chat and JSON export. HTTP/stdio MCP builder: configuration only, compatible-client guide, no process or arbitrary endpoint launch. Context7: existing allowlisted read client. OpenAI and Anthropic: fixed native API destinations, own credentials, explicit connection consent, one request per send, no fallback or retries. Model quality and real provider inference are NOT_EXECUTED.

## U09 model controls
Official OpenAI/Anthropic documentation supports the local reference catalog and effort mapping. Model selection checks access with the existing fixed-host transport; it is not live catalog discovery. No credentials are discovered from the machine. Seven added tests cover API payloads, unsupported effort, transactional changes, busy/disconnect behavior and catalog isolation. Browser tests use local provider doubles.
