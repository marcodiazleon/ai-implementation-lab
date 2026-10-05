# Brief de revisión — ai-implementation-lab (para un revisor externo en OpenAI)

> Copia versionada (U12, 2026-10-05) del brief entregado al revisor externo. Describe el estado previo a U12: main 81dfced y rama feat/reset-and-explain en 075db9d.

Fecha: 2026-10-05. Autor del brief: sesión Claude (ancla) de Marco Díaz de León. Documento autocontenido: el revisor no necesita acceso a conversaciones previas.

## 1. Qué es el repositorio y para qué sirve
- URL: https://github.com/marcodiazleon/ai-implementation-lab · demo pública: https://marcodiazleon.github.io/ai-implementation-lab/
- Propósito: **carta de presentación** de Marco como Forward Deployment Engineer / implementador de IA. Público objetivo: empresas que contratarían servicios (vía Vonnect, su empresa de servicios), clientes y recruiters. BrainTask (producto SaaS propio) se menciona solo por nombre.
- Contenido: un caso sintético de revisión de reembolsos (tienda ficticia, 7 solicitudes, política de ejemplo: entregado · ≤14 días · ≤100 DEMO · solo el espacio «sample-store»). Flujo: solicitud → propuesta → aprobación humana simulada → ejecución simulada con protección contra reintento → recibo local. Cadena de hashes sobre el registro de eventos. Sin LLM en el flujo determinista; chat con OpenAI/Anthropic opcional solo en la versión local con clave del operador.
- Método: desarrollo guiado por especificaciones (SDD) según el «Libro de ingeniería de desarrollo» de Marco: necesidad → casos de uso → investigación → constitución → especificación (EARS) → plan → tareas → implementación → validación → entrega. Cada requisito tiene ID (R01–R29), fuente (U01–U11 = peticiones del dueño), caso de aceptación (acceptance.csv) y test mapeado; `scripts/sdd_check.py` falla si un test no tiene fila. Estados que no se mezclan: PASS / FAIL / NO_PROBADO / BLOQUEADO / NO_APLICA. Quien construye no se aprueba: la aceptación del dueño y la revisión independiente se registran aparte.
- Stack: Python 3.10+ stdlib (sin dependencias), HTML/CSS/JS sin librerías, servidor loopback para uso local, build estático para GitHub Pages (`scripts/build_pages.py`) con la lógica portada a JS (`web/public-demo.js`) y un test de paridad Python↔JS.

## 2. Estado al 2026-10-05
- `main` = 81dfced (PR #3). Rama pendiente de merge: `feat/reset-and-explain` (075db9d): reinicio explícito con confirmación + panel «Analiza tu propia solicitud» (explicación por condición, sin crear propuesta).
- Verificación: `python scripts/verify.py` → 114 tests, 7 escenarios, `passed: true`; 135 casos PASS, 3 NO_PROBADO (manuales históricos), 0 FAIL.
- Backlog de expansión (`specs/002-expansion/tasks.md`, 20 ítems): 5 PARTIAL (A01 demo pública, A08 explorador de evidencia, M01 narrativa, M02 reinicio, M07 evidencia reproducible), 15 PENDING, 0 COMPLETE. Lo que impide cerrar los PARTIAL no es código: falta **revisión independiente** y «recorrido de otra persona» registrado.
- Entregas de los últimos 2 días (construidas por asistentes bajo encargo escrito, auditadas por una sesión ancla, mergeadas por Marco): demo pública en Pages; cierre documental + paridad; vista «Evidencia» con explorador requisito → caso → test → evidencia; reinicio + solicitud editable.
- Decisiones vigentes del dueño: público sin claves, cuentas ni datos de visitante; chat IA/MCP ocultos en público; BrainTask solo una línea; QA independiente por una sesión distinta en solo lectura; el dueño abre y mergea los PR.
- Orden de features aprobado: página Servicios/Contratar → diagnóstico guiado de oportunidad (cuestionario → brief) → simulador beneficio/coste con fórmulas visibles → vídeo narrado 90 s → accesibilidad → segundo flujo operativo (triage con escalado).

## 3. Límites declarados (no son hallazgos; ya están documentados en el repo)
Reembolsos simulados, revisor simulado (cualquier proceso local puede aprobar), estado en memoria, cadena de hashes no firmada, allowlist de herramientas ≠ defensa contra prompt injection, MCP probado solo contra un subconjunto, inferencia real de modelos NO ejecutada, segunda PC NO ejecutada, accesibilidad no certificada. Sin licencia open source (visible para inspección, no para reutilizar).

## 4. Preguntas para el revisor
Responde con evidencia concreta (archivo:línea, URL, captura descrita) y clasifica cada respuesta como OBSERVADO / INFERIDO / OPINIÓN. No asumas que algo existe porque el README lo dice.

**A. Como carta de presentación (lo más importante)**
1. Abre la demo pública sin leer el README. En 3 minutos: ¿entiendes qué hace Marco, para quién y por qué contratarlo? ¿Qué te faltó?
2. ¿Qué parte del método (requisitos con ID, casos, evidencia, estados honestos) se ve sin esfuerzo y cuál queda enterrada en Markdown?
3. ¿La vista «Evidencia» convence a un CTO o le parece ruido? ¿Qué una sola cosa la haría convincente?
4. ¿Hay algo en el sitio o el repo que un recruiter interpretaría como señal negativa (jerga, exceso de documentos, UI poco pulida, promesas vagas)?
5. ¿Qué distingue este repo de un portafolio típico de «proyecto demo con IA»? Si nada, dilo.

**B. Método y coherencia SDD**
6. Elige 3 requisitos (sugeridos: R02, R27, R28). ¿La cadena requisito → tarea → test → caso → evidencia cierra de verdad? ¿Dónde se rompe?
7. ¿El uso de EARS en R27–R29 es correcto o decorativo? ¿Algún requisito no es observable?
8. ¿La separación «constructor ≠ aprobador ≠ dueño» se nota en los documentos o es solo una declaración?
9. ¿Qué documento sobra o duplica a otro? ¿Qué documento falta para que un tercero retome el trabajo mañana?

**C. Técnica y seguridad**
10. Revisa `src/lab/server.py` y `web/public-demo.js`: ¿la versión pública expone algo que no debería (datos, claves, rutas, dependencias externas)? ¿Hay petición de red a terceros?
11. ¿El test de paridad Python↔JS (`tests/test_parity.py`) basta para afirmar «mismas reglas en el navegador»? ¿Qué caso añadirías?
12. ¿Protección contra reintento, propuesta obsoleta (`STALE_PROPOSAL`) y cadena de hashes están bien implementadas para su alcance declarado? ¿Algún error lógico?
13. ¿Qué harías para que `verify.py` corra en CI (Windows + Linux) sin inflar el proyecto?

**D. Roadmap y prioridad**
14. Con el orden aprobado (Servicios → diagnóstico → simulador → vídeo → a11y → segundo flujo), ¿cambiarías el orden? Justifica con el objetivo (que lo contraten).
15. De los 15 ítems PENDING, ¿cuáles descartarías por no aportar a la carta de presentación?
16. ¿Qué feature de una tarde de trabajo tendría el mayor efecto en la impresión de un visitante?

**E. Riesgos**
17. ¿Qué podría hacer que este repo juegue en contra de Marco en una entrevista técnica (p. ej., código generado con IA que no pueda defender línea por línea)? ¿Qué preguntas le harías para comprobarlo?
18. ¿La nota «código desarrollado con asistencia de IA; mi rol es definir, acotar y coordinar» es ventaja o debilidad para un puesto FDE? ¿Cómo la redactarías?

## 5. Formato de respuesta pedido
Lista numerada 1–18, cada punto ≤ 6 líneas, con evidencia y etiqueta OBSERVADO / INFERIDO / OPINIÓN. Cierre: 3 cambios de mayor impacto, 3 cosas que no tocar, 1 riesgo que Marco debe decidir él mismo.
