# AI Implementation Lab — Backend Schema

Versión documental 0.2 · 2026-10-05 · Base `95c1795` · Modelo leído de código; sin base SQL ni migraciones.

## 1. Mapa de almacenes

| Almacén | Contenido y duración |
|---|---|
| `CloudSessions.sessions` | Tokens opacos, clave, proveedor, modelo, esfuerzo, historial y presupuesto en memoria |
| Sesiones Context7 | Conexión y permisos acotados en memoria |
| `.local/agents.json` | Lista local de definiciones; ignorada en Git |
| Estado del navegador | Borrador, respuestas y agentes públicos en pestaña; preferencias/perfiles en localStorage |
| `data/*.json` | Fixtures y políticas sintéticas versionadas |
| `evidence/latest.json` | Ejecución, entorno, hashes y resultados por test |
| `evidence/sdd-check.json` | Comprobación estructural y hashes SDD |
| `specs/001-support-demo/acceptance.csv` | Casos, expectativas, estados y referencias de evidencia |

No existe tabla de usuarios, autenticación multiusuario ni almacenamiento duradero de conversación. Reiniciar backend elimina sesiones y estado histórico en memoria. localStorage contiene `lab.language`, `lab.sidebar` y `lab.mcp-profiles`; no debe describirse como almacén exclusivo de idioma.

## 2. Sesiones de proveedores

Clave de diccionario: token generado con `secrets.token_urlsafe(32)`. Campos: `key`, `provider`, `transport`, `model`, `limit`, `effort`, `history`, `touched`, `requests`, `busy`; `context_id` se añade al conversar. La referencia de transporte es objeto Python, no JSON persistido.

Máximo ocho sesiones; caducidad de 1800 segundos de inactividad al acceder; veinte peticiones compartidas entre chat y agente. Historial limitado a dieciséis mensajes y recortado por tamaño mientras conserva al menos el último intercambio. Mensaje de usuario: no vacío, máximo 2000 caracteres. Salida configurable: 256, 512, 1024, 2048, 4096 u 8192 tokens. Estos límites no son garantía de costo monetario máximo.

`RLock` protege estado y `busy` evita operaciones simultáneas incompatibles. Cambiar modelo comprueba acceso antes de confirmar configuración y limpia historia; cambiar esfuerzo conserva historia/presupuesto. Desconectar elimina sesión. Las claves no se escriben en los archivos de evidencia.

## 3. Definiciones de agentes

JSON: lista de objetos con exactamente `id`, `name`, `role`, `prompt`, `work_mode`. ID nuevo vacío en solicitud; servidor asigna `custom-` más 32 hex. Nombre 2–80 caracteres; rol 3–160; prompt 20–4000; modo `plan`, `research`, `implementation` o `review`. Máximo cincuenta filas y lectura limitada a 400000 bytes.

Guardar valida, normaliza espacios exteriores, escribe temporal y hace `os.replace` bajo lock. El detector de patrones sensibles es limitado; no equivale a detección universal de secretos. No se admiten campos de proveedor/clave ni rutas suministradas por usuario. Resolver agente añade alcance de propuesta textual y un digest del contexto; no concede herramientas.

## 4. Contratos HTTP actuales

| Método/ruta | Entrada/salida principal |
|---|---|
| GET `/api/model-catalog` | Catálogo de referencia |
| GET `/api/agents`, `/api/custom-agents` | Contratos de plantillas y lista local |
| POST `/api/custom-agents/save` | Definición cerrada → definición guardada |
| POST `/api/cloud/connect` | `api_key`, `model`, `max_output_tokens`, `consent`; opcionales `provider`, `effort` → sesión y límites |
| POST `/api/cloud/ask` | `session_id`, `message`; variante con `agent_id` resuelta por servidor → texto y uso |
| POST `/api/cloud/configure` | `session_id`, `model`, `effort` → configuración confirmada |
| POST `/api/cloud/clear`, `/disconnect` | `session_id` → resultado de limpieza/desconexión |
| POST `/api/agents/run` | Contrato de `agents.py` → propuesta y evidencia acotadas |
| POST `/api/mcp/connect`, `/call`, `/disconnect` | Contratos de `context7.py`; lectura allowlist |
| GET `/api/evidence`, `/acceptance`, `/requirements` | JSON de ejecución, CSV, requisitos extraídos del SDD |

Host/Origin se comprueban antes del enrutamiento; POST exige `application/json` y objeto JSON. Límites de cuerpo: agentes/run 100000 bytes, custom-agents/save 20000, cloud/MCP 16384, resto 4096. Errores: JSON_REQUIRED, INVALID_BODY_SIZE, INVALID_JSON, HOST_OR_ORIGIN_BLOCKED y códigos de dominio/proveedor. El detalle del contrato lo gobierna código y pruebas, no una duplicación completa aquí.

## 5. Fixtures y evidencia histórica

El controlador conserva órdenes, propuestas, aprobaciones simuladas, recibos y eventos en memoria. `data/orders.json`, `policy.json` y `scenarios.json` son archivos sintéticos; no son tablas SQL ni operaciones de clientes. Las rutas `/api/state`, `/scenarios`, `/request`, `/decision` y `/execute` se conservan en backend, aunque U12 retire su interfaz. `/api/reset` y `/api/explain` pertenecen al PR #4 y no existen en esta base.

`latest.json` identifica revisión de entrada, árbol sucio, source_id, entorno, resultados, hashes y limitaciones. acceptance.csv separa pruebas automatizadas y verificaciones manuales; su PASS no acredita aceptación de Marco. No cambiar resultados históricos para simular aprobación actual.

## 6. Fuentes

`src/lab/server.py`, `cloud.py`, `agent_store.py`, `context7.py`, `controller.py`, `web/studio.js`, `web/public-demo.js`, `scripts/verify.py`. [TRD](02_TECHNICAL_REQUIREMENTS_DOCUMENT.md) · [SDD](../../specs/001-support-demo/spec.md) · [Plan](06_IMPLEMENTATION_PLAN.md).
