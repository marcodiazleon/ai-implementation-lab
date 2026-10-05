# AI Implementation Lab — Implementation Plan

Versión documental 0.2 · 2026-10-05 · Base `95c1795` · Plan de continuidad; el SDD canónico conserva autoridad.

## 1. Punto de partida

`main` observado: `81dfced`; PR #5 abierto: `fix/session-first-public`, `95c1795`; PR #4 abierto: `feat/reset-and-explain`, `ea5fe51`. No se fusionan sus ramas. Sesión, políticas y borrador PRD existen en #5; reset/explain es un incremento separado.

La copia de trabajo `C:/MASTER/lab-session-continuation` conserva las dos copias anteriores sin sobrescribir su evidencia. El método de Notion se leyó y se confirmaron base 1.0, ampliación portable 1.1 y adopción del 03/10/2026.

## 2. Responsabilidades

Marco decide producto, credenciales, publicación y aceptación; abre PRs según D20. El asistente implementa y verifica el alcance autorizado. La revisión propia se identifica como interna. No se activa automáticamente un agente independiente o monitor; su ausencia queda documentada.

## 3. Secuencia y gates

| Unidad | Referencias | Resultado y cierre |
|---|---|---|
| Estado y CI | T43,R14 | SHA/ramas y runs exactos; distinguir cola/fallo/PASS |
| Controles administrativos | T45,C145 | Protección main, colaboradores, token, workflows externos y entorno Pages comprobados |
| Paquete documental | U14,T46,R11/R12/R14 | Seis referencias leídas; seis documentos propios, enlaces y comparación sin importar datos privados |
| Revisión de Sesión | T41–T43,C139–C142 | Regresión automatizada, navegación, catálogo, diálogo, ES/EN, borrador, teclado y móvil |
| Inferencia real | C143 | Solo con clave/consentimiento del operador; registrar resultado y costo observable |
| Revisión PR #4 | Rama separada | Tests, Host/Origin en reset/explain y vocabulario DEMO-105; informe sin mezclar cambios |
| Entrega | R12,R14,D20 | Evidencia por revisión, diff, límites, revisión del propietario; merge/publicación explícitos |
| Despliegue | Pages/main | Run del workflow nuevo y revisión de URL pública sobre revisión publicada |

## 4. Método por incremento

Medir árbol y fuentes → vincular fuente/caso/requisito/tarea → implementar unidad mínima → ejecutar checks afectados → revisar salidas por caso → conservar evidencia/fallos → actualizar tareas, aceptación, notebook y estado → entregar diff y pendientes. Una corrección documental no justifica construir todo S02.

Para comportamiento: `python scripts/verify.py`; para estructura: `python scripts/sdd_check.py`; para publicación: guard de bytes preparados, build y sintaxis JavaScript. Conservar fallos causados por entorno como tales; no atribuirlos a producto sin contraste. El primer run sandbox bloqueó sockets; el run autorizado de la misma base pasó 101 tests y siete escenarios.

## 5. Comparación documental

Las seis referencias de PRODUCT_DOCUMENTS se usan como estructura: propósito/personas/aceptación; arquitectura/requisitos; navegación/errores; dirección/estados/accesibilidad; almacenes/contratos; dependencias/gates. Cada documento adapta esa estructura a Implementation Lab y enlaza S01. No se trasladan tecnologías, datos, métricas, decisiones ni capacidades de NUCLEUS. Lectura no modifica sus archivos. El inventario de referencias y hashes queda en `evidence/product-document-references.json`.

## 6. Riesgos, pendientes y reversión

CI en cola no es fallo ni PASS; resultados #4 no validan #5. Captura del propietario ausente impide comparar fidelidad. Pruebas de transporte simulado no acreditan inferencia real. Apps conectadas requieren inspección de autorizaciones de cuenta; colaboradores no equivalen a todas las aplicaciones. La política de licencia no impide técnicamente descargas/forks.

Revertir mediante un commit normal o descartar únicamente el incremento propio tras revisar el diff; conservar ramas, evidencia y trabajo previo. Sesiones en memoria no son recuperables tras reinicio. No activar SQL, autenticación, shell de agente o alojamiento de inferencia como efecto de documentación.

## 7. Autoridad y fuentes

[Tareas S01](../../specs/001-support-demo/tasks.md), [plan S01](../../specs/001-support-demo/plan.md), [acceptance](../../specs/001-support-demo/acceptance.csv), [S02](../../specs/002-expansion/spec.md), [decisiones](../decisions.md), [notebook](../notebook.md), [seguridad](../repository-security.md). [PRD](01_PRODUCT_REQUIREMENTS_DOCUMENT.md) · [TRD](02_TECHNICAL_REQUIREMENTS_DOCUMENT.md) · [App Flow](03_APP_FLOW.md) · [Design Brief](04_DESIGN_BRIEF.md) · [Backend Schema](05_BACKEND_SCHEMA.md).
