# 3 Recorrido del código y secuencias

[Índice del libro](README.md) · Código descrito: `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be` (PR #9). Las tres secuencias dibujan comportamiento que existe en esa revisión, con el archivo y la línea de cada paso. Donde hay rechazo, error, límite o desconexión se dice qué código devuelve el servidor y qué ve la persona.

## 3.1 Mapa de carpetas en una pantalla

| Carpeta | Qué contiene | Entra en la huella de fuentes |
|---|---|---|
| `run.py`, `src/lab/cli.py` | Comandos `serve`, `demo`, `evaluate`, `mcp`, `tour`; `--port` (8765), `--lang` | Sí |
| `src/lab/` | `server.py` (HTTP), `controller.py`/`models.py`/`hooks.py` (devoluciones simuladas), `cloud.py` (proveedores), `context7.py` (MCP remoto), `agents.py`/`agent_store.py` (agentes de texto), `sensitive.py` (detector), `model_catalog.py`, `mcp_server.py` (stdio) | Sí |
| `web/` | `index.html` y los módulos de la [tabla de componentes](02-arquitectura.md#22-diagrama-de-componentes) | Sí |
| `data/`, `agents/roles.json` | Pedidos DEMO-101…105, política (100 DEMO, 14 días), 7 escenarios, 4 roles | Sí |
| `scripts/` | Verificación y gates; `sandbox/` y `browser/` | Sí |
| `tests/` | `unittest`, descubiertos por `scripts/verify.py` | Sí |
| `specs/001-support-demo/` | spec, plan, tasks, `acceptance.csv`, `case-kinds.json`, `security-controls.json` | No: huella de registros |
| `docs/project-status.json`, `docs/id-registry.json` | Registros de aceptación, revisión, integración, despliegue; IDs reservados | No: huella de registros |
| `evidence/` | `latest.json`, `sdd-check.json` escritos por `verify.py` | En ninguna huella (D38) |
| `docs/`, `reports/` | Explicación e informes; no se huellan, las pruebas los leen | No |

Las dos huellas (`source_id`, `record_id`) las calcula `scripts/check_evidence.py:29-32`; ningún archivo contiene su propia huella (D38).

## 3.2 Secuencia A: recorrido y vista Evidencia en la demo pública

Qué es el "recorrido": una página estática dentro del destino *Cómo está construido* (`web/index.html:76-115`), con cuatro pasos y una tabla de resultado escrita a mano. No ejecuta nada; `web/orientation.js:1-7` solo pliega la orientación en pantallas de 700 px o menos. El enlace *Empezar el recorrido de 3 minutos* es `href="#method"` (`index.html:37`).

```mermaid
sequenceDiagram
  autonumber
  participant V as Visitante
  participant P as GitHub Pages (estático)
  participant N as Navegador: studio.js · evidence.js · public-demo.js
  V->>P: GET index.html, JS, data/*.json
  P-->>N: build estático (build_pages.py:34-61)
  N->>N: public-demo.js añade html.public-demo y sustituye fetch (public-demo.js:6,149)
  N->>N: route() muestra Sesión · conexión deshabilitada (studio.js:11 · cloud.js:32-33,63)
  V->>N: clic "Empezar el recorrido" → #35;method (index.html:37)
  N->>N: route() muestra view-method: 4 pasos estáticos y tabla fija (index.html:76-115)
  V->>N: clic en un paso → #35;evidence/R02 (index.html:83-89)
  N->>N: load() ya corrió al cargar (evidence.js:176) · fetch de 4 rutas
  N->>P: GET data/latest.json, acceptance.csv, requirements.json, status.json (public-demo.js:147,154)
  P-->>N: archivos comprometidos en el build
  N->>N: validatePayload: forma y coherencia · un payload inválido nunca muestra PASS (evidence-rules.js:24-61)
  N->>N: statusRows: verificación, revisión, aceptación, integración, despliegue (evidence-rules.js:66-108)
  N-->>V: insignias por requisito y casos · #35;evidence/Rnn selecciona R02 (evidence.js:135,174)
```

**Equivalente en texto.** 1) Pages entrega el build; 2) `public-demo.js` marca la página como pública y redirige `/api/*` a archivos o a memoria; 3) Sesión aparece con la conexión deshabilitada; 4) el recorrido es contenido estático; 5) Evidencia lee cuatro archivos comprometidos en el build (`status.json` se calculó en CI al construir, `build_pages.py:44-46`), valida su forma antes de pintar nada y muestra cinco registros separados. En la demo pública **no hay** llamada a ningún servidor Python ni a ningún modelo.

Qué significa "mismo contenido que la revisión aceptada/publicada": `scripts/revision.py:97-112` compara el árbol de Git de la revisión registrada con el árbol de HEAD y exige que no haya archivos servidos modificados; "integrada" significa que HEAD es ancestro de `integration.main` (`revision.py:113-123`). Un candidato en rama nunca hereda el estado de main (D41, D43).

## 3.3 Secuencia B: pregunta local con conexión opcional y consentimiento

```mermaid
sequenceDiagram
  autonumber
  participant O as Operador
  participant B as Navegador: cloud.js
  participant S as server.py (127.0.0.1:8765)
  participant C as cloud.py: CloudSessions
  participant X as Proveedor (api.openai.com o api.anthropic.com)
  O->>B: Configurar conexión: proveedor, clave, modelo, esfuerzo, límite, casilla de consentimiento (required)
  B->>B: lee la clave y vacía el campo antes de enviar (cloud.js:64)
  B->>S: POST /api/cloud/connect {provider, api_key, model, effort, max_output_tokens, consent}
  S->>S: Host/Origin, Content-Type JSON, tamaño ≤ 16384, objeto JSON (server.py:260-274)
  S->>C: connect(body) (server.py:288-293)
  C->>C: consent debe ser true → si no, 400 CONSENT_REQUIRED (cloud.py:140-141)
  C->>C: formato de clave 20–300 [A-Za-z0-9_-] → 400 INVALID_KEY_FORMAT · modelo, límite 256–8192, esfuerzo · capacidad 8 → 429 SESSION_CAPACITY (cloud.py:147-158)
  C->>X: GET /v1/models/{model} con la clave (check · cloud.py:52-55)
  X-->>C: 200 o 401/403/404/429 → 502 API_KEY_REJECTED / API_ACCESS_DENIED / MODEL_UNAVAILABLE / API_LIMIT (cloud.py:35-38)
  C-->>S: {session_id = token_urlsafe(32), modelo, esfuerzo, límites} (cloud.py:162-170)
  S-->>B: 200 JSON · el token vive solo en la variable session (cloud.js:65)
  O->>B: escribe una pregunta y envía
  B->>S: POST /api/cloud/ask {session_id, message, agent_id} (cloud.js:68-70)
  S->>S: agent_store.resolve(agent_id) → instrucciones y context_id (server.py:278-280 · agent_store.py:63-73)
  S->>C: ask(body, instructions, context_id)
  C->>C: mensaje 1–2000 · busy → 409 REQUEST_IN_PROGRESS · 20 peticiones → 429 SESSION_REQUEST_LIMIT · el contador sube antes de llamar (cloud.py:176-186)
  C->>X: POST /v1/responses (store:false) o POST /v1/messages: instrucciones del agente + hasta 16 mensajes + el nuevo (cloud.py:57-66,99-115,194)
  X-->>C: texto y uso · respuesta ≤ 1 MiB · sin reintentos ni redirecciones (cloud.py:29,34,39)
  C-->>S: {text, usage, requests_used, request_limit} · historial recortado a 16 / 24 000 caracteres (cloud.py:201-203)
  S-->>B: 200 · muestra respuesta y "usadas/límite · tokens" (cloud.js:70)
  O->>B: Desconectar
  B->>S: POST /api/cloud/disconnect {session_id} (cloud.js:46)
  S->>C: disconnect: borra clave e historial de la fila (cloud.py:244-252)
  S-->>B: 200 · la vista vacía mensajes y la casilla de consentimiento
```

**Equivalente en texto y casos de rechazo.**

| Situación | Dónde se corta | Código | Qué ve la persona |
|---|---|---|---|
| Sin consentimiento | Navegador: la casilla es `required` (`index.html:67`); servidor: `cloud.py:140-141` | `400 CONSENT_REQUIRED` | Mensaje mapeado más el código (`cloud.js:12-13,66`) |
| Clave mal formada | Antes de cualquier red (`cloud.py:147-148`) | `400 INVALID_KEY_FORMAT` | Igual |
| Clave rechazada por el proveedor | `transport.check` (`cloud.py:35-38,52-55`) | `502 API_KEY_REJECTED` | Igual; el cuerpo del proveedor nunca se copia |
| Novena sesión | `cloud.py:157-158` | `429 SESSION_CAPACITY` | Igual |
| Vigésimo primera pregunta | `cloud.py:183-184`; los intentos fallidos también cuentan (`cloud.py:186`) | `429 SESSION_REQUEST_LIMIT` | Igual |
| 1800 s sin actividad | `_prune` en la siguiente operación (`cloud.py:126-131`) | `401 SESSION_EXPIRED` | El navegador descarta `session` (`cloud.js:71`) |
| Novena conexión simultánea | `server.py:121-131`, antes de crear un hilo o leer un byte | `503 SERVER_BUSY` | Igual |
| Cliente lento o incompleto | `DeadlineReader` (`server.py:41-91`): 10 s sin bytes o 30 s totales | `408 REQUEST_TIMEOUT` | Igual |
| Host u Origin ajenos | `server.py:178-181` | `403 HOST_OR_ORIGIN_BLOCKED` | Igual |
| Excepción inesperada | `server.py:189-191` | `500 INTERNAL_ERROR` sin mensaje; stderr imprime una línea fija (`server.py:144-146`) | Igual |

Qué sale hacia el proveedor y nada más: la clave en una cabecera, el modelo, las instrucciones del agente como mensaje de desarrollador o sistema, hasta 16 mensajes previos, el mensaje nuevo, el límite de tokens y el esfuerzo (`cloud.py:57-66,99-115`). Qué no sale: ningún archivo, ninguna herramienta, ningún dato de otro usuario. Lo que no se guarda: la clave en el navegador, la conversación en disco, nada en logs.

## 3.4 Secuencia C: agente en la conversación y MCP (configurar frente a conectar)

```mermaid
sequenceDiagram
  autonumber
  participant O as Operador
  participant B as Navegador: studio.js · workbench.js
  participant S as server.py
  participant A as agent_store.py · agents.py
  participant M as context7.py
  participant R as mcp.context7.com
  rect rgb(245,245,245)
  note over O,A: Agente personalizado (texto, sin herramientas)
  O->>B: Agentes: nombre, rol, prompt, modo de trabajo → Guardar
  B->>S: POST /api/custom-agents/save (≤ 20000 bytes) (studio.js:31 · server.py:276-277)
  S->>A: validate: claves exactas, longitudes, id custom-[0-9a-f]{32}, find_secrets_in (agent_store.py:32-39)
  A-->>S: 400 AGENT_SENSITIVE_INPUT si hay credencial · 409 AGENT_STORE_FULL (50 filas) · si no, escritura atómica en .local/agents.json (agent_store.py:44-61)
  S-->>B: 200 con la definición
  O->>B: Exportar → LabSensitive.findSecretsIn(row) · con hallazgo: "Retira las credenciales…" y sin descarga (studio.js:9,33)
  O->>B: Conversar → selecciona el agente en Sesión (studio.js:28)
  B->>S: POST /api/cloud/ask {…, agent_id}
  S->>A: resolve(agent_id) → rol integrado: sus instrucciones (agent_store.py:67) · personalizado: "Role/Work mode/Instructions" (71) · a ambos el sufijo "no tools, no filesystem, no authority" (72)
  note over S,A: el prompt del agente son instrucciones de texto para el modelo · no concede permisos
  end
  rect rgb(245,245,245)
  note over O,B: MCPs: configurar NO es conectar
  O->>B: Guía de perfiles: nombre, URL, transporte → Guardar / Exportar mcp-config.json
  B->>B: safeProfile: LabSensitive + palabras de credencial · rechaza usuario, contraseña, query y hash en la URL (studio.js:34-41)
  B->>B: localStorage lab.mcp-profiles (máx. 20) · descarga del JSON · ninguna conexión de red (studio.js:42-50)
  end
  rect rgb(245,245,245)
  note over O,R: Context7: conectar y llamar (opcional, solo local)
  O->>B: clave (opcional) y casilla de consentimiento → Conectar
  B->>S: POST /api/mcp/connect {api_key, consent} · el campo de clave se vacía (workbench.js:9-14)
  S->>M: connect: consent true, clave 0–300 imprimible, 8 sesiones (context7.py:75-83)
  M->>R: initialize · notifications/initialized · tools/list (context7.py:88-96)
  R-->>M: debe listar resolve-library-id y query-docs · respuesta ≤ 256 KiB, 25 s
  M-->>S: {session_id, tools}
  S-->>B: 200 JSON · workbench.js guarda la sesión en memoria (workbench.js:13)
  O->>B: herramienta, argumentos, consentimiento por llamada → Llamar
  B->>S: POST /api/mcp/call {session_id, tool, arguments, consent} (workbench.js:15-26)
  S->>M: call: MCP_CONSENT_REQUIRED · MCP_TOOL_BLOCKED · MCP_INVALID_ARGUMENTS (cadenas 1–1000 · libraryId empieza por "/") · 409 MCP_BUSY · 429 MCP_REQUEST_LIMIT (context7.py:105-124)
  M->>R: tools/call
  R-->>M: texto, truncado a 12 000 (context7.py:140)
  M-->>B: resultado en #35;mcpResult · la casilla de consentimiento se reinicia tras cada llamada (workbench.js:21,25)
  end
```

**Equivalente en texto.**

- Un agente es un rol de `agents/roles.json` o una definición guardada; en la conversación se convierte en instrucciones de texto que `agent_store.resolve` antepone al historial con un sufijo que niega herramientas y autoridad (`agent_store.py:72`). El contrato público declara `can_execute_code: False` (`agents.py:16-19`). El endpoint `POST /api/agents/run` (`agents.py:98-134`: modo `local` con plantillas o una sola llamada `cloud.task` con consentimiento) existe pero ninguna vista lo invoca; lo cubren las pruebas.
- "Configurar un MCP" en la pestaña *MCPs* produce un archivo `mcp-config.json` validado por la guarda y guardado en `localStorage`; no abre ninguna conexión.
- "Conectar Context7" sí habla con `mcp.context7.com`, solo desde el servidor local, con consentimiento en `connect` y en cada `call`, dos herramientas de lectura, 8 sesiones, 20 llamadas, TTL 1800 s, y `disconnect` local (`context7.py:145-152`). En la demo pública estas rutas responden `403 PUBLIC_DEMO_DISABLED` y el panel está oculto por CSS (`web/style.css:188`).
- El resultado de Context7 se guarda en una variable (`workbench.js:22`) que ninguna otra función lee; el texto de la interfaz decía "El Investigador podrá usar el resultado cuando lo selecciones" (`index.html:187` en `a16a4e6`), algo que el código no hace; en esta entrega el texto ES/EN pasa a describir la lectura manual sin implementar ningún reenvío (fila 19 del [cap. 7](07-operacion-y-limites.md#73-discrepancias-encontradas-entre-documentos-y-código-clasificadas)).

## 3.5 El caso de devoluciones: `python run.py tour`

`src/lab/cli.py:40-65` ejecuta seis pasos sobre un `Lab` nuevo: solicitar devolución de DEMO-101, ejecutar sin aprobación (`APPROVAL_REQUIRED`, sin recibo), aprobar como `human_reviewer`, ejecutar con `fail_connector=True` (falla **antes** de escribir el recibo, `controller.py:109-110`), ejecutar (recibo `SIM-…` con `real_effect: False`, `controller.py:112-114`) y ejecutar de nuevo (devuelve el mismo recibo, `controller.py:100-102`). La tabla de *Cómo está construido* reproduce esos recuentos; `scripts/browser/tour_result.js` compara ambos. Elegibilidad: `ALREADY_COMPENSATED`, `NOT_DELIVERED`, `OUTSIDE_WINDOW`, `ABOVE_LIMIT` (`controller.py:36-44`); un pedido de otra tienda es `ORDER_UNAVAILABLE` (`controller.py:29-34`). Todo es sintético: no hay cliente, dinero ni integración.

## Summary in English

Three sequences, every arrow anchored to a file and line of `a16a4e6`. (A) On the public demo the "tour" is static HTML inside *How it is built*; the Evidence view fetches four committed files, validates their shape before rendering and shows five separate records; no Python and no model are involved. (B) Locally, the connection dialog clears the key field before sending, the server checks origin, size and JSON, `CloudSessions.connect` refuses without `consent: true` and validates the key format before any network call, then probes the fixed provider; `ask` counts the attempt before calling, sends only the agent instructions, up to 16 prior messages and the new one, and maps every provider failure to a fixed 502 code; `disconnect` blanks key and history. (C) A custom agent is validated and stored atomically outside Git, its prompt becomes text instructions with a no-tools suffix and never a permission; configuring an MCP profile only validates, stores and exports JSON; connecting Context7 performs the real handshake with per-call consent, two read-only tools and hard limits. The refund case runs only through `python run.py tour`.
