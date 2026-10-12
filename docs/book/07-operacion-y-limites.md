# 7 Operación, límites y contradicciones encontradas

[Índice del libro](README.md) · Código descrito: `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be` (PR #9). Guía operativa completa: [docs/operations.md](../operations.md); seguridad operativa: [docs/security-runbook.md](../security-runbook.md).

## 7.1 Operar el laboratorio

```sh
python scripts/check_environment.py   # Python 3.11+, Git, avisos (reescritura de evidencia)
python run.py tour                    # el caso de devoluciones, sin red ni clave
python scripts/verify.py              # suite, guardas, SDD, seguridad, escenarios; reescribe 4 archivos
python run.py serve                   # http://127.0.0.1:8765 (--port 8766 si está ocupado)
python run.py mcp                     # servidor MCP por stdio, dos herramientas de lectura
```

- `verify.py` reescribe `evidence/latest.json`, `evidence/sdd-check.json`, `specs/001-support-demo/acceptance.csv` y `docs/requirements-matrix.md`; para descartar solo esos cuatro: `git checkout -- …` de esos paths (nunca el árbol completo).
- Parar el servidor (Ctrl+C) borra las referencias en memoria a claves e historiales; "un borrado absoluto de la memoria del proceso y la protección frente a otros procesos locales no se proporcionan" (R54e).
- Estado durable local: solo `.local/agents.json`. Reiniciar el servidor vacía propuestas, recibos, auditoría y sesiones.
- Revisar un candidato no publicado: traer la rama, `git checkout --detach FETCH_HEAD`, comparar `git rev-parse HEAD` con el SHA informado en su PR, `python scripts/check_evidence.py`, `python run.py serve` (README, *Published or candidate*).
- Publicación: solo Marco, con un push a `main` que `pages.yml` verifica y despliega; el asistente no abre PR (D20) ni fusiona.

## 7.2 Límites que permanecen (por frontera)

| Frontera | Límite registrado | Fuente |
|---|---|---|
| Datos | Caso ficticio; recibos simulados; ningún cliente, dinero ni integración | README, *Limits*; `controller.py:112-114` |
| Identidad | El revisor no tiene autenticación real; el operador local tiene autoridad total sobre la demo | D06, [architecture.md](../architecture.md) |
| Estado | Memoria por proceso; sin recuperación tras reinicio; `RLock` en un proceso; los hooks posteriores no se revierten transaccionalmente | D04, architecture.md *State and failures* |
| Servidor local | Mismo origen por Host/Origin, no autenticación frente a procesos locales; no protege de un proceso local hostil ni de una exposición a la red | R55e, D46 |
| Detector de credenciales | Formatos con nombre, sin análisis de entropía; el hook local es evitable; los mensajes de chat no se escanean | D45; `cloud.py:172-210` |
| Demo pública | CSP como `meta` sin `frame-ancestors`; Pages no añade cabeceras | `build_pages.py:16-17`, R55e |
| Proveedores | Hosts fijos sin reintentos; la calidad de las respuestas no se evalúa; la llamada real queda `NOT_EXECUTED` por el desarrollador | R55c, project-status `live_api` |
| MCP | Dos herramientas de lectura; interoperabilidad viva con un cliente MCP sin verificar (EXP-M09) | D05 |
| Cadena de suministro | Sin paquetes de terceros; sin SAST externo ni auditoría de dependencias en CI | D48, supply-chain.md |
| Corredor aislado | Linux con cgroups y user namespaces; el payload es root de su namespace anidado; el kernel es el del host | D57, [informe U21](../../reports/U21_SECURITY_2026-10-12.md) |
| Futuro (SC-17) | Autenticación real, aislamiento de usuarios, cifrado en reposo, auditoría durable, firma | security-controls.json |

## 7.3 Contradicciones encontradas entre documentos y código

Al escribir este libro se contrastaron los documentos con el código de `a16a4e6`. Lo que sigue **se señala y no se corrige**: modificar los registros es decisión de Marco, y el histórico no se reescribe (constitución, regla 9). Cada fila dice dónde está la discrepancia y qué dice el código hoy.

| # | Documentos | Qué dice el código o el registro más reciente |
|---|---|---|
| 1 | `decisions.md` D19 sigue en "RESOLVED" con "chat, API-key and MCP views hidden in public"; D29 dice que sustituye "D19's public refund presentation" sin decir qué pasa con el resto; la bitácora U12 dice que el build público muestra la conversación | El build público muestra Sesión con la conexión deshabilitada (`cloud.js:32-33,63`) |
| 2 | `decisions.md` cabecera "Updated 2026-10-04"; D57 aparece antes que D56 | Entradas hasta 2026-10-12 |
| 3 | `plan.md` U10: insignia "PASS if at least one PASS case has evidence" | R36a/D33: PASS solo cuando todos los casos aplicables pasaron; `evidence-rules.js:5-20` |
| 4 | `plan.md` U21 y el texto de límites de D45 dicen que el escaneo del árbol omite directorios ocultos | D53 y R54b enmendado: con Git se escanea todo candidato versionado, ocultos incluidos (`scripts/publication_check.py`) |
| 5 | S02 EXP-M07 "no CI versionado"; `capabilities.md` deja CI de navegador en EXP-M07 | CI en Linux y Windows existe (D32, R39a); las comprobaciones de navegador siguen fuera de CI |
| 6 | CU09 "Fixed HTTPS destination api.openai.com"; constitución "opt-in OpenAI text Q&A"; `capabilities.md` "Optional OpenAI" | U08 y `SECURITY.md` añaden Anthropic; `cloud.py:93` |
| 7 | CU08 "choose demonstration, conversation, API connection or engineering" | U13: cinco destinos con la conexión dentro de Sesión |
| 8 | `architecture.md` describe la vista como "selection, reviewer controls and event trace" y su diagrama parte de un operador hacia el controlador; también "The view selects when documentation is included" | `index.html` no carga `app.js` (`tests/test_session_shell.py:31`); ninguna vista llama a `/api/agents/run` ni reenvía la documentación de Context7 |
| 9 | `engineering-guide.md`: "Model integration is deferred", "no live model", roles "conceptual, not claimed independent agents" | Conversación opcional con dos proveedores (U05, U08) y cuatro roles de texto (U07) |
| 10 | `roadmap.md` (2026-10-03): "next task remains the M02 selection-state correction" | `project-status.json` `next_task` nombra la revisión U21, C304, D35, ruff, PR #4–#6 y C170 |
| 11 | `sdd-adoption.md` "Version 0.2, reviewed 2026-10-03" con alcance U17; etapa 5B "no independent-review claim" | `project-status.json` registra una revisión independiente COMPLETED sobre `fb7ecf6` |
| 12 | `project-status.json`: `current_task` "T80–T85 IMPLEMENTED"; `development_executor` nombra la rama `-sec`; `open_prs` solo #4–#6 | `tasks.md` registra T86–T88; PR #8 y #9 abiertos en borrador |
| 13 | `spec.md`, línea de versión, lista incrementos hasta U20 | El archivo define U21 y R54–R58 |
| 14 | R58a pide un canal privado "through the existing GitHub profile"; `SECURITY.md` dice "to arrange a suitable disclosure channel" | La bitácora lo lista como pendiente: no hay canal operativo confirmado |
| 15 | `SECURITY.md` "Controls not supplied: LLM prompt-injection defenses" | R57c/T84 demuestran con transportes falsos que instrucciones inyectadas no amplían herramientas ni destinos; redacciones compatibles pero distintas |
| 16 | `START_HERE_ES.md`: MCP "aquí son dos consultas de datos ficticios" | Además existe la conexión de lectura a Context7 (U07, `context7.py`) |
| 17 | `tools-and-capabilities.md`: "local check 3.12.14", revisado 2026-10-03 | CI corre 3.11 y 3.13 |
| 18 | Constitución, regla 6: "A future model proposes through the same controlled interface" | U13: el ejemplo de devoluciones es histórico como código/CLI, no interfaz actual |
| 19 | `index.html:187`: "El Investigador podrá usar el resultado cuando lo selecciones" | `workbench.js:22` guarda `documentation` y nada lo lee; `WORKBENCH.md:20` ("not forwarded automatically") coincide con el código |
| 20 | `spec.md` R21: "Demonstration embeds conversation first and optional deterministic exercise" | No hay ejercicio en la interfaz; U13 y D29 lo sustituyen |
| 21 | `WORKBENCH.md:12`: "Obvious key patterns are rejected" (demo pública) | En Pages, guardar un agente usa solo `sk-` y bloque de clave privada (`public-demo.js:119`), no los 11 patrones compartidos |
| 22 | `agents.py:27`: el modo se llama `openai` | `cloud.task` usa el proveedor de la sesión, Anthropic incluido |
| 23 | `decisions.md` D33 nombra `web/evidence.js` como código de la regla de insignias | La regla vive en `web/evidence-rules.js:5-20`; `evidence.js` la usa |

Ninguna de estas filas es un hallazgo de seguridad nuevo; son textos que envejecieron o nombres heredados. Decidir cuáles corregir, y cómo, queda para Marco; el libro describe el código tal como está.

## 7.4 Validación de este libro

Lo que se verificó para esta entrega y lo que no (detalle en el PR):

- Verificado: cada referencia archivo:línea se leyó en `a16a4e6`; los enlaces relativos de `docs/book/` resuelven (caso C322); cada diagrama Mermaid va seguido de su equivalente textual (C323); el libro nombra el SHA descrito (C324); `python scripts/sdd_check.py` y la cadena de `python scripts/verify.py` corrieron bajo el corredor aislado de tres etapas (corrida A de arranque, B y C idénticas: 219 pruebas, 7 escenarios, casos PASS 270 / NO_PROBADO 9 / FAIL 0, huella de fuentes `147511afd522…`), y un pase interno de revisión de los diagramas contra el código cuyos hallazgos se aplicaron antes de la entrega.
- Reportado, no verificado localmente: el render de Mermaid lo hace GitHub al mostrar el Markdown; en el entorno del implementador no hay un renderizador de Mermaid instalado y no se instaló ninguno, así que la sintaxis se revisó a mano. Si un diagrama no renderiza, el equivalente textual que lo sigue es la fuente accesible.
- No reclamado: aceptación, revisión independiente de los diagramas (la hace Codex), ningún cambio de nota.

## Summary in English

Operate with five commands (environment check, tour, verify, serve, stdio MCP); `verify.py` rewrites four generated files; durable local state is only `.local/agents.json`; publication happens only from main by the owner. The limits that remain are listed per boundary with their records: fictional data, simulated identity, memory-only state, a same-origin local server without authentication against local processes, named-pattern credential detection that does not scan chat messages, a static CSP without `frame-ancestors`, fixed providers without retries, read-only MCP, no third-party packages or external SAST, and a Linux-only isolated runner. Twenty-three mismatches between older documents and the code were found while writing and are listed without being corrected, because changing records is the owner's call and history is not rewritten. The book's own validation is stated honestly: references read at `a16a4e6`, links and textual alternatives checked by tests, SDD and verify run under the isolated runner, Mermaid rendering reported from GitHub rather than verified by a local tool.
