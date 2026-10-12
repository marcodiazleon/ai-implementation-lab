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
- Publicación: solo Marco, con un push a `main` que `pages.yml` verifica y despliega. El asistente puede abrir PR en borrador para revisión (D20 enmendado el 2026-10-12) y nunca fusiona ni publica.

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

## 7.3 Discrepancias encontradas entre documentos y código, clasificadas

Al escribir este libro se contrastaron los documentos con el código de `a16a4e6`. La primera versión del libro se limitó a listarlas; la revisión de Codex de `afd6e04` pidió, con razón, que una guía vigente no quede describiendo el código de forma falsa. Cada fila lleva ahora una clase (R59e):

- **HISTÓRICA**: el texto describe una versión anterior; se conserva y lleva una nota de alcance fechada.
- **CORREGIDA**: guía vigente corregida con enmienda fechada; la entrada histórica se conserva.
- **DECISIÓN**: solo Marco puede resolverla; queda pendiente y nombrada.
- **PENDIENTE TÉCNICO**: diferencia real en el código, registrada como pendiente en los registros y no parcheada en esta entrega documental.

| # | Clase | Documentos | Qué dice el código o el registro más reciente | Qué se hizo |
|---|---|---|---|---|
| 1 | DECISIÓN | `decisions.md` D19 sigue en "RESOLVED" con "chat, API-key and MCP views hidden in public"; D29 dice que sustituye "D19's public refund presentation" sin decir qué pasa con el resto; la bitácora U12 dice que el build público muestra la conversación | El build público muestra Sesión con la conexión deshabilitada (`cloud.js:32-33,63`) | Qué queda de D19 lo decide Marco; está en `next_task` de project-status.json |
| 2 | CORREGIDA | `decisions.md` cabecera "Updated 2026-10-04"; D58 y D57 aparecen antes que D56 | Entradas hasta 2026-10-12 | Cabecera enmendada: la tabla es de 2026-10-04 y las secciones fechadas se ordenan por ID |
| 3 | CORREGIDA | `plan.md` U10: insignia "PASS if at least one PASS case has evidence" | R36a/D33: PASS solo cuando todos los casos aplicables pasaron; `evidence-rules.js:5-20` | Nota fechada en plan.md que remite a R36a/D33 |
| 4 | CORREGIDA | `plan.md` U21 y el texto de límites de D45 dicen que el escaneo del árbol omite directorios ocultos | D53 y R54b enmendado: con Git se escanea todo candidato versionado, ocultos incluidos (`scripts/publication_check.py`) | Notas fechadas en plan.md y en D45 que remiten a D53 |
| 5 | CORREGIDA | S02 EXP-M07 "no CI versionado"; `capabilities.md` deja CI de navegador en EXP-M07 | CI en Linux y Windows existe (D32, R39a); las comprobaciones de navegador siguen fuera de CI | Notas fechadas en EXP-M07 y en capabilities.md |
| 6 | CORREGIDA | CU09 "Fixed HTTPS destination api.openai.com"; constitución "opt-in OpenAI text Q&A"; `capabilities.md` "Optional OpenAI" | U08 y `SECURITY.md` añaden Anthropic; `cloud.py:93` | Notas de alcance en CU09 y en la constitución (U08, U13); la fila histórica de capabilities conserva su alcance por incremento |
| 7 | HISTÓRICA | CU08 "choose demonstration, conversation, API connection or engineering" | U13: cinco destinos con la conexión dentro de Sesión | Nota de alcance en CU08 |
| 8 | CORREGIDA | `architecture.md` describe la vista como "selection, reviewer controls and event trace", su diagrama parte de un operador hacia el controlador, y dice "The view selects when documentation is included" | `index.html` no carga `app.js` (`tests/test_session_shell.py:31`); ninguna vista llama a `/api/agents/run` ni reenvía la documentación de Context7 | Nota de alcance al inicio (tabla y primer diagrama = historia U01–U12; lo vigente está en este libro), fila de la vista marcada como histórica, frase de la documentación corregida |
| 9 | CORREGIDA | `engineering-guide.md`: "Model integration is deferred", "no live model", roles "conceptual, not claimed independent agents" | Conversación opcional con dos proveedores (U05, U08) y cuatro roles de texto (U07) | Tres filas de la tabla de capas enmendadas con fecha y con el texto anterior citado |
| 10 | HISTÓRICA | `roadmap.md` (2026-10-03): "next task remains the M02 selection-state correction" | `project-status.json` `next_task` nombra lo vigente | Nota de alcance al inicio del roadmap |
| 11 | CORREGIDA | `sdd-adoption.md` "Version 0.2, reviewed 2026-10-03" con alcance U17; etapa 5B "no independent-review claim" | `project-status.json` registra una revisión independiente COMPLETED sobre `fb7ecf6` | Nota de alcance en la cabecera: 5B es la autorrevisión de esa fecha; las revisiones independientes están en project-status y en la bitácora |
| 12 | CORREGIDA | `project-status.json`: `current_task` "T80–T85 IMPLEMENTED"; `development_executor` nombra la rama `-sec`; `open_prs` solo #4–#6 | `tasks.md` registra T86–T89; PR #8, #9 y #10 abiertos en borrador | Campos actualizados (registro, no evidencia: ningún estado de aceptación, integración o despliegue cambia) |
| 13 | CORREGIDA | `spec.md`, línea de versión, lista incrementos hasta U20 | El archivo define U21, U22 y R54–R59 | Línea de versión actualizada |
| 14 | DECISIÓN | R58a pide un canal privado "through the existing GitHub profile"; `SECURITY.md` dice "to arrange a suitable disclosure channel" | No hay canal operativo confirmado | Pendiente del propietario; en `next_task` |
| 15 | CORREGIDA | `SECURITY.md` "Controls not supplied: LLM prompt-injection defenses" | R57c/T84 demuestran con transportes falsos que instrucciones inyectadas no amplían herramientas ni destinos | Frase reconciliada: no hay defensa general; sí existen esas demostraciones |
| 16 | CORREGIDA | `START_HERE_ES.md`: MCP "aquí son dos consultas de datos ficticios" | Además existe la conexión de lectura a Context7 (U07, `context7.py`) | Frase enmendada con fecha |
| 17 | CORREGIDA | `tools-and-capabilities.md`: "local check 3.12.14", revisado 2026-10-03 | CI corre 3.11 y 3.13 | Celda enmendada con fecha |
| 18 | DECISIÓN | Constitución, regla 6: "A future model proposes through the same controlled interface" | U13: el ejemplo de devoluciones es histórico como código/CLI, no interfaz actual | Principio de la constitución; su redacción es de Marco |
| 19 | CORREGIDA | `index.html:187` en `a16a4e6`: "El Investigador podrá usar el resultado cuando lo selecciones" | `workbench.js:22` guarda `documentation` y nada lo lee; `WORKBENCH.md:20` ("not forwarded automatically") coincide con el código | Texto ES/EN corregido: el resultado se muestra para leerlo y no se reenvía; sin implementar ninguna integración (C326) |
| 20 | HISTÓRICA | `spec.md` R21: "Demonstration embeds conversation first and optional deterministic exercise" | No hay ejercicio en la interfaz; U13 y D29 lo sustituyen | Nota de alcance en R21 |
| 21 | PENDIENTE TÉCNICO | `WORKBENCH.md:12`: "Obvious key patterns are rejected" (demo pública) | En Pages, guardar un agente usa solo `sk-` y bloque de clave privada (`public-demo.js:119`), no los 11 patrones compartidos del almacén local y de las exportaciones | **Brecha de cobertura de guardas**, no un mero nombre viejo: registrada en el límite de SC-02 (security-controls.json), en capabilities.md (Pendiente), en C326 y en `next_task`; no se parchea en esta entrega documental; sin afirmar explotación (el dato no sale de la pestaña) |
| 22 | PENDIENTE TÉCNICO | `agents.py:27`: el modo se llama `openai` | `cloud.task` usa el proveedor de la sesión, Anthropic incluido | Nombre heredado en código; cambiarlo es un cambio de fuente fuera de esta entrega |
| 23 | CORREGIDA | `decisions.md` D33 nombra `web/evidence.js` como código de la regla de insignias | La regla vive en `web/evidence-rules.js:5-20`; `evidence.js` la usa | Nota fechada en D33 |
| 24 | CORREGIDA | `decisions.md` D20: "the owner opens pull requests manually; the assistant only pushes branches"; este libro y `operations.md` lo presentaban como vigente | Marco, vía Codex, autorizó al asistente a abrir PR en borrador para revisión (PR #9, #10); fusionar y publicar siguen siendo del dueño | Enmienda fechada en D20; 7.1 y el cap. 5 actualizados |

Las filas PENDIENTE TÉCNICO son diferencias reales del código y quedan registradas como tales; las DECISIÓN son de Marco; las HISTÓRICA conservan su texto con aviso; las CORREGIDA llevan enmienda fechada y no reescriben la entrada original.

## 7.4 Validación de este libro

Lo que se verificó para esta entrega y lo que no (detalle en el PR):

- Verificado: cada referencia archivo:línea se leyó en `a16a4e6`; los enlaces relativos de `docs/book/` resuelven (caso C322); cada diagrama Mermaid va seguido de su equivalente textual (C323); el libro nombra el SHA descrito (C324); `python scripts/sdd_check.py` y la cadena de `python scripts/verify.py` corrieron bajo el corredor aislado de tres etapas (entrega inicial: A de arranque, B y C idénticas, 219 pruebas, PASS 270 / NO_PROBADO 9, huella `147511afd522…`; tras las correcciones de la revisión de `afd6e04`: A de arranque, B y C idénticas, 221 pruebas, 7 escenarios, casos PASS 272 / NO_PROBADO 10 / FAIL 0, huella de fuentes `71368f4bfcc6…`; el NO_PROBADO nuevo es C327), y un pase interno de revisión de los diagramas contra el código cuyos hallazgos se aplicaron antes de la entrega.
- Reportado, no verificado localmente: el render de Mermaid lo hace GitHub al mostrar el Markdown; en el entorno del implementador no hay un renderizador de Mermaid instalado y no se instaló ninguno, así que la sintaxis se revisó a mano. Si un diagrama no renderiza, el equivalente textual que lo sigue es la fuente accesible.
- Evidencia visual (R59f, C327): **no ejecutada**. Se intentó capturar el render de GitHub del SHA `77e1712` con el Chromium preinstalado a 1280 px y 390 px; la política de red del entorno deniega `github.githubassets.com` y `viewscreen.githubusercontent.com` (túnel rechazado), así que los scripts de la página y el iframe del render nunca cargan. Capacidad faltante: permitir esos dos dominios en el entorno, o que una persona capture desde su navegador. Lo que sí consta: Codex comprobó en el DOM de GitHub el render de cinco de los seis diagramas en `afd6e04` (los dos de arquitectura y las tres secuencias); el diagrama SDD del capítulo 4 no tiene evidencia de render de nadie. Legibilidad en móvil y las lecturas humanas de un y tres minutos siguen NO_PROBADO.
- No reclamado: aceptación, revisión independiente de los diagramas (la hace Codex), ningún cambio de nota.

## Summary in English

Operate with five commands (environment check, tour, verify, serve, stdio MCP); `verify.py` rewrites four generated files; durable local state is only `.local/agents.json`; publication happens only from main by the owner. The limits that remain are listed per boundary with their records: fictional data, simulated identity, memory-only state, a same-origin local server without authentication against local processes, named-pattern credential detection that does not scan chat messages, a static CSP without `frame-ancestors`, fixed providers without retries, read-only MCP, no third-party packages or external SAST, and a Linux-only isolated runner. Twenty-four mismatches between older documents and the code are classified: historical (kept with a dated scope note), corrected (current guide amended with a date, history kept), owner decision (named, pending) or technical pending (recorded, never patched silently here); the Pages agent-save guard gap and the Context7 copy are the two bounded by the review of afd6e04. The book's own validation is stated honestly: references read at `a16a4e6`, links and textual alternatives checked by tests, SDD and verify run under the isolated runner, Mermaid rendering reported from GitHub rather than verified by a local tool.
