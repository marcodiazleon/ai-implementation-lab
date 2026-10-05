# Product Requirements Document — AI Implementation Lab

Versión 0.2 · 2026-10-05 · Propietario: Marco Díaz de León · Estado: revisión interna; aceptación pendiente.
Base observada: especificación S01 1.0 y commit 95c1795. Las seis referencias locales de PRODUCT_DOCUMENTS fueron leídas en esta continuación. Se adapta su estructura a esta app; no se importan datos, métricas ni capacidades de NUCLEUS. Inventario y hashes: evidence/product-document-references.json.

## 1. Problema y propósito
Un posible cliente o reclutador necesita conocer cómo Marco convierte una necesidad en una implementación: alcance, interfaces, decisiones, pruebas y límites verificables. La demo permite inspeccionar ese trabajo y evaluar localmente un espacio de conversación con asistentes de texto. No promete resultados de negocio ni un servicio autónomo desplegado.

## 2. Personas y resultados
| Persona | Necesidad | Resultado verificable |
|---|---|---|
| Reclutador | Entender la forma de trabajar de Marco | Encontrar decisiones, estructura y evidencia atribuida |
| Cliente potencial | Explorar una implementación de IA | Recorrer cinco vistas y distinguir configuración de integración activa |
| Revisor técnico | Contrastar código y comportamiento | Ejecutar verificación local y seguir requisitos a casos y pruebas |
| Marco, mantenedor | Controlar cambios y publicación | Integrar únicamente cambios autorizados con revisión y CI |

## 3. Alcance del producto
Sesión es la entrada principal: mensajes, respuestas, proveedor, modelo, esfuerzo y agente. Incluye configuración de conexión dentro de un diálogo. Agentes permite crear y editar definiciones textuales desde plantillas o desde cero. MCPs prepara configuraciones y distingue servidores configurados de conexiones ejecutables. Cómo está construido explica componentes y método. Evidencia muestra los archivos registrados y su revisión de origen.
El ejercicio histórico de devoluciones sigue como código, CLI, fixtures y pruebas; no pertenece a la interfaz actual solicitada por Marco.

## 4. Dos modalidades
| Modalidad | Permitido | Límite |
|---|---|---|
| Vista pública estática | Explorar interfaz, catálogo y definiciones de agentes | Sin backend de inferencia; credenciales bloqueadas; definiciones en pestaña |
| Evaluación local con Python | Ejecutar backend, persistir definiciones locales y conectar API propia con consentimiento | Solo loopback; llamadas pueden generar cargos; sin autenticación multiusuario |
La licencia permite las copias necesarias para evaluación. Reutilizar, redistribuir o modificar el código fuente requiere autorización escrita. Crear datos de prueba o definiciones locales no es contribuir al repositorio.

## 5. Requisitos y aceptación
| Capacidad | Referencia canónica | Aceptación |
|---|---|---|
| Chat con conexión explícita | R16,R24, CU09 | Respuesta textual y error saneado; consentimiento y límites |
| Agentes sin herramientas de ejecución | R18,R19,R22, CU11/CU13 | Definición válida; contexto aislado; sin efectos sobre archivos fuente |
| MCP de documentación acotado | R20,R23, CU12/CU14 | Dos herramientas permitidas; exportar configuración no la ejecuta |
| Proveedor/modelo/esfuerzo | R25,R26, CU15 | Compatibilidad validada; modelo cambia historial y esfuerzo lo conserva |
| Sesión sin registro de operaciones | R30, CU17 | Cinco destinos; diálogo integrado; paneles de devoluciones ausentes |
| Evidencia fiel y derechos de evaluación | R11,R12,R14,R27, U13 | Revisión de origen visible; políticas consistentes y pendientes explícitos |
Los casos y estados se mantienen en acceptance.csv; este PRD no crea PASS nuevos.

## 6. Fuera de alcance
ChatGPT/Claude como suscripción integrada, API gratuita compartida, ejecución de shell por agentes, instalación automática de MCPs, clientes reales, pagos/reembolsos reales, aislamiento de usuarios, alta disponibilidad y latencia garantizada.

## 7. Medición y riesgos
La base 95c1795 pasó localmente 101 tests y siete escenarios, con SDD sin errores; evidence/latest.json identifica revisión y entorno. CI del HEAD 95c1795 completó Ubuntu/Windows correctamente en run 37372497568; el nuevo incremento documental requiere CI propia. No hay aceptación del propietario, revisión independiente ni inferencia real observada para esta entrega. Métricas futuras: éxito del recorrido de un visitante, comprensión de límites, incidencias por revisión y pasos para reproducir una prueba; no se inventan valores.

## 8. Autoridad y entrega
Marco decide alcance, permisos y aceptación. Codex documenta y verifica dentro del encargo. D20 conserva apertura manual de PR y revisión del propietario; publicación y aceptación son estados distintos. Riesgos: README/publicación atrasados, confundir catálogo con acceso a modelos, exposición de clave y falsa sensación de seguridad por una política. Mitigación: revisión por commit, consentimiento, loopback y controles administrativos verificados.

Fuentes: [especificación](../../specs/001-support-demo/spec.md), [decisiones](../decisions.md), [licencia](../../LICENSE.md), [estado](../project-status.json).

Paquete: [TRD](02_TECHNICAL_REQUIREMENTS_DOCUMENT.md) · [App Flow](03_APP_FLOW.md) · [Design Brief](04_DESIGN_BRIEF.md) · [Backend Schema](05_BACKEND_SCHEMA.md) · [Implementation Plan](06_IMPLEMENTATION_PLAN.md). La aceptación por caso sigue en el SDD canónico.
