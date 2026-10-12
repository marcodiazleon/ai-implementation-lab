# 1 Propósito y alcance

[Índice del libro](README.md) · Código descrito: `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be` (PR #9).

## 1.1 Qué es este repositorio

Un laboratorio pequeño y funcional con el que Marco Díaz de León muestra su método para convertir una idea de IA en una primera versión acotada: definir el problema y el alcance, fijar criterios de aceptación, coordinar la construcción y verificar el resultado. El código se escribió con asistencia de IA; la definición del problema, el alcance, los criterios y la verificación son trabajo de Marco (README, encabezado). La necesidad registrada: "A recruiter or prospective client needs to inspect how Marco defines an integration, selects tools, organizes work and verifies a result" ([spec.md](../../specs/001-support-demo/spec.md), *Need*).

Es un **ejercicio con un caso ficticio**: una tienda inventada, pedidos DEMO-101 a DEMO-105, una política de devoluciones de 100 DEMO y 14 días (D01). No hay clientes, dinero, integraciones ni resultados comerciales; ningún recibo tiene efecto real (`real_effect: False` en `src/lab/controller.py:112-114`).

## 1.2 Qué hace, en tres capas

| Capa | Qué puede hacer una persona | Qué necesita | Estado |
|---|---|---|---|
| Demo pública (GitHub Pages) | Leer la presentación en Sesión, seguir el recorrido de tres minutos en *Cómo está construido*, abrir Evidencia y ver qué se verificó, revisó, aceptó, integró y publicó por revisión; redactar borradores de agentes (solo en la pestaña) y perfiles MCP (en el almacenamiento del navegador) que no salen del navegador | Un navegador | Implementado; sin servidor, sin claves, sin datos de visitantes |
| Laboratorio local | Todo lo anterior más una conversación con OpenAI o Anthropic usando la clave propia y consentimiento explícito, agentes de texto con definiciones guardadas en `.local/`, y una conexión de lectura a Context7 | Python 3.11+ y Git; una clave solo para conversar | Implementado; la llamada real a un proveedor está registrada como `NOT_EXECUTED` por el desarrollador (`docs/project-status.json`, `live_api`) |
| Caso de devoluciones | Ejecutar los seis pasos del caso (solicitud, bloqueo sin aprobación, aprobación, fallo simulado, ejecución, reintento idempotente) | `python run.py tour` o la suite de pruebas | Simulado; retirado de la interfaz en U13 por decisión de Marco (D29, D35) |

Lo que es **futuro** y nunca se cuenta como hecho: autenticación real, aislamiento de usuarios, cifrado en reposo, auditoría durable, firma (SC-17 en el [catálogo](../threat-model.md#control-catalog--catálogo-de-controles)); un backend alojado; interoperabilidad viva con un cliente MCP (EXP-M09); los 20 elementos del backlog [S02](../../specs/002-expansion/spec.md).

## 1.3 Los cinco destinos

La navegación tiene exactamente cinco destinos, exigidos por Marco en U13 (spec.md, U13; D29) y vigentes en cada incremento posterior: **Sesión** (la conversación, con la presentación y el acceso a la conexión), **Agentes**, **MCPs**, **Cómo está construido** (el recorrido) y **Evidencia**. En el código son los cinco enlaces de `nav#mainNav` (`web/index.html:22`) y la lista `['demo','agents','mcp','method','evidence']` de `web/studio.js:4`; `#connection` abre un diálogo y no es un destino. El [capítulo 2](02-arquitectura.md#22-diagrama-de-componentes) los sitúa; el [capítulo 5](05-decisiones.md#52-producto-interfaz-y-conexión-opcional-u04u09-u13) recoge que el registro atribuye la decisión a la petición de Marco y no añade un motivo adicional.

## 1.4 Qué no cubre este libro

- No sustituye los registros: la [especificación](../../specs/001-support-demo/spec.md), el [plan](../../specs/001-support-demo/plan.md), las [tareas](../../specs/001-support-demo/tasks.md), las [decisiones](../decisions.md) y la [bitácora](../notebook.md) siguen siendo la fuente; el libro los ordena en una ruta de lectura y los cita.
- No es aceptación ni revisión: la aceptación del dueño, la revisión independiente, la integración y la publicación son registros separados ([cap. 6](06-validacion.md)). Esta documentación no cambia ninguno ni eleva la nota de seguridad, que a la fecha de este libro es 8.5/10 provisional según la cuarta revisión de Codex y queda fuera del repositorio.
- No describe los PR #4, #5 y #6, pendientes de conciliación por Marco; sus IDs están reservados en [id-registry.json](../id-registry.json).

## 1.5 Para quién y en cuánto tiempo

- **Visitante, un minuto:** lee 1.1 y 1.2 y abre la [demo pública](https://marcodiazleon.github.io/ai-implementation-lab/).
- **Revisor técnico, tres minutos:** el [diagrama de contexto](02-arquitectura.md#21-diagrama-de-contexto) y la [tabla de componentes](02-arquitectura.md#22-diagrama-de-componentes) ubican frontend, backend, adaptadores, estado, evidencia y CI con archivo y línea.
- **Quien va a tocar el código:** el [recorrido](03-recorrido-del-codigo.md), el [método](04-metodo-y-sdd.md) y el procedimiento de [validación](06-validacion.md), en ese orden.

## Summary in English

A small working lab that shows Marco's method on a fictional refund case: public static demo (presentation, three-minute tour, evidence; no server, keys or visitor data), local lab (optional conversation with the operator's own OpenAI or Anthropic key and explicit consent, text-only agents, a read-only Context7 connection) and the simulated refund case run only through `python run.py tour`. Real authentication, durable state, a hosted backend and the S02 backlog are future and never counted as done. Navigation has exactly five destinations by the owner's decision (U13). This book orders the existing records into a reading route and cites them; it is neither acceptance nor review and raises no score.
