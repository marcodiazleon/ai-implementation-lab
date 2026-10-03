# Producto y diseño — 3 de octubre de 2026

Fuente: U04. Responsable: Marco Díaz de León; ejecución técnica por tarea. La solicitud contiene dos alcances: investigar la siguiente experiencia de producto y aplicar ahora el cambio visual.

## Plan 1. Una mesa de trabajo que produzca un resultado útil

**Recomendación:** ampliar primero el análisis de solicitudes y después añadir un recorrido comercial pequeño. El visitante debe poder cambiar datos, comprender una decisión y llevarse un resumen. El [informe de investigación](INVESTIGACION_PRODUCTO_INTERACTIVO_2026-10-03.md) contiene diagnóstico, fuentes oficiales, siete opciones y criterios negativos.

| Corte | Qué hace el visitante | Qué obtiene | Relación con S02 | Cierre |
|---|---|---|---|---|
| F0. Selección coherente | Cambia de solicitud | Contexto y acciones de la solicitud visible | M02 | No puede actuar por accidente sobre una propuesta anterior |
| F1. Solicitud editable | Introduce importe, plazo y estado de un pedido ficticio | Explicación de cada condición, datos faltantes y resumen descargable | M02 y parte mínima de M10 | Dos incumplimientos muestran dos motivos; no se modifica un pedido ni se genera recibo |
| F2. Comparación | Duplica y cambia un dato | Diferencias A/B y explicación del cambio | A03/A09 | La variante no modifica política base, aprobaciones ni ejecución |
| F3. Bandeja comercial | Revisa cinco prospectos ficticios, completa necesidad/plazo/datos conocidos | Prioridad explicada, preguntas pendientes, siguiente paso y borrador editable/exportable | A02/A07 | No inventa presupuesto, contactos ni probabilidad de cierre; nada se envía |
| F4. Ingeniería visible | Abre «Cómo se comprobó» desde el resultado | Requisito, caso, prueba, resultado, fecha y versión | A08 | Un caso sin evidencia aparece pendiente |
| F5. Acceso público | Abre una URL sin instalar Python | Muestra estática interactiva equivalente en sus reglas | A01 | Pruebas de contrato compartidas; sin API privada ni datos de cliente |

Cada corte necesita su caso de uso y aceptación antes del código. No exige terminar todo S02. La investigación no activa ninguno de estos recorridos.

### Qué cambia en el análisis de solicitud

Ahora: seleccionar un caso → un resultado previsto → decisión simulada.

Propuesto: introducir o cargar datos → comprobar campos → ver cada condición → ajustar una variante → descargar una explicación.

Ejemplo de aceptación: pedido entregado hace 20 días por 180 DEMO. La pantalla explica **plazo: supera 14 días** e **importe: supera 100 DEMO**, al mismo tiempo. Cambiar a 10 días elimina el incumplimiento del plazo y conserva el del importe. Todo se calcula con reglas visibles.

### Por qué añadir el recorrido comercial

Permite demostrar un trabajo distinto: convertir información incompleta en una siguiente acción. Un prospecto puede tener una necesidad clara y presupuesto desconocido; la salida debe incluir preguntas útiles, no un porcentaje de cierre inventado.

La primera versión usa reglas y plantillas editables. Una integración con un modelo, si aporta valor medido, sería un corte posterior con proveedor, presupuesto y evaluación propios. No hacen falta CRM, envío de correo ni varios agentes para demostrar el recorrido.

### Reutilización y límites

- Reutilización inmediata: controlador, validación, estados, eventos y exportación del repositorio público.
- Aplicación de patrones: ficha de oportunidad, prioridad, historial, revisión y siguiente acción en un ejemplo original.
- Reutilización literal de otro producto: identificar componente, dependencias, licencia y material publicable antes de extraerlo. No se copió código, instrucciones, documentos ni datos privados.
- La presencia de código o documentación en otro proyecto no prueba que una integración conjunta esté terminada.

### Otras opciones para una segunda ronda

Bandeja operativa con responsables; consulta de documentos ficticios con fuentes; simulador de volumen de trabajo y tiempo estimado. Están desarrolladas en la investigación y no se agregan como tres proyectos obligatorios.

### Cómo llegará a un reclutador

127.0.0.1 abre un servidor en el propio equipo. El repositorio ya es público, pero la aplicación sigue siendo local. F5 propone una URL pública para probar una versión estática; no se expone el servidor de desarrollo.

## Plan 2. Identidad visual aplicada ahora

Objetivo: una herramienta sobria, reconocible como trabajo de Marco y fácil de leer.

| Elemento | Cambio |
|---|---|
| Identidad | Nombre completo y monograma MD; título de la muestra claramente separado |
| Colores | Fondo #080808, paneles #111113, texto #FAFAFA; secundarios #B6B6BF |
| Jerarquía | Introducción compacta, contexto del ejercicio y cifras de las reglas |
| Trabajo | Solicitud y decisión a la izquierda; criterios a la derecha; actividad debajo |
| Acciones | Botón principal blanco, secundarios oscuros; controles con foco visible |
| Navegación | Enlaces a trabajo/registro y acceso directo por teclado |
| Pantalla estrecha | Una columna; controles y tarjetas ajustados; tabla con desplazamiento propio |
| Dependencias | Tipografía del sistema; sin fuentes ni servicios externos |

Estado: implementado en HTML/CSS. Comprobaciones en [revisión visual](../reports/VISUAL_REVIEW_2026-10-03.md). El cambio visual no equivale a implementar F1–F5 ni a una certificación de accesibilidad.

Los paneles reordenables, el editor, la terminal y el chat con modelo no son necesarios para este corte. Si un recorrido posterior los necesita, se definirán como requisitos de ese recorrido.
