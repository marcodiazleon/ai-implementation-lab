# Revisión español/inglés — 3 de octubre de 2026

U06 / R15,R13 / T24 / C068. Revisión del ejecutor; no aceptación de cliente.

- 57 pruebas y siete escenarios sintéticos: PASS. Sintaxis JavaScript y trazabilidad SDD comprobadas.
- Las cuatro vistas cambian entre español e inglés, incluyendo nombres accesibles, placeholders, escenarios, resultados y avisos. document.lang cambia a en/es.
- En el navegador: propuesta preparada en español, cambio a inglés, bloqueo antes de aprobar, aprobación, cambio a español y ejecución; estado y recibo conservados. Las filas del registro se traducen visualmente; los códigos originales se conservan en la evidencia.
- La selección English persistió al recargar la página. Español es el valor por defecto. El código maneja almacenamiento no disponible; esa condición no se simuló en un navegador.
- Con transporte local simulado: error de modelo traducido después de cambiar el idioma, conexión conservada, borrador intacto, pregunta y respuesta sin traducción de su contenido, contador y aviso de desconexión traducidos.
- Captura desktop: docs/assets/language-english.jpg. La vista observada fue 1280x720; no se declara una auditoría completa de accesibilidad.
- No se usaron claves reales ni se realizaron llamadas a OpenAI. El idioma de la interfaz no cambia el modelo, las autorizaciones o el contenido del chat.

Solo la preferencia es/en se guarda en localStorage. Claves y conversación siguen fuera del almacenamiento persistente de la app.
