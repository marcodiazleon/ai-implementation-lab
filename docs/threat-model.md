# Threat model and control catalog · Modelo de amenazas y catálogo de controles

U21 · introduced in S01 1.1 · R54–R58, D45–D49. This is the implementer's reading of the lab's boundaries, reviewed independently by Codex; it is not an external audit, a certification or a compliance statement. Codex's 175-item checklist stays outside this repository; the `checklist` references in [security-controls.json](../specs/001-support-demo/security-controls.json) are item numbers only. States are derived from the acceptance records by `python scripts/security_catalog.py`, never typed into this page: a test fails when this table and the records disagree.

Scope: the static demo on GitHub Pages, the Python server that listens on loopback only, synthetic data, and the optional cloud (OpenAI, Anthropic) and MCP (Context7) adapters with fixed destinations and text-only agents. The server is not a product, has no users and must not be exposed to a network.

## Assets · Activos

| Asset | Where it lives | Value to an attacker |
|---|---|---|
| Operator's provider key | Memory of the local server for the session | Paid API use, account access |
| Operator's Context7 key (optional) | Memory of the local server for the session | Documentation quota |
| Messages, agent prompts and recent context | Memory; sent to the chosen provider | Private intent, pasted material |
| Custom agent definitions | `.local/agents.json`, ignored by Git | Private instructions |
| Repository and its records | Git, GitHub, Pages | Integrity of what the lab claims |
| CI workflow permissions | GitHub Actions | Publication of a tampered site |

## Actors · Actores

The operator (the only person with authority, simulated as reviewer), a visitor of the public demo (reads only), a model (returns text that the lab treats as data), the MCP remote (returns text), a contributor through a pull request (code under review), and a hostile local process on the operator's computer (outside what this sample can defend against).

## Trust boundaries · Fronteras de confianza

| Boundary | Crosses | Mitigation | Limit |
|---|---|---|---|
| `browser` | Operator ↔ page | Password fields without autocomplete, key cleared before the request, text nodes only, no browser storage of keys, CSP | Extensions and the clipboard are outside; the public page has no server at all |
| `local-server` | Page ↔ Python process on 127.0.0.1 | Host and Origin same-origin check, fixed routes, body size and type, connection cap applied before a thread exists, inactivity timeout and a total delivery deadline, fixed error codes, security headers | Host and Origin are a same-origin boundary for browsers, not authentication: any local process can send requests; no TLS on loopback |
| `runtime` | Server ↔ controller, agents, store | Allowlisted intents and tools, approval before effect, shared secret detector, text-only agents, atomic writes to a fixed path | In-memory state; reviewer role simulated; a model can still write misleading text |
| `git-github` | Working copy ↔ repository | Pre-commit guard over staged bytes, publication guard over every versioned candidate (hidden directories included), security gate in verify and CI, pinned actions, least privilege | A local hook can be bypassed; named patterns only; without Git the guard falls back to a narrower walk; branch protection and MFA are owner settings (NO_PROBADO until evidence) |
| `pages` | Repository ↔ public site | Deploy only from main, Pages permissions only in the deploy job, CSP meta element, no server, no keys, no visitor data | GitHub Pages adds no security headers of its own; `frame-ancestors` cannot be expressed in a meta element |
| `providers` | Server ↔ api.openai.com, api.anthropic.com | Fixed hosts over TLS, consent per connection, budgets, TTL, response size and shape limits, no retries, sanitized error codes | A request already received by the provider cannot be cancelled; provider retention follows its policy |
| `mcp` | Server ↔ mcp.context7.com | Fixed URL, two read tools, consent per query, response size limit, text returned as data | Remote DELETE not implemented; the stdio MCP server exposes two synthetic reads only |

## Data inventory · Inventario de datos

| Store | Flow | Retention | Deletion |
|---|---|---|---|
| Provider key | Typed into the connection dialog → POST /api/cloud/connect → memory of the session → `Authorization` or `x-api-key` header to the fixed host | Until disconnect, server stop, or expiry after 30 idle minutes (expired sessions are pruned when another operation is served, not at the exact minute) | Disconnect or expiry empties the reference; absolute erasure of process memory is not provided |
| Context7 key | Typed into the MCP panel → POST /api/mcp/connect → memory → bearer header to mcp.context7.com | Same as above | Same as above |
| Messages and prompts | Composer → POST /api/cloud/ask → provider request with message, recent context and the agent prompt only (no files, orders, environment or credentials) | Recent context in memory (up to 8 exchanges, 24,000 characters) | Clear conversation, disconnect, expiry or server stop |
| Conversation history | Memory per session; never written to disk, never returned by /api/state | Same as the session | Same as the session |
| `.local/agents.json` | Agents view → POST /api/custom-agents/save → atomic write to this fixed path, ignored by Git and rejected by the staged guard | Until the operator deletes the file | Operator deletes the file; the staged guard blocks it from a commit |
| Browser storage | Language, sidebar state and public MCP profiles (name, transport, URL or command) in `localStorage`; keys and conversations are never stored | Until cleared by the browser | Browser site-data removal; the public demo stores nothing else |
| Exports | Agent definition and MCP configuration downloads, created in the browser after a guard for credential patterns | On the operator's disk | Operator's responsibility; the guard is a named-pattern check, not a review |
| Third parties | OpenAI, Anthropic and Context7 receive what the rows above say and nothing else; GitHub hosts the repository and the site | Their own policies | Their own policies; `store: false` is sent to OpenAI but does not cancel every provider policy |

Not provided: zeroing of memory, isolation from other processes of the same user, encryption at rest (there is nothing at rest except `.local/agents.json`), and cancellation of a request the provider already received.

## Endpoint matrix · Matriz de endpoints

Every route the local server defines. Authority "simulated" means the request stands for a role in the fictional case; nothing authenticates a person. Session tokens (`session_id`) are returned by design by the connect routes and accepted in the session fields; they appear in no error response, state snapshot, standard error output or artifact. Common refusals on every route: 503 SERVER_BUSY written on the socket before any byte is read when the connection cap (8) is reached, 408 REQUEST_TIMEOUT after 10 seconds without bytes or when the request line, headers and body take longer than 30 seconds in total (enforced inside every read, so a continuous trickle within a line or the body ends at the deadline too), 403 HOST_OR_ORIGIN_BLOCKED, 500 INTERNAL_ERROR (no message), 501 for other methods. The listen backlog of 16 is a queue of accepted connections, not a cap. POST routes also refuse 415 JSON_REQUIRED, 413 INVALID_BODY_SIZE, 400 INVALID_JSON (non-object, invalid or deeply nested). Static assets (`/`, `/app.js`, `/cloud.js`, `/evidence.js`, `/evidence-rules.js`, `/i18n.js`, `/orientation.js`, `/studio.js`, `/style.css`, `/workbench.js`) are a fixed allowlist; anything else is 404.

| Route | Method | Fields | Limit | Authority | Errors |
|---|---|---|---|---|---|
| `GET /api/model-catalog` | GET | none | documented reference copy | public | — |
| `GET /api/state` | GET | none | memory snapshot without keys, tokens or messages | public | — |
| `GET /api/scenarios` | GET | none | fixed file | public | — |
| `GET /api/agents` | GET | none | four fixed contracts | public | — |
| `GET /api/custom-agents` | GET | none | 50 definitions, 400 KB file | public | 500 AGENT_STORE_UNREADABLE |
| `GET /api/evidence` | GET | none | fixed file | public | — |
| `GET /api/acceptance` | GET | none | fixed file | public | — |
| `GET /api/status` | GET | none | Git computation of this checkout | public | — |
| `GET /api/requirements` | GET | none | fixed file | public | — |
| `POST /api/request` | POST | order_id, intent (lookup or refund) | 4 KB | simulated operator | 200 with BLOCKED and a reason |
| `POST /api/decision` | POST | proposal_id, decision (approve or reject) | 4 KB | simulated reviewer | 409 BLOCKED, 400 INVALID_ACTION or INVALID_ARGUMENTS |
| `POST /api/execute` | POST | proposal_id, optional fail_connector | 4 KB | simulated operator | 409 BLOCKED, 400 |
| `POST /api/cloud/connect` | POST | provider, api_key, model, max_output_tokens, consent true, optional effort | 16 KB; 8 sessions | operator's own key and consent | 400 CONSENT_REQUIRED, INVALID_KEY_FORMAT, INVALID_MODEL, INVALID_OUTPUT_LIMIT, PROVIDER_UNSUPPORTED, EFFORT_UNSUPPORTED; 429 SESSION_CAPACITY; 502 API_* |
| `POST /api/cloud/ask` | POST | session_id, message, agent_id | 16 KB; 2,000 characters; 20 attempts | session token | 401 SESSION_EXPIRED, 409 REQUEST_IN_PROGRESS, 429 SESSION_REQUEST_LIMIT, 404 AGENT_NOT_FOUND, 502 API_* |
| `POST /api/cloud/configure` | POST | session_id, model, effort | 16 KB | session token | 401, 409, 400 INVALID_MODEL or EFFORT_UNSUPPORTED, 502 |
| `POST /api/cloud/clear` | POST | session_id | 16 KB | session token | 401, 409 |
| `POST /api/cloud/disconnect` | POST | session_id | 16 KB | session token | 400 INVALID_CHAT_REQUEST |
| `POST /api/mcp/connect` | POST | api_key (may be empty), consent true | 16 KB; 8 sessions | operator's consent | 400 MCP_CONSENT_REQUIRED, MCP_INVALID_KEY; 429 MCP_CAPACITY; 502 MCP_* |
| `POST /api/mcp/call` | POST | session_id, tool (two allowed), arguments, consent true | 16 KB; 1,000 characters per argument; 20 attempts; 256 KiB response; 12,000 characters shown | session token and consent per call | 401 MCP_SESSION_EXPIRED, 400 MCP_TOOL_BLOCKED or MCP_INVALID_ARGUMENTS, 409 MCP_BUSY, 429 MCP_REQUEST_LIMIT, 502 MCP_* |
| `POST /api/mcp/disconnect` | POST | session_id | 16 KB | session token | 400 MCP_INVALID_ARGUMENTS |
| `POST /api/agents/run` | POST | agent, mode, brief, language, artifacts, documentation, session_id, consent | 100 KB; 3,000-character brief; 16,000 characters of context | local mode: none; openai mode: session token and consent | 400 AGENT_*; 502 AGENT_INVALID_OUTPUT, AGENT_SENSITIVE_OUTPUT, AGENT_INCOMPLETE_OUTPUT |
| `POST /api/custom-agents/save` | POST | id, name, role, prompt, work_mode | 20 KB; 50 definitions | operator of this checkout | 400 AGENT_DEFINITION_INVALID, AGENT_SENSITIVE_INPUT; 404; 409 AGENT_STORE_FULL; 500 |

## Headers · Cabeceras

The local server sends on every response: `Content-Security-Policy` (default-src, script-src, style-src, img-src and connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'), `X-Content-Type-Options: nosniff`, `Cache-Control: no-store` and `Referrer-Policy: no-referrer`. GitHub Pages adds no such headers: the public build carries the same policy as a `<meta http-equiv="Content-Security-Policy">` element, which browsers honor for everything except `frame-ancestors`. The public page runs no server, so the only effect of framing it is cosmetic.

## Control catalog · Catálogo de controles

Generated states (`python scripts/security_catalog.py`); the checklist column holds Codex's item numbers as references.

| ID | Boundary | Control | Cases | State |
|---|---|---|---|---|
| SC-01 | runtime | Shared detector for named credential formats, private files and personal paths; guard over staged blobs, links, artifacts and every versioned candidate | C270–C273, C305, C311, C312 | VERIFICADO |
| SC-02 | runtime | Agent briefs, documentation, artifacts, model output and saved definitions reject credential material by walking every string value raw and serialized; exports guarded with the same formats in the browser, real form checked | C274, C276, C310, C316, C317 | VERIFICADO |
| SC-03 | local-server | No credential or authorization header in responses, standard error or artifacts; session tokens only where the protocol returns them; fixed 500 envelope | C275, C305 | VERIFICADO |
| SC-04 | browser | Key field cleared before each request; no key in browser storage; text nodes only | C276, C278 | VERIFICADO |
| SC-05 | runtime | Sessions discard key and history on disconnect, expiry and stop; role tasks never read chat history | C277 | PARCIAL |
| SC-06 | local-server | Connection cap before any thread or byte (503), inactivity timeout and total delivery deadline enforced inside every read (408) with recovery; body, type, nesting, route, method, Host and Origin checks | C280–C284, C308, C309, C314, C315 | VERIFICADO |
| SC-07 | providers | TTL, budget, capacity, busy flag, revocation; remote responses bounded; fixed hosts, no redirects, no retries | C285, C286 | VERIFICADO |
| SC-08 | pages | Security headers locally and the CSP meta element in the public build; endpoint matrix complete | C287–C289 | VERIFICADO |
| SC-09 | git-github | Actions pinned by verified commit SHA; persist-credentials false; minimal permissions; required check names | C290, C291 | VERIFICADO |
| SC-10 | git-github | Standard-library security gate in verify and CI; evidence without it is rejected | C292–C296 | VERIFICADO |
| SC-11 | git-github | External static analysis executed and triaged outside CI | C297 | PARCIAL |
| SC-12 | runtime | Untrusted content cannot widen tools, destinations or permissions; consent, minimization, budgets | C300, C301 | VERIFICADO |
| SC-13 | runtime | Threat model, data inventory and catalog kept with the records | C279, C298, C299 | PARCIAL |
| SC-14 | git-github | Runbook, patch policy, reporting channel, severities, rollback; synthetic drill executed | C302, C303 | VERIFICADO |
| SC-15 | git-github | Owner and provider settings: MFA, branch protection, private vulnerability reporting, Pages | C304 | NO_PROBADO |
| SC-16 | runtime | Sandboxed validation with an inspectable script: minimal root with a synthetic /etc, no writable host path, fail-closed probes inside the limits; the export owner outside the payload's namespace, non-dumpable supervisor, nested namespace with locked flags for the payload, promotion after every process ended with safe opens and limits | C306, C307, C313, C318–C321 | PARCIAL |
| SC-17 | local-server | Real authentication, user isolation, encryption at rest, durable audit, signing | — | FUTURO |

PARCIAL on SC-05, SC-13 and SC-16 means the listed cases passed but the control has only positive cases, or only one manual case; FUTURO never counts as passed. States derive from case polarities and statuses; they do not prove the checklist items a control references, which stay Codex's evaluation.

## Resumen en español

Activos: la clave del proveedor y la de Context7 (memoria del servidor local durante la sesión), mensajes y prompts (enviados solo al proveedor elegido), definiciones de agentes (`.local/agents.json`, fuera de Git), el repositorio y sus registros, y los permisos del flujo de CI. Actores: el operador (única autoridad, revisor simulado), el visitante de la demo pública, el modelo y el MCP remoto (devuelven texto que el laboratorio trata como datos), un colaborador por pull request y un proceso local hostil (fuera de lo que esta muestra puede defender).

Fronteras: navegador, servidor local (127.0.0.1; Host y Origin son una frontera de mismo origen, no autenticación frente a procesos locales), runtime, Git y GitHub, Pages (no añade cabeceras; el CSP va en un elemento meta, sin `frame-ancestors`), proveedores y MCP (destinos fijos, consentimiento, presupuestos, respuestas acotadas, sin reintentos).

Inventario de datos: cada almacén con su flujo, retención y borrado en la tabla anterior. No se proporciona borrado absoluto de memoria, aislamiento frente a otros procesos del mismo usuario ni cancelación de una solicitud ya recibida por el proveedor. La matriz de endpoints lista cada ruta con método, campos, límites, autoridad (real o simulada) y errores; un test falla si el servidor define una ruta que no está aquí. El catálogo de controles tiene cuatro estados derivados de los registros (VERIFICADO, PARCIAL, NO_PROBADO, FUTURO); los controles futuros nunca cuentan como aprobados, y la lista de 175 puntos de Codex queda fuera del repositorio como referencia.
