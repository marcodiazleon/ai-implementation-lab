# Qué puede hacer el visitante dentro de AI Implementation Lab

Investigación de producto, 3 de octubre de 2026. Estado: propuesta; no implementa funcionalidades ni habilita servicios. Revisión del repositorio público en `97775f51ea701808cff656de6ed58f0680d1eef6` y fuentes oficiales. La revisión delegada se limitó al repositorio público y a fuentes oficiales. Este informe no incorpora contenido privado ni datos de clientes.

## Diagnóstico

Hoy el visitante escoge una solicitud preparada, pulsa analizar, observa un resultado y simula aprobación/ejecución. No puede construir una solicitud, comparar alternativas ni llevarse una explicación de cada condición. El selector incluso anticipa el resultado esperado. El controlador comprueba estado, plazo e importe, pero devuelve el primer bloqueo, mientras la interfaz muestra un resumen. Son observaciones del código actual, no resultados de una entrevista adicional. Fuentes: [interfaz](https://github.com/marcodiazleon/ai-implementation-lab/blob/97775f51ea701808cff656de6ed58f0680d1eef6/web/app.js), [controlador](https://github.com/marcodiazleon/ai-implementation-lab/blob/97775f51ea701808cff656de6ed58f0680d1eef6/src/lab/controller.py) y [especificación](https://github.com/marcodiazleon/ai-implementation-lab/blob/97775f51ea701808cff656de6ed58f0680d1eef6/specs/001-support-demo/spec.md).

Recomendación: convertir el ejemplo en una **mesa de decisiones de negocio**. Que la persona cambie algo y comprenda la consecuencia. La hipótesis de valor es que ese recorrido comunica mejor el criterio de implementación de Marco que acumular indicadores técnicos. Hay que comprobarla con un visitante; todavía no es un resultado medido. Esta prioridad coincide con el principio de diseñar desde lo que la persona necesita hacer y observar su comportamiento, en lugar de asumir que necesita una funcionalidad específica. [GOV.UK: necesidades de usuarios](https://www.gov.uk/service-manual/user-research/start-by-learning-user-needs).

## Siete experiencias concretas

Las siguientes son propuestas de diseño propias. Esfuerzo relativo: S = cambio contenido; M = nuevo recorrido con validación y pruebas; L = varios recorridos y contratos nuevos. No son estimaciones de horas.

| Prioridad | Experiencia y acción del visitante | Resultado visible y descargable | Alcance inicial y aceptación | Esfuerzo / relación con backlog |
|---|---|---|---|---|
| 1 | **Crear una solicitud de prueba.** Cambiar importe, días desde entrega y estado en un formulario, o cargar un ejemplo como punto de partida. | Tabla: dato introducido → regla → cumple/no cumple/no evaluable → explicación. Resumen editable para entregar a un responsable. | Solo análisis de una copia sintética. Una solicitud con 20 días y 180 DEMO muestra los dos incumplimientos, sin detener la explicación en el primero. No crea recibo ni modifica pedidos existentes. | M; nueva concreción de CU03, M02 y M10. |
| 2 | **Comparar dos decisiones.** Duplicar la solicitud y variar un dato; en un segundo paso, ensayar otra ventana de devolución. | Vista A/B que resalta qué cambió, cuáles condiciones cambian y por qué. Con 14 días frente a 15 cambia únicamente el resultado de plazo. | La política alternativa se etiqueta hipotética; no reemplaza la política base ni una aprobación. La comparación es de reglas, no una recomendación comercial automática. | S–M después de 1; extiende A03 con impacto operativo. |
| 3 | **Trabajar una bandeja comercial.** Abrir cinco prospectos inventados, completar problema, interlocutor, presupuesto conocido/desconocido y plazo; ordenar el trabajo. | Prioridad explicada por reglas visibles, información faltante, tres preguntas de descubrimiento, siguiente paso y borrador editable del próximo contacto que se puede exportar. | Nunca inventar presupuesto ni decisor; desconocido no equivale a descartado. Un formulario incompleto produce preguntas, no un porcentaje de cierre. Cambiar el plazo debe explicar el cambio de prioridad. No CRM ni envío. | M; concreta A02/A07/A10 en una experiencia de ventas. |
| 4 | **Resolver una bandeja de trabajo.** Revisar cinco solicitudes ficticias de soporte/operación, proponer responsable y ver qué impide avanzar. | Tarjetas con motivo, responsable propuesto, pendiente y siguiente acción; comparación entre orden de llegada y prioridad. | Reglas de urgencia explícitas y datos sintéticos. Una petición ambigua pasa a revisión humana. Sin programación de trabajos, notificaciones ni supuesto SLA real. | M; concreta A07, reutiliza revisión/estado. |
| 5 | **Consultar la política con su fuente.** Escribir una pregunta acotada o pulsar una sugerida. | Fragmento exacto del documento ficticio y regla relacionada; opción de abrir la fuente y probarla en el formulario. | Tres documentos originales y un pequeño índice por términos/sinónimos. Si no hay coincidencia suficiente: «No encontré esa información». Sin embeddings ni promesa de comprensión semántica. | M; concreta A05 y enlaza con 1. |
| 6 | **Ver cuánto trabajo cambia.** Aplicar reglas a 20 solicitudes ficticias y editar minutos manuales, asistidos y de revisión. | Cantidades por resultado y horas estimadas; supuestos y fórmulas visibles. Un cambio de política muestra cuántos casos pasarían a revisión. | Resultados reproducibles; no confundir solicitudes elegibles con operaciones ejecutadas ni estimaciones con ahorro obtenido. Puede dar ahorro negativo. No importar archivos externos al principio. | M; concreta A03/A09 sobre el mismo conjunto. |
| 7 | **Abrir la ingeniería de un resultado.** Desde una condición, pulsar «Cómo se comprobó». | Panel con requisito, prueba, versión, resultado observado y enlace al código/evidencia pública. | Un caso pendiente aparece pendiente. Mostrar fecha/versión del reporte para no confundir evidencia de otra versión con el estado de la sesión. No editor, terminal ni acceso arbitrario al disco. | S–M; concreta A08 aprovechando lo existente. |

La experiencia 3 puede usar un esquema de calificación como referencia, sin copiar una implementación ajena: Salesforce documenta BANT y también sus límites, entre ellos la falta de respuestas de algunos prospectos. Por eso se propone registrar información desconocida y preguntas pendientes, en lugar de producir una puntuación pretendidamente objetiva. [Salesforce Trailhead: calificación de oportunidades](https://trailhead.salesforce.com/content/learn/modules/lead-qualification-quick-look/get-to-know-lead-qualification).

Las experiencias 1, 2, 4, 6 y 7 pueden construirse con los contratos locales ya presentes más funciones deterministas nuevas. La 5 puede comenzar con búsqueda literal y normalización; las funciones de similitud de `difflib` comparan secuencias, no aportan comprensión semántica. [Python: difflib](https://docs.python.org/3/library/difflib.html). Esta viabilidad es una evaluación técnica del alcance propuesto; no se ha implementado ni probado aún.

## Primer incremento recomendado: crear y explicar una solicitud

**Objetivo:** en un recorrido de aproximadamente dos minutos como objetivo de diseño, el visitante modifica un ejemplo, entiende cada condición y descarga una explicación. El tiempo debe medirse con una persona; no se afirma haberlo logrado.

1. Entrada con tres campos: estado, días desde entrega e importe en unidades DEMO. Botón «Cargar ejemplo» opcional, sin anunciar antes la respuesta.
2. Botón «Revisar condiciones». Datos incompletos se señalan junto al campo y se conserva lo escrito.
3. Resultado con cada condición, sus valores y un resumen: cumple las condiciones / requiere revisión / faltan datos. «Cumple» nunca equivale a aprobado o ejecutado.
4. Botón «Duplicar para comparar» como siguiente corte pequeño, después de cerrar el análisis básico.
5. Botón «Descargar resumen» en JSON y texto Markdown: entradas, reglas/versiones, condiciones y limitación del ejercicio.

No añadir un campo de texto libre que finja comprender cualquier solicitud. Un futuro modelo podría extraer campos o redactar mejor el borrador, pero el usuario revisaría esos campos y el mismo evaluador comprobaría las reglas. Eso es otro incremento: selección de proveedor/modelo, presupuesto, permisos, cancelación y evaluación separada, conforme al [registro de herramientas vigente](https://github.com/marcodiazleon/ai-implementation-lab/blob/97775f51ea701808cff656de6ed58f0680d1eef6/docs/tools-and-capabilities.md).

### Diseño técnico contenido

- Añadir una función pura que devuelva una lista de condiciones; compartir las condiciones de elegibilidad con el controlador para evitar dos implementaciones de las mismas reglas. Mantener compensación previa, aprobación y ejecución en sus controles actuales.
- Entrada de análisis independiente, con esquema de campos cerrado y rangos numéricos explícitos. Campos adicionales, booleanos como números, negativos y valores no finitos deben rechazarse.
- El análisis de una variante no modifica `Lab.orders`, `Lab.policy`, propuestas ni recibos. El espacio se fija en el servidor y no admite selección de tiendas ajenas. Una ampliación posterior podría convertir una copia válida en nueva solicitud con nueva identidad; no incluirla en el primer corte.
- Etiquetar el resultado como análisis de ejercicio. Solo el flujo existente puede generar un recibo simulado bajo sus reglas actuales.
- Validar en servidor, además de ayudas de formulario. W3C advierte que la validación del navegador puede eludirse y recomienda validación también en servidor. [W3C: validación de formularios](https://www.w3.org/WAI/tutorials/forms/validation/).
- No nuevos paquetes, base de datos, cuentas, agentes en ejecución ni servicios externos. Mantener límites HTTP y representación de texto segura de la app existente.

### Criterios de aceptación que deben escribirse antes del código

| Caso | Resultado esperado |
|---|---|
| Entregado, 14 días, 100 DEMO | Cada condición elegible muestra cumplimiento; no se crea recibo. |
| Entregado, 15 días, 101 DEMO | Se explican ambos incumplimientos, con sus límites. |
| En tránsito con 0 días | Se explica que aún no está entregado; plazo desde entrega figura no evaluable. |
| Dato ausente, negativo, texto en número, infinito o campo extra | Error concreto; ninguna mutación de estado. |
| Cambio de ejemplo mientras existe una propuesta previa | No quedan acciones que aparenten pertenecer al nuevo ejemplo. Corregir M02 antes de extender el formulario. |
| Analizar repetidamente o comparar una variante | No cambia ninguna propuesta aprobada ni el estado de los casos base. |
| Exportar | El resumen corresponde a los valores/resultados mostrados e identifica versión de política; no incluye datos de otras solicitudes. |
| Teclado y zoom | Campos, errores, botones y resultados accesibles sin ratón; comprobación manual separada de pruebas de API. |
| Regresión | Se conservan los casos positivos/negativos existentes y se registra evidencia individual de los nuevos. |

Dependencias: cerrar la identificación del caso seleccionado (M02), extraer solo la función de evaluación necesaria (una parte acotada de M10), especificar campos/errores/casos y después implementar. No hace falta cerrar identidad real, persistencia o todo el backlog para este análisis sin efectos.

## Qué tomar de los otros productos

El propietario propone aprovechar trabajo de productos existentes. Esta investigación no verificó sus capacidades ni su estado. Se proponen **patrones transferibles**: separar propuesta y acción; explicar decisiones; revisar información incompleta; asignar responsable; mostrar trazabilidad; convertir una oportunidad en un siguiente paso concreto. Se pueden escribir ejemplos originales que demuestren esos patrones sin copiar módulos, instrucciones internas, bases documentales ni datos privados.

Si después se decide reutilizar código real, hace falta identificar el módulo exacto, su autorización de publicación, licencia, dependencias y pruebas, antes de extraerlo. No es necesario para el primer incremento recomendado. Esta nota no establece que los patrones ya estén implementados en un producto privado.

## Cómo lo abrirá otra persona

`127.0.0.1` es acceso a la propia máquina: el reclutador necesitaría ejecutar su copia local. No es un enlace público al equipo del autor. Para compartir por LinkedIn conviene añadir después una **versión estática interactiva** con los mismos casos y reglas de contrato, enlazada desde GitHub. El servidor Python actual permanece local; la documentación de Python advierte que `http.server` no está recomendado para producción. [IETF: direcciones loopback](https://datatracker.ietf.org/doc/html/rfc3330), [Python: http.server](https://docs.python.org/3/library/http.server.html).

Una versión pública estática sería otra entrega, con pruebas de equivalencia y revisión de contenido; no se habilita mediante esta investigación. GOV.UK recomienda usar prototipos para explorar y comprobar recorridos y evaluar aparte el paso a producción. [GOV.UK: prototipos](https://www.gov.uk/service-manual/design/making-prototypes).

## Orden de trabajo propuesto

1. Entrega visual actual: fondo negro, tipografía clara y espacios de trabajo reconocibles. Validar contraste/foco y conservar las acciones. La corrección funcional de la selección (M02) queda como primer paso antes de ampliar el análisis.
2. Primer incremento funcional: formulario sintético y explicación por condición; validar y cerrar antes de añadir otro módulo.
3. Segundo incremento: comparación A/B y reporte comprensible. Elegir después entre oportunidad comercial y bandeja operativa según qué quiera mostrar Marco primero.
4. Incorporar el visor de evidencia desde el resultado, sin convertir la página inicial en documentación técnica.
5. Preparar acceso público estático cuando el recorrido ya sea comprensible. Medir con un visitante si puede explicar qué decisión tomó y por qué.

Evitar por ahora un CRM completo, múltiples agentes, correo automático, WhatsApp, autenticación comercial, bóveda, editor/terminal o integración privada. Son alcances diferentes al objetivo de conseguir una muestra pequeña que alguien quiera utilizar y pueda comprender.
