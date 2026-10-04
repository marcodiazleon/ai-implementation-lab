# Conecta tu IA: OpenAI y Claude

U09 · S01 0.8 · R16,R21,R22,R24–R26. La demostración de devoluciones sigue siendo determinista. La nueva conversación es una función independiente y opcional.

## Uso
1. Ejecuta INICIAR_LAB.cmd desde la carpeta copiada, con Python 3.11 o posterior.
2. Abre http://127.0.0.1:8765 y entra en Conecta tu IA.
3. Elige OpenAI o Claude/Anthropic. Introduce una clave propia y un modelo habilitado en tu proyecto. El programa no selecciona otro modelo.
4. Elige el límite de salida, confirma el destino y el posible coste, y pulsa Comprobar y conectar.
5. En Sesión, selecciona un agente o el asistente general; cada envío solicita una respuesta real. Vaciar conversación elimina el contexto local, pero conserva el contador de intentos.

## Comportamiento
La comprobación consulta GET /v1/models/{id}. OpenAI usa POST /v1/responses con store:false; Claude usa POST /v1/messages con las instrucciones en system y su cabecera de versión. Los destinos son api.openai.com y api.anthropic.com, respectivamente. La clave permanece en memoria del servidor y el navegador conserva solo un identificador aleatorio de sesión. Se envían el mensaje, el contexto reciente y el prompt del agente seleccionado. No se incluyen archivos, herramientas, pedidos ni credenciales del sistema.

Máximo 2.000 caracteres por pregunta, 256–8.192 tokens de salida, 20 intentos por conexión, ocho sesiones y 30 minutos de inactividad. El contexto conserva hasta ocho intercambios y recorta intercambios completos al superar 24.000 caracteres. Los intentos fallidos también consumen el límite local. No hay reintentos ni cambio automático de proveedor/modelo. El límite de tokens incluye razonamiento y no equivale a un presupuesto monetario.

Desconectar retira la referencia local a la clave y el historial; no garantiza borrado forense de la memoria ni cancela una solicitud ya recibida por el proveedor. La limpieza de sesiones caducadas ocurre al atender otra operación. Reiniciar el servidor vacía su memoria. Recargar la página pierde el identificador del navegador; la sesión huérfana se retirará con la caducidad o al detener el servidor.

La comprobación de modelo no acredita que todos sus parámetros sean compatibles con Responses. Errores de formato, acceso, cuota o falta de texto se muestran sin copiar el cuerpo del error del proveedor. Una respuesta incompleta se identifica como tal. No se envía otra solicitud automáticamente.

## Alcance de validación
Las pruebas automatizadas sustituyen el transporte de cada proveedor por un doble local. Verifican contratos, consentimiento, sesiones, límites, desconexión, errores y separación de la evidencia del ejercicio. Una prueba con clave real y el arranque en otro equipo siguen pendientes; no se han generado cargos para validar esta entrega.

## Fuentes oficiales consultadas el 3 de octubre de 2026
- [Generación de texto y Responses](https://developers.openai.com/api/docs/guides/text).
- [Contexto de conversación](https://developers.openai.com/api/docs/guides/conversation-state).
- [Claves y operación](https://developers.openai.com/api/docs/guides/production-best-practices).
- [Retención de datos](https://developers.openai.com/api/docs/guides/your-data).

store:false no elimina todas las políticas de retención del proveedor. Esta implementación usa clave de API; no implementa inicio de sesión con ChatGPT ni Claude. Una suscripción de chat no sustituye la facturación de API.

## Traslado
Copia la carpeta del repositorio sin claves ni sesiones. No requiere paquetes de Python adicionales; Python debe estar instalado en destino. Ejecuta primero `python scripts/check_environment.py`: es una comprobación de solo lectura de versión, archivos y puerto. No instala dependencias ni comprueba credenciales. Un puerto ocupado exige revisar el servidor existente. No cambies el enlace loopback por una interfaz pública.

## Idioma de la interfaz
El selector Español / English traduce menús, formularios, estados y errores sin cambiar la conexión ni traducir el texto de preguntas o respuestas. Se guardan la preferencia de idioma, el estado del menú y las configuraciones MCP públicas en localStorage; no se guardan claves ni conversaciones. Los agentes se guardan localmente en .local/agents.json, fuera de Git.

Fuentes de Claude: [API overview](https://platform.claude.com/docs/en/api/overview) y [Messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages), consultadas el 3 de octubre de 2026.

## U09 · Modelos y esfuerzo desde Sesión
Los selectores de proveedor, modelo, esfuerzo y agente están debajo del mensaje. Puedes escribir un borrador antes de conectar. La flecha abre la conexión si aún no está configurada; al conectar conserva el borrador. El catálogo local ofrece modelos documentados para esta integración; no afirma que tu cuenta tenga acceso a todos ellos. También puedes escribir un identificador exacto en la configuración; para modelos no catalogados solo se admite el esfuerzo predeterminado.

Cambiar de modelo con una conexión activa comprueba su acceso antes de aplicarlo; si falla conserva la configuración anterior. Un cambio de modelo vacía el contexto; un cambio de esfuerzo lo conserva. Ambos mantienen el contador de intentos. Otro proveedor cierra la conexión anterior y requiere su propia clave y consentimiento. Las opciones de esfuerzo se validan en servidor: OpenAI usa `reasoning.effort`, Anthropic `output_config.effort`. El control queda en Estándar para Haiku porque esta integración no configura su presupuesto manual de thinking.

La salida permite 256, 512, 1024, 2048, 4096 u 8192 tokens; el formulario inicia en 4096. Ese límite incluye el razonamiento donde lo aplique el proveedor. Un esfuerzo alto puede agotar el límite o los 30 segundos de espera; se muestra el fallo/respuesta incompleta sin reintentos ni gastos adicionales automáticos. No se activa fast mode ni priority tier. Las descripciones de velocidad son orientativas, no mediciones de esta aplicación.

Fuentes del catálogo consultadas el 3 de octubre de 2026:
- [OpenAI: modelos](https://developers.openai.com/api/docs/models) y [razonamiento](https://developers.openai.com/api/docs/guides/reasoning).
- [Anthropic: esfuerzo](https://platform.claude.com/docs/en/build-with-claude/effort).
- [Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/overview), [Sonnet 5.5](https://platform.claude.com/docs/en/models/sonnet-5-5/overview), [Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/overview), [Haiku 4.5](https://platform.claude.com/docs/en/models/haiku-4-5/overview).
