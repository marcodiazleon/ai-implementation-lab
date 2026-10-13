# Libro de ingeniería · Engineering Book

**Versión del libro:** 1.0 (2026-10-12) · **Código descrito:** `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be`, cabecera del PR #9 (U21, rama `claude/laughing-rubin-6e32ve-sec`, apilada sobre PR #8 `86051b5`). Esta es la base histórica de las referencias archivo:línea; U20–U22 ya se integraron mediante PR #10 → #9 → #8. La publicación de aplicación/nombre confirmada es `8675cac`, registrada en `deployment` de [project-status.json](../project-status.json). El anclaje `a16a4e6` conserva la procedencia técnica; no significa que siga pendiente de integración.

Qué es: una ruta de lectura para entender toda la aplicación, por qué está construida así y qué decidió el proyecto. Consolida los registros existentes ([spec](../../specs/001-support-demo/spec.md), [plan](../../specs/001-support-demo/plan.md), [tasks](../../specs/001-support-demo/tasks.md), [decisions](../decisions.md), [notebook](../notebook.md)) sin crear un segundo registro: cada afirmación cita archivo y línea de ese SHA o el ID del registro. Qué no es: ni aceptación, ni revisión independiente, ni una nota de seguridad distinta de la registrada (8.5/10 provisional, cuarta revisión de Codex, fuera del repositorio).

## Rutas de lectura

| Tiempo | Quién | Lee |
|---|---|---|
| 1 minuto | Visitante | [1 · Propósito y alcance](01-proposito-y-alcance.md), secciones 1.1 y 1.2 |
| 3 minutos | Revisor | [2 · Arquitectura](02-arquitectura.md): diagrama de contexto y tabla de componentes (frontend, backend, adaptadores, estado, evidencia, CI con archivo y línea) |
| Media hora | Quien va a tocar el código | [3 · Recorrido del código](03-recorrido-del-codigo.md), [4 · Método y SDD](04-metodo-y-sdd.md), [6 · Validación](06-validacion.md) |
| Antes de decidir | Marco | [5 · Decisiones](05-decisiones.md) y [7 · Límites y discrepancias](07-operacion-y-limites.md#73-discrepancias-encontradas-entre-documentos-y-código-clasificadas) |

## Capítulos

1. [Propósito y alcance](01-proposito-y-alcance.md): qué es, tres capas (pública, local, caso simulado), los cinco destinos, qué es futuro.
2. [Arquitectura](02-arquitectura.md): diagrama de contexto, diagrama de componentes, fronteras de confianza, qué vive dónde, qué no hace.
3. [Recorrido del código](03-recorrido-del-codigo.md): mapa de carpetas y tres secuencias (recorrido y Evidencia; pregunta local con consentimiento; agente y MCP) con rechazos, errores, límites y desconexión.
4. [Método de ingeniería y SDD](04-metodo-y-sdd.md): la cadena de la necesidad a la evidencia, reglas de la constitución, vocabulario, qué hace `verify.py`.
5. [Decisiones](05-decisiones.md): D01–D58 con problema, decisión, motivo registrado, alternativas, trade-offs, requisito y evidencia; "no registrado" e "inferido" marcados.
6. [Validación](06-validacion.md): los cinco registros, CI, el corredor aislado, las rondas de revisión independiente, lo pendiente.
7. [Operación y límites](07-operacion-y-limites.md): cómo operar, límites por frontera, 24 discrepancias entre documentos y código clasificadas (histórica, corregida, decisión, pendiente técnico), validación de este libro.

## Las preguntas que responde

| Pregunta | Dónde |
|---|---|
| ¿Por qué Python y biblioteca estándar? | [5.1](05-decisiones.md#51-decisiones-fundacionales-u01u03-2026-10-03) (D03, D45, D48) |
| ¿Por qué separar Pages del backend local? | [2.1](02-arquitectura.md#21-diagrama-de-contexto), [5.3](05-decisiones.md#53-publicación-y-evidencia-e-a01-u10-2026-10-04) (D19, D29) |
| ¿Por qué datos sintéticos, nube opcional y consentimiento? | [1.1](01-proposito-y-alcance.md#11-qué-es-este-repositorio), [3.3](03-recorrido-del-codigo.md#33-secuencia-b-pregunta-local-con-conexión-opcional-y-consentimiento), [4.2](04-metodo-y-sdd.md#42-reglas-que-gobiernan-cada-cambio) |
| ¿Por qué destinos y MCP limitados, agentes de texto y claves en memoria? | [2.2](02-arquitectura.md#22-diagrama-de-componentes), [2.3](02-arquitectura.md#23-qué-vive-dónde), [3.4](03-recorrido-del-codigo.md#34-secuencia-c-agente-en-la-conversación-y-mcp-configurar-frente-a-conectar) |
| ¿Por qué conservar Sesión y los cinco destinos? | [1.3](01-proposito-y-alcance.md#13-los-cinco-destinos), [5.2](05-decisiones.md#52-producto-interfaz-y-conexión-opcional-u04u09-u13) (D29) |
| ¿Qué aportan spec, plan, tasks, tests y evidencia, y por qué un libro? | [4.1](04-metodo-y-sdd.md#41-la-cadena-de-la-necesidad-a-la-evidencia), [4.5](04-metodo-y-sdd.md#45-por-qué-un-libro-de-ingeniería) |
| ¿Por qué distinguir CI, revisión, aceptación, integración y publicación? | [6.1](06-validacion.md#61-cinco-registros-que-nadie-infiere-de-otro), [6.2](06-validacion.md#62-ci-qué-corre-y-qué-no-autoriza) |
| ¿Qué cambió tras las revisiones y qué límites permanecen? | [6.4](06-validacion.md#64-las-rondas-de-revisión-independiente), [6.5](06-validacion.md#65-lo-que-sigue-pendiente-y-no-lo-cierra-esta-documentación), [7.2](07-operacion-y-limites.md#72-límites-que-permanecen-por-frontera) |

## Cómo se mantiene

- Fuente editable: este Markdown y los bloques Mermaid dentro de cada capítulo; cada diagrama lleva debajo su equivalente en texto (lectores de pantalla, móvil, y respaldo si el render falla). Ningún CDN ni dependencia nueva: GitHub renderiza Mermaid al mostrar el archivo. Los once diagramas (contexto, navegador en carga y en uso, servidor, recorrido, conectar, preguntar, agente, perfil MCP, Context7, cadena SDD) están trazados para 390 px: verticales, etiquetas breves, tres participantes como máximo; el detalle vive en el texto (C328). Ninguna flecha ordena cajas: el orden vertical se obtiene con enlaces invisibles, y las flechas del navegador se derivan de la fuente (C329).
- Cuando cambie el código descrito, se actualiza el SHA de esta página y de cada capítulo, y las referencias archivo:línea que hayan cambiado. Los casos C322–C324 comprueban enlaces, alternativa textual y SHA ([acceptance.csv](../../specs/001-support-demo/acceptance.csv)).
- Registro de esta entrega: U22, R59, T89, D58 ([decisions.md](../decisions.md#d58--un-libro-de-ingeniería-que-consolida-sin-sustituir-u22-r59)).

## In English

An engineering book for the code at `a16a4e67b4257c2cb13054efd3ffa20acc2dd3be` (historical file-and-line reference base from PR #9; U20–U22 are now integrated through PRs #8–#10, and the confirmed runtime/name release is `8675cac`, recorded under `deployment`). It consolidates the existing records into one reading route and cites file and line for every claim; it is not acceptance, not an independent review and changes no score. Routes: one minute for a visitor (chapter 1, sections 1.1–1.2), three minutes for a reviewer (chapter 2: context diagram and component table), half an hour for someone about to change the code (chapters 3, 4, 6). Each chapter ends with a summary in English; each Mermaid diagram is followed by its textual equivalent. Chapter 7 classifies twenty-four mismatches between older documents and the code: historical entries keep a dated scope note, current guides were corrected with dated amendments, owner decisions are named and left pending, and technical gaps are recorded as pending items, never patched silently in a documentation change.
