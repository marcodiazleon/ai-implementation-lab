# AI Implementation Lab — Design Brief

Versión documental 0.2 · 2026-10-05 · Base `95c1795` · Dirección leída del código; capturas desktop/móvil revisadas internamente; comparación de referencia y aceptación pendientes.

## 1. Problema de diseño

Un visitante necesita reconocer el trabajo de Marco, entender el límite de la demo y encontrar evidencia sin aprender una consola. U12 sitúa la conversación en el centro, con una composición familiar de texto y controles compactos. No se copia código de otras aplicaciones ni se presenta una integración con sus suscripciones.

## 2. Dirección visual existente

| Elemento | Valor leído en `web/style.css` |
|---|---|
| Fondo | `--bg: #080808` |
| Superficie | `--paper: #111113` |
| Texto | `--ink: #fafafa` |
| Secundario | `--muted: #b6b6bf` |
| Borde | `--line: #3c3c43` |
| Acento | Blanco |
| Tipografía | Segoe UI, system-ui, sans-serif; monoespaciada para datos técnicos |

Interfaz oscura monocroma, superficies discretas, conversación amplia y menú lateral contraíble. La identidad de Marco y atribución factual de asistencia de IA deben mantenerse. No hay requisito nuevo de marca, fotografía o biblioteca de diseño.

## 3. Jerarquía y componentes

Primero conversación y borrador; después proveedor/modelo/esfuerzo/agente en el compositor; conexión API bajo demanda en diálogo. La barra superior conserva idioma. Los cinco destinos separan conversación, definiciones, configuración MCP, método y evidencia. Los paneles históricos de devoluciones/recibos/operaciones no se muestran.

Agentes usa plantillas y formulario editable; MCPs diferencia preparado de conectado; Evidencia muestra versión y estados. La interfaz debe explicar las limitaciones públicas antes de solicitar credenciales y bloquear su envío estático.

## 4. Lenguaje y estados

Texto directo en español e inglés. No prometer rapidez medida, acceso a modelos, ejecución autónoma o aceptación por una etiqueta. Modelo y mensajes conservan sus códigos/contenido; cambiar idioma solo modifica presentación.

En progreso: actividad real, sin porcentaje inventado. Fallo: motivo saneado. Pendiente: comprobación faltante. Probado: versión y alcance. Histórico: revisión de origen distinta. Configuración MCP preparada: no conectada. Una revisión de agente es texto propuesto, no una prueba realizada.

## 5. Accesibilidad e interacción

Selectores nativos con nombres accesibles, foco visible, etiqueta del mensaje, diálogo etiquetado y cierre por teclado. La invitación animada debe detenerse al escribir, ocultar la página o solicitar movimiento reducido. La navegación estrecha debe conservar el borrador y evitar desbordamiento horizontal de página; las tablas pueden desplazarse dentro de su región.

Revisar teclado completo, apertura/cierre y retorno de foco del diálogo, ES/EN, proveedores y anchos móvil/escritorio bajo C142. Leer CSS o pasar tests de markup no certifica accesibilidad integral. Zoom 200 % y contraste de todos los estados todavía requieren medición propia.

## 6. Entregables y límites

Mapa de navegación en [App Flow](03_APP_FLOW.md), contratos en [TRD](02_TECHNICAL_REQUIREMENTS_DOCUMENT.md), casos canónicos en [acceptance.csv](../../specs/001-support-demo/acceptance.csv). Capturas deben identificar revisión y viewport; la captura anterior de Marco está pendiente de recuperación. No se declara fidelidad visual sin verla.

Fuentes: U04/U06/U09/U12, R13/R15/R21/R25/R30, `web/index.html`, `style.css`, `cloud.js`, `studio.js`, `i18n.js`. No se implementó un rediseño adicional al escribir este documento.
