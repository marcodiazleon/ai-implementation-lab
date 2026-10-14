# 5 Decisiones: problema, decisión, motivo y límites

[Índice del libro](README.md) · Código descrito: `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be` (PR #9) · Fuente de verdad: [docs/decisions.md](../decisions.md). Este capítulo no crea un segundo registro: reutiliza los IDs existentes, cita el motivo tal como está escrito y dice **no registrado** cuando el registro calla. Lo que yo deduzco va marcado como **inferido** y nunca se atribuye a Marco ni al autor del código como un hecho.

Cómo leer la tabla: *Problema* y *Decisión* resumen el registro; *Motivo registrado* es cita o paráfrasis cercana de decisions.md; *Alternativas* y *Trade-offs / límites* solo cuando el registro las nombra; *Requisito* es el que cita el registro o, para D01–D07, la celda *Source* de la tabla de requisitos de spec.md; *Código / prueba / evidencia* es lo que el propio registro nombra. Los IDs D22–D28, D30 y D31 están reservados para los PR #4–#6 ([id-registry.json](../id-registry.json)) y no existen aquí. En decisions.md los D01–D15 no llevan fecha propia (la tabla dice "Updated 2026-10-04").

## 5.1 Decisiones fundacionales (U01–U03, 2026-10-03)

| ID | Problema | Decisión | Motivo registrado | Alternativas | Trade-offs / límites | Requisito | Código / prueba / evidencia |
|---|---|---|---|---|---|---|---|
| D01 | Hacía falta un caso concreto para el ejercicio | Tienda ficticia, ventana de 14 días, máximo 100 DEMO | "One concrete workflow makes positive and negative cases inspectable" | "another synthetic domain is possible" | "IMPLEMENTED_EXERCISE, not commercial-policy approval"; preferencia de escenario sin responder | R01, R02, R04 | no registrado en la fila; el caso vive en `src/lab/controller.py` y `data/` (ver cap. 3) |
| D02 | ¿Modelo o reglas deterministas? | Runtime determinista | "Model could add language interpretation, but no current CU requires it" | un modelo de lenguaje | revisar comparando modelos en EXP-A04 | no registrado | no registrado |
| D03 | ¿Framework, nube o biblioteca estándar? | Python estándar y servidor loopback | "Framework/cloud increase setup; reconsider for authenticated hosting" | framework o nube | TESTED_LOCALLY | R08 | no registrado |
| D04 | ¿Persistencia? | Estado en memoria | "SQLite adds durable recovery; unnecessary for a disposable session, required for persistent workflows" | SQLite | IMPLEMENTED_WITH_LIMITS; EXP-M05 | R04–R06 | no registrado |
| D05 | Mostrar integración de herramientas | Dos herramientas MCP de solo lectura | "U01 asks to show tool integration" | "HTTP/CLI remains available without MCP" | WIRE_TESTED; cliente vivo en EXP-M09 | R09 | no registrado |
| D06 | ¿Identidad real del revisor? | Rol de revisor simulado | "Real identity belongs to pilot scope" | no registrado | IMPLEMENTED_WITH_LIMITS; EXP-M04 | R03 | no registrado |
| D07 | Repetibilidad de comprobaciones | Hooks de aplicación y guarda local de Git | "Manual checks alone are less repeatable" | comprobaciones manuales | "local hooks are bypassable"; EXP-M08 | R07, R10 | no registrado |
| D08 | Reutilización del repositorio | Licencia no seleccionada | "licensing is an owner decision" | no registrado | PENDING; bloquea un paquete reutilizable, no esta revisión | no registrado | no registrado |
| D09 | El primer entregable precedió a su especificación | Completar SDD contra el libro vigente | "Reconcile existing work rather than regenerate the project" | regenerar el proyecto | CURRENT_MAINTENANCE_SCOPE | no registrado | no registrado |
| D10 | Qué hacer con 20 propuestas de expansión | Incorporarlas todas como backlog S02 | "One canonical backlog with dependencies and closure criteria" | no registrado | "implementation states are separate" | no registrado | [specs/002-expansion/spec.md](../../specs/002-expansion/spec.md) |
| D11 | Qué capítulos del método aplican | Capas de curso 00–05 | "Chapter 13 and corrected chapter 01 supersede older chapter-10 wording" | no registrado | "original book not edited" | no registrado | no registrado |
| D12 | Lenguaje promocional en la presentación | Presentación descriptiva y llana | "Replace slogan-like framing with task and result" (U02) | no registrado | "owner comprehension untested" | no registrado | no registrado |
| D13 | Cuál es la especificación activa | S01 es la activa | "A later numbered spec may be planning-only" | no registrado | S02 sigue en BACKLOG | no registrado | [project-status.json](../project-status.json) |
| D14 | Presupuesto y destino del modelo | Pendiente | no registrado | "Local model or approved remote service, compare before enabling" | PENDING para EXP-A04 | no registrado | no registrado |
| D15 | Identidad y usuarios de un piloto | Pendiente | no registrado | "Choose actual roles/resources with the business owner" | PENDING para EXP-M04/A10 | no registrado | no registrado |

Registrado en dos momentos: D03 da el motivo de instalación ("Framework/cloud increase setup") y D48/R56b dan, para U21, el de cadena de suministro comprobada por `scripts/security_check.py`. **Inferido (no registrado):** que el primer motivo precediera al segundo como razón de diseño es una lectura del orden de los registros, no algo que ninguno afirme.

## 5.2 Producto, interfaz y conexión opcional (U04–U09, U13)

| ID | Problema | Decisión | Motivo registrado | Alternativas | Trade-offs / límites | Requisito | Código / prueba / evidencia |
|---|---|---|---|---|---|---|---|
| D16 (2026-10-03) | Marco pidió rediseño en blanco y negro e investigación de producto | Cambio visual en S01 ahora; funciones de producto como propuestas S02 | no registrado más allá de la petición | "Compare extending request analysis with a bounded commercial workflow" | "no private product code, customer data or unverified integration claim" | no registrado | no registrado |
| D17 (2026-10-03) | Conversación opcional con API | Cuatro vistas; conversación OpenAI independiente con clave del operador y modelo exacto | no registrado | no registrado (el registro añade la restricción "do not import private product code") | "Fixed endpoint, explicit consent, bounded sessions and no automatic retries" | no registrado | no registrado |
| D18 | Idioma de la interfaz | Diccionario local, español por defecto, una preferencia en localStorage | "Language switching is a view operation, never a model call" | no registrado | texto de usuario/modelo y códigos técnicos sin traducir | no registrado | `web/i18n.js` (ver cap. 3) |
| D-U07 | U07 pide roles Implementer y Quality Reviewer | Cuatro roles; plantilla local más una llamada opcional al modelo; consultas Context7 explícitas "instead of model-directed tools" | no registrado | herramientas dirigidas por el modelo (implícita) | "Review remains a proposal, not test execution" | no registrado | `src/lab/agents.py` |
| U08 | Barra lateral, creación de agentes, multi-MCP, proveedor no OpenAI | Dos adaptadores fijos de proveedor; "separates configuration generation from executable connections" | no registrado | no registrado | "local text-only showcase" | no registrado | "Existing U07 executor tests remain" |
| U09 | Barra de U08 sobredimensionada | Chips selectores; catálogo público versionado "instead of claiming to list account entitlements"; parámetros nativos de esfuerzo | no registrado | no registrado | "Speed hints are qualitative and do not enable premium latency tiers" | no registrado | `src/lab/model_catalog.py` |
| D29 (2026-10-05) | U13: la conversación debe ser la experiencia principal | Sustituir los paneles de devolución por el chat; cinco destinos; ajustes de API dentro de Sesión | "Source: Marco, 2026-10-05, U13"; sin motivo adicional | no registrado | "supersedes D19's public refund presentation"; "The static preview cannot claim live cloud chat" | R31 | no registrado |

**Inferido (no registrado):** el título de D29, "Conversation is the primary experience", sugiere un motivo de enfoque de producto; el registro solo atribuye la decisión a la petición de Marco.

## 5.3 Publicación y evidencia (E-A01, U10, 2026-10-04)

| ID | Problema | Decisión | Motivo registrado | Alternativas | Trade-offs / límites | Requisito | Código / prueba / evidencia |
|---|---|---|---|---|---|---|---|
| D19 | Publicar sin servidor | Build estático en GitHub Pages con las reglas en el navegador; sin datos de visitantes | "A hosted Python server would need hosting, identity and cost decisions; the browser port reuses the fixtures" | servidor Python alojado | RESOLVED; D29 dice que sustituye "D19's public refund presentation"; el registro no dice qué pasa con el resto de D19 (hoy el build público muestra Sesión con la conexión deshabilitada, `cloud.js:32-33,63`) | no registrado | paridad C113 |
| D20 | Quién abre los PR | El dueño abre los PR; el asistente solo empuja ramas. Enmienda 2026-10-12: Marco, vía Codex, autorizó al asistente a abrir PR en borrador para revisión independiente (PR #9, #10); fusionar, publicar y todo lo que toque main sigue siendo del dueño | "Assistant-opened PRs would bypass the owner's review step" | no registrado | RESOLVED con enmienda fechada | no registrado | no registrado |
| D21 | Datos de la vista Evidencia | JSON generado de la tabla de la spec (misma expresión que sdd_check); latest.json y acceptance.csv sin cambios; spec.md no publicado | no registrado | "Publishing spec.md and parsing Markdown in the browser; recalculating states client-side" | RESOLVED | R27 | C116, C118, C119 |

## 5.4 Registros honestos y CI (U17–U20, 2026-10-11/12)

| ID | Problema | Decisión | Motivo registrado | Alternativas | Trade-offs / límites | Requisito | Código / prueba / evidencia |
|---|---|---|---|---|---|---|---|
| D32 | Los PR #4, #5 y #6 definían CI de forma distinta | Un solo verify.yml; pages.yml lo reutiliza; check_evidence.py | "Reproducibility replaces regeneration at deploy" | "publishing regenerated evidence (changes D21 without an owner decision) and keeping several workflows" | sustituye D27 (PR #4), parte de D25 (PR #5) y D22 (PR #6) solo en esta rama | R39 | verify.yml, pages.yml, scripts/check_evidence.py |
| D33 | Semántica de la insignia por requisito | FAIL > BLOQUEADO > PASS > PARCIAL "n de m" > PENDIENTE; NO_APLICA fuera del conteo con motivo | port de D24 (PR #4) | no registrado | no registrado | R36a | el registro nombra web/evidence.js; la regla vive en `web/evidence-rules.js:5-20` (referencia envejecida, fila 23 del cap. 7) |
| D34 | IDs en conflicto entre PR abiertos | id-registry.json; main inmutable; el PR abierto más antiguo conserva sus IDs | no registrado | no registrado | texto histórico sin reescribir | R36c | docs/id-registry.json, sdd_check |
| D35 | U13 quita el ejercicio de la interfaz y la constitución lo conserva como código/CLI | El recorrido lo describe; `python run.py tour` lo ejecuta | no registrado | (a) transcripción de solo lectura en Cómo está construido; (b) ejercicio interactivo fuera de Sesión | PENDING OWNER DECISION | R35b | run.py tour |
| D36 | Tres ramas declaraban 0.10, 0.11 y 1.0 | Versión 1.1 en un solo lugar | "so that no number means two things" | no registrado | informes fechados conservan sus números | R36c | project-status.json |
| D37 | Los nombres de la matriz nunca reportarían los checks requeridos | Matriz por plataforma más dos trabajos gate con nombres exactos, `if: always()` | no registrado | renombrar la matriz ("loses Python 3.11"); un check por miembro ("needs a protection change") | protección sin cambios | R40 | scripts/ci_gate.py |
| D38 | La huella de U17 "claimed more" | Manifiesto de fuentes y manifiesto de registros; acceptance.csv sin la columna de entorno | "so no file contains its own fingerprint" | no registrado | cualquier edición de registros exige una verificación nueva antes del commit | R42 | check_evidence.py |
| D39 | blob/main abría contenido más nuevo | Build y servidor registran la revisión; enlaces fijados a ella | "nothing guarantees a merge" | no registrado | un enlace etiquetado como main vivo | R43 | no registrado |
| D40 | Un `source_id` falso pasaba con mapas correctos | Digest ausente, malformado o distinto es siempre error | no registrado | no registrado | "Evidence is not regenerated to hide a mismatch" | R46 | check_committed |
| D41 | main servía estados escritos a mano tras fusionar PR #7 | Cada registro nombra su revisión; Git calcula contenido y contención | no registrado | no registrado | aceptación acotada al árbol; un merge con el mismo árbol queda cubierto | R49 | scripts/revision.py |
| D42 | "sdd_check checks structure, not meaning" | case-kinds.json y requirement_matrix.py | no registrado | no registrado | "nothing is marked executed by inspection" | R51 | case-kinds.json, requirement_matrix.py, requirements-matrix.md |
| D43 | Codex: un checkout sucio se leía como aceptado/publicado | Los estados de contenido describen los archivos servidos; sucio → falso con archivos nombrados | no registrado | no registrado | contención en main separada; "Nothing is written to the index" | R49f | build_states |
| D44 | Codex: una lista de código vacía o un reetiquetado pasaban | Referencias de código obligatorias; pisos derivados de los tests; overrides con motivo, autoridad y fecha, impresos | no registrado | no registrado | "a completeness check ... not a proof of semantics" | R51d | requirement_matrix.py |

## 5.5 Seguridad hacia nueve y sus revisiones (U21, 2026-10-12)

| ID | Problema | Decisión | Motivo registrado | Alternativas | Trade-offs / límites | Requisito | Código / prueba / evidencia |
|---|---|---|---|---|---|---|---|
| D45 | Cada guarda tenía su propia expresión regular | `src/lab/sensitive.py` para todas las guardas Python; la interfaz lo espeja | no registrado | "a third-party scanner, which would add a dependency this increment is not allowed to install" | "named formats only, no entropy analysis, a local hook can be bypassed" | R54 | src/lab/sensitive.py |
| D46 | Hilo sin tiempo de lectura (confirmado en servidor aislado) | Timeout de 10 s, semáforo de 8 → 503, 408, 400 anidado, 500 sin mensaje | no registrado | no registrado | "not protection against a hostile local process or a network exposure" | R55 | server.py |
| D47 | "a moved tag would change the code CI runs" | SHA completo por `uses:` con la versión en comentario | "behavior is unchanged because the pinned commit is the one the floating tag pointed to" | no registrado | actualizaciones manuales | R56 | scripts/security_check.py |
| D48 | "No SAST, dependency audit or secret scanner can be installed" | security_check.py en verify y CI; check_evidence rechaza un resultado ausente | "so a skipped scanner never reads as green" | no registrado | reglas con nombre; ruff en CI NO_PROBADO hasta decisión de dependencia de Marco | R56 | security_check.py, docs/supply-chain.md |
| D49 | Falta un modelo de amenazas y un catálogo | threat-model.md; estados de security-controls.json derivados de los registros; run_isolated.sh | no registrado | no registrado | "future controls never count as passed"; la lista de Codex queda fuera del repositorio | R57, R58 | threat-model.md, security-controls.json, run_isolated.sh |
| D50 | Codex: solo lectura bajo alias, memoria opcional, sondas que pasaban vacías | pivot_root a raíz mínima; cgroup de memoria obligatorio; sondas validadas | no registrado | no registrado | 11 corridas previas "reported and superseded"; exige cgroups y user namespaces | R58e | run_isolated.sh |
| D51 | Codex: semáforo después del hilo y las cabeceras; goteo | process_request adquiere el slot; REQUEST_DEADLINE | no registrado | no registrado | backlog 16 "a queue, not a cap" | R55a | LabServer.process_request |
| D52 | Codex: guardas de interfaz solo con prefijos; rama HTTP retornaba antes | web/sensitive-rules.js espeja Python; comprobado con Node | no registrado | no registrado | la guarda del navegador es la única en la ruta estática | R54g | web/sensitive-rules.js, tests/test_u21.py |
| D53 | Codex: directorios ocultos omitidos | Con Git: seguidos y no seguidos no ignorados | no registrado | no registrado | sin Git, fallback más estrecho documentado | R54b | guarda de publicación |
| D54 | Codex: /etc del host expuesto; /export fuera de cuota; sonda de memoria débil | /etc sintético por allowlist; export tras el payload; sonda = estado 137 | no registrado | no registrado | no registrado | R58e | run_isolated.sh |
| D55 | Codex: deadline armado una vez por llamada | Lector sobre el socket crudo; timeout por recepción | no registrado | no registrado | no registrado | R55a | DeadlineReader; tests |
| D56 | Codex: una asignación entrecomillada sin dígitos escapaba tras serializar | Recorrer cada cadena cruda y la serialización completa | no registrado | no registrado | no registrado | R54g | sensitive.py, sensitive-rules.js |
| D57 | Codex: /proc/<pid>/fd alcanzable, remount posible, promoción insegura (ambos reproducidos) | Tres etapas y tres niveles de confianza; promote.py con aperturas seguras | no registrado | "a second host uid for the payload (not needed … and not portable); a writable host bind for the results (rejected in D54)" | corridas anteriores "reported and superseded" | R58f | scripts/sandbox/promote.py, run_isolated.sh |

Nota de orden: en decisions.md, D58 y D57 aparecen antes que D56; el ID y la fecha son los que valen.

## 5.6 La decisión nueva de esta entrega

| ID | Problema | Decisión | Motivo registrado | Alternativas | Trade-offs / límites | Requisito | Código / prueba / evidencia |
|---|---|---|---|---|---|---|---|
| D58 (2026-10-12) | spec, plan, tasks, decisions y notebook describen el sistema por incrementos; nadie puede leer la aplicación de principio a fin sin recomponerlos | Un libro de ingeniería en `docs/book/` que consolida una ruta de lectura y diagramas que representan el código de `a16a4e6`, sin crear un segundo registro | spec.md U22: "consolidate the existing records into a reading route for the code of a16a4e6; documentation only, no acceptance, no score change" (Marco vía Codex, 2026-10-12; [decisions.md D58](../decisions.md#d58--un-libro-de-ingeniería-que-consolida-sin-sustituir-u22-r59)) | "keeping only the per-increment records; rewriting architecture.md in place as the book" | el libro no repite nada que esté en un registro salvo como cita con enlace; cuando un documento previo contradice al código, el libro lo señala en el cap. 7 y no corrige el histórico; la documentación no es aceptación ni eleva ninguna nota; el render de Mermaid es el de GitHub, reportado y no verificado con una herramienta local | R59 | docs/book/, casos C322–C324 |
| D59 (2026-10-13, después del SHA descrito) | El guardado de agentes en la demo pública comprobaba dos formatos y el almacén local los once compartidos | `saveAgent` usa `LabSensitive.findSecretsIn` sobre toda la definición y se niega con `AGENT_SENSITIVE_INPUT`, también si las reglas compartidas no están cargadas | no registrado | quitar el guardado de la demo pública; dejar la brecha registrada | RESOLVED; el dato nunca sale de la pestaña, no se afirma explotación; no sube ninguna nota | R54 | C326 (enmendado), C331 |

## 5.7 Lo que las revisiones independientes cambiaron

Las rondas de revisión de Codex y lo que cada una cerró están en el [capítulo 6](06-validacion.md#64-las-rondas-de-revisión-independiente); aquí solo la regla: toda corrección de una revisión quedó registrada **antes** del código (requisito enmendado, tarea, decisión, casos), después se implementó y por último se regeneró la evidencia, en commits separados y en ese orden. Los registros anteriores se conservan como "reported and superseded", nunca se borran.

## Summary in English

This chapter is a reading guide to [docs/decisions.md](../decisions.md), not a second register. Each row keeps the existing ID, the problem, the decision, the reason exactly as recorded, the alternatives and trade-offs only where the record names them ("no registrado" otherwise), the linked requirement and the code, tests, cases or evidence the record cites. Two inferences are marked as such and attributed to nobody. D58 is the only new decision: an engineering book that consolidates a reading route for the code at `a16a4e6` without replacing the records; documentation is not acceptance and raises no score. IDs reserved for pull requests #4–#6 are absent on purpose.
