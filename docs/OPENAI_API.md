# Conecta tu IA: OpenAI y Claude

U08 · S01 0.7 · R16,R21,R22,R24. La demostración de devoluciones sigue siendo determinista. La nueva conversación es una función independiente y opcional.

## Uso
1. Ejecuta INICIAR_LAB.cmd desde la carpeta copiada, con Python 3.11 o posterior.
2. Abre http://127.0.0.1:8765 y entra en Conecta tu IA.
3. Elige OpenAI o Claude/Anthropic. Introduce una clave propia y un modelo habilitado en tu proyecto. El programa no selecciona otro modelo.
4. Elige el límite de salida, confirma el destino y el posible coste, y pulsa Comprobar y conectar.
5. En Demostración, selecciona un agente o el asistente general; cada envío solicita una respuesta real. Vaciar conversación elimina el contexto local, pero conserva el contador de intentos.

## Comportamiento
La comprobación consulta GET /v1/models/{id}. OpenAI usa POST /v1/responses con store:false; Claude usa POST /v1/messages con las instrucciones en system y su cabecera de versión. Los destinos son api.openai.com y api.anthropic.com, respectivamente. La clave permanece en memoria del servidor y el navegador conserva solo un identificador aleatorio de sesión. Se envían el mensaje, el contexto reciente y el prompt del agente seleccionado. No se incluyen archivos, herramientas, pedidos ni credenciales del sistema.

Máximo 2.000 caracteres por pregunta, 256/512/1.024 tokens de salida, 20 intentos por conexión, ocho sesiones y 30 minutos de inactividad. El contexto conserva hasta ocho intercambios y recorta intercambios completos al superar 24.000 caracteres. Los intentos fallidos también consumen el límite local. No hay reintentos ni cambio automático de proveedor/modelo. El límite de tokens incluye razonamiento y no equivale a un presupuesto monetario.

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
