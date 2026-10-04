"use strict";
(() => {
 const english = {
 "Ir al área de trabajo": "Skip to workspace",
 "AI Implementation Lab, inicio": "AI Implementation Lab, home",
 "Secciones": "Sections",
 "Demostración": "Demonstration",
 "Conversación": "Conversation",
 "Conexión API": "API connection",
 "Cómo está construido": "How it is built",
 "DEMO LOCAL": "LOCAL DEMO",
 "Idioma": "Language",
 "ESTRATEGIA E IMPLEMENTACIÓN DE IA": "AI STRATEGY AND IMPLEMENTATION",
 "CASO 01": "CASE 01",
 "Revisión de una solicitud de devolución": "Review a refund request",
 "Consulta un pedido, revisa sus condiciones y decide el siguiente paso. Prueba también qué ocurre cuando una operación falla.": "Look up an order, review its conditions and decide the next step. Try what happens when an operation fails.",
 "Contexto del ejercicio": "Exercise context",
 "EL EJERCICIO": "THE EXERCISE",
 "Condiciones de la devolución.": "Refund conditions.",
 "Una tienda ficticia, siete solicitudes y un registro que permite seguir cada intento.": "A fictional shop, seven requests and a log of every attempt.",
 "Se aplican reglas fijas a datos de ejemplo. Sin devoluciones reales ni llamadas a modelos.": "Fixed rules apply to sample data. No real refunds or model calls.",
 "Reglas y resultados de la demostración": "Demonstration rules and results",
 "Casos disponibles": "Available cases",
 "Plazo del ejercicio": "Exercise time limit",
 "días": "days",
 "Límite por devolución": "Refund limit",
 "Recibos simulados": "Simulated receipts",
 "ENTRADA Y DECISIÓN": "INPUT AND DECISION",
 "Analizar una solicitud": "Analyze a request",
 "Solicitud ficticia": "Sample request",
 "Analizar solicitud": "Analyze request",
 "Selecciona una solicitud para comenzar.": "Select a request to begin.",
 "Revisar la devolución": "Review the refund",
 "Revisa el importe antes de decidir. La aprobación de este ejemplo se prueba sin iniciar sesión.": "Review the amount before deciding. Approval in this example can be tested without signing in.",
 "Aprobar propuesta": "Approve proposal",
 "Rechazar": "Reject",
 "Simular fallo del conector": "Simulate connector failure",
 "Intentar ejecución simulada": "Try simulated execution",
 "CRITERIOS DEL EJERCICIO": "EXERCISE CRITERIA",
 "Cómo se revisa la solicitud": "How the request is reviewed",
 "Entrada validada": "Validated input",
 "Comprueba el tipo de solicitud y sus campos.": "Checks the request type and its fields.",
 "Condiciones del pedido": "Order conditions",
 "Revisa la tienda, el plazo y el importe.": "Checks the shop, time window and amount.",
 "Aprobación o rechazo": "Approval or rejection",
 "La devolución queda pendiente hasta que decidas.": "The refund stays pending until you decide.",
 "Recibo de prueba": "Test receipt",
 "Reintentar no genera un segundo recibo.": "Retrying does not create a second receipt.",
 "Reglas del ejercicio": "Exercise rules",
 "Pedido entregado · hasta 14 días · máximo 100 unidades DEMO · solo el espacio de ejemplo.": "Delivered order · up to 14 days · maximum 100 DEMO units · sample workspace only.",
 "Son condiciones inventadas para esta muestra.": "These conditions were made up for this sample.",
 "Descargar evidencia de esta sesión": "Download session evidence",
 "ACTIVIDAD DE LA SESIÓN": "SESSION ACTIVITY",
 "Registro de operaciones": "Operation log",
 "Sin operaciones": "No operations",
 "Cada intento conserva su resultado. La comprobación de hashes detecta cambios parciales; no identifica al autor del registro.": "Each attempt retains its result. Hash checks detect partial changes; they do not identify the log's author.",
 "Eventos de la sesión": "Session events",
 "Evento": "Event",
 "Acción": "Action",
 "Resultado": "Result",
 "PREGUNTAS Y RESPUESTAS": "QUESTIONS AND ANSWERS",
 "Conversación con OpenAI": "Conversation with OpenAI",
 "Haz preguntas con tu propia conexión API. Esta conversación no consulta los archivos del proyecto ni ejecuta operaciones.": "Ask questions using your own API connection. This conversation does not read project files or execute operations.",
 "Sin conexión. Configura tu clave y modelo en Conexión API.": "Not connected. Set up your key and model under API connection.",
 "Configurar conexión": "Set up connection",
 "Tu pregunta": "Your question",
 "¿Cómo evaluarías una primera implementación de IA?": "How would you evaluate an initial AI implementation?",
 "Se enviará a OpenAI junto con el contexto reciente de esta conversación. Hasta 2.000 caracteres por pregunta y 20 intentos por conexión.": "It will be sent to OpenAI with the recent context of this conversation. Up to 2,000 characters per question and 20 attempts per connection.",
 "Enviar a OpenAI": "Send to OpenAI",
 "Vaciar conversación": "Clear conversation",
 "Desconectar": "Disconnect",
 "CONEXIÓN OPCIONAL": "OPTIONAL CONNECTION",
 "OpenAI API · clave propia": "OpenAI API · your own key",
 "La demostración funciona sin conexión. Para conversar, utiliza una clave de API y el identificador de un modelo habilitado en tu proyecto de OpenAI.": "The demonstration works offline. To chat, use an API key and the ID of a model enabled in your OpenAI project.",
 "Clave de API": "API key",
 "Identificador del modelo": "Model ID",
 "Identificador exacto de tu modelo": "Your exact model ID",
 "Máximo de tokens de salida por respuesta": "Maximum output tokens per response",
 "Destino: https://api.openai.com. El límite incluye los tokens de razonamiento; no es un presupuesto monetario. No hay cambio automático de proveedor o modelo.": "Destination: https://api.openai.com. The limit includes reasoning tokens; it is not a monetary budget. The provider and model never change automatically.",
 "Autorizo comprobar la conexión y enviar mis preguntas a OpenAI. Entiendo que el uso de la API puede generar cargos.": "I authorize checking the connection and sending my questions to OpenAI. I understand API usage may incur charges.",
 "Comprobar y conectar": "Check and connect",
 "Sin conexión.": "Not connected.",
 "Datos de esta sesión": "Session data",
 "La clave se conserva en la memoria del servidor local. No se guarda en archivos, registros, cookies ni almacenamiento del navegador. Desconectar elimina la referencia a la clave y el historial de la sesión.": "The key is held in the local server's memory. It is not saved in files, logs, cookies or browser storage. Disconnecting removes the reference to the key and the session history.",
 "La sesión caduca tras 30 minutos sin uso; el servidor retira las sesiones vencidas al atender otra operación. Reiniciar el servidor vacía todas las sesiones. Recargar la página pierde la conexión del navegador.": "The session expires after 30 minutes of inactivity; the server removes expired sessions when handling another operation. Restarting the server clears all sessions. Reloading the page loses the browser connection.",
 "Las respuestas se solicitan con store:false. Esto no elimina las políticas de retención del proveedor. No introduzcas contraseñas, datos de clientes ni documentación privada en tus preguntas.": "Responses are requested with store:false. The provider's retention policies still apply. Do not include passwords, customer data or private documents in your questions.",
 "DEL PROBLEMA A LA IMPLEMENTACIÓN": "FROM PROBLEM TO IMPLEMENTATION",
 "El recorrido conecta un problema, sus reglas, una implementación acotada y evidencia de lo que se probó.": "The walkthrough connects a problem, its rules, a scoped implementation and evidence of what was tested.",
 "Definir el alcance": "Define the scope",
 "Casos de uso, requisitos y resultados esperados antes de implementar.": "Use cases, requirements and expected results before implementation.",
 "Construir por capas": "Build in layers",
 "Interfaz, controlador, reglas y conectores con responsabilidades distintas.": "Interface, controller, rules and connectors with separate responsibilities.",
 "Probar los límites": "Test the boundaries",
 "Entradas inválidas, permisos, reintentos y fallos del proveedor.": "Invalid input, permissions, retries and provider failures.",
 "Registrar lo observado": "Record observations",
 "Resultados reproducibles, pendientes y diferencias entre simulación y uso real.": "Reproducible results, pending work and differences between simulation and real use.",
 "Especificación": "Specification",
 "Herramientas": "Tools",
 "Evidencia": "Evidence",
 "La conversación API es independiente del ejercicio de devoluciones. El servidor está diseñado para ejecutarse en tu equipo por loopback.": "API chat is independent of the refund exercise. The server is designed to run on your computer over loopback.",
 "Sesión en memoria · Reiniciar el servidor restablece los escenarios · Uso local": "In-memory session · Restarting the server resets scenarios · Local use",
 "Devolución dentro de política": "Refund within policy",
 "Fuera de plazo": "Outside the time window",
 "Importe sobre el límite": "Amount above the limit",
 "Pedido de otro espacio": "Order from another workspace",
 "Consulta sin efecto": "Read-only lookup",
 "Pedido inexistente": "Order not found",
 "Petición de herramienta no autorizada": "Unauthorized tool request",
 "Falta aprobación humana.": "Human approval is required.",
 "Importe por encima del límite.": "Amount exceeds the limit.",
 "Fuera del plazo permitido.": "Outside the allowed time window.",
 "Pedido no disponible en este espacio.": "Order unavailable in this workspace.",
 "Herramienta fuera del alcance permitido.": "Tool is outside the allowed scope.",
 "Fallo simulado: no se generó un recibo. Puedes reintentar.": "Simulated failure: no receipt was created. You can retry.",
 "La propuesta ya no corresponde a los datos vigentes.": "The proposal no longer matches the current data.",
 "Esta decisión ya no está disponible.": "This decision is no longer available.",
 "Propuesta preparada. Importe: {amount} DEMO. Espera una decisión humana.": "Proposal ready. Amount: {amount} DEMO. Waiting for a human decision.",
 "Aprobada. Ahora puedes intentar la ejecución simulada.": "Approved. You can now try the simulated execution.",
 "Rechazada. La ejecución permanecerá bloqueada.": "Rejected. Execution will remain blocked.",
 "Recibo simulado: {id}. No hubo operación real.": "Simulated receipt: {id}. No real operation took place.",
 "Consulta completada: {id} · {status}": "Lookup complete: {id} · {status}",
 "CADENA COHERENTE": "CONSISTENT CHAIN",
 "REVISAR CADENA": "CHECK CHAIN",
 "No se pudo contactar al servidor local. Comprueba que siga activo.": "Could not reach the local server. Check that it is running.",
 "Pulsa Analizar solicitud para revisar este caso.": "Select Analyze request to review this case.",
 "{id} · resultado esperado: {status}": "{id} · expected result: {status}",
 "Confirma la autorización antes de conectar.": "Confirm authorization before connecting.",
 "Revisa el formato de la clave.": "Check the key format.",
 "Revisa el identificador del modelo.": "Check the model ID.",
 "OpenAI rechazó la clave.": "OpenAI rejected the key.",
 "Tu proyecto no tiene acceso a este recurso.": "Your project cannot access this resource.",
 "El modelo no está disponible para esta clave.": "The model is unavailable for this key.",
 "OpenAI informó un límite de uso. Revisa tu cuenta antes de reintentar.": "OpenAI reported a usage limit. Check your account before retrying.",
 "OpenAI no completó la solicitud. El modelo puede no admitir estos parámetros.": "OpenAI did not complete the request. The model may not support these parameters.",
 "No se completó la conexión. No se reintentó automáticamente.": "The connection did not complete. No automatic retry was made.",
 "La API no devolvió texto utilizable. Revisa el modelo y el límite de salida.": "The API returned no usable text. Check the model and output limit.",
 "La respuesta excedió el tamaño permitido.": "The response exceeded the allowed size.",
 "La conexión caducó o se cerró. Conecta de nuevo.": "The connection expired or closed. Connect again.",
 "Hay demasiadas sesiones locales. Espera su caducidad o reinicia el servidor.": "There are too many local sessions. Wait for them to expire or restart the server.",
 "Alcanzaste los 20 intentos de esta conexión. Revisa tu uso antes de volver a conectar.": "You reached 20 attempts on this connection. Review your usage before reconnecting.",
 "Ya hay una solicitud en curso.": "A request is already in progress.",
 "Escribe una pregunta de hasta 2.000 caracteres.": "Enter a question of up to 2,000 characters.",
 "No se pudo contactar al servidor local.": "Could not reach the local server.",
 "El servidor no devolvió una respuesta válida.": "The server did not return a valid response.",
 "No se pudo completar la operación.": "The operation could not be completed.",
 "Conectado · {model} · máximo {limit} tokens de salida": "Connected · {model} · maximum {limit} output tokens",
 "Tú": "You",
 "Comprobando acceso al modelo…": "Checking model access…",
 "Conexión comprobada. El modelo todavía no ha generado una respuesta.": "Connection checked. The model has not generated a response yet.",
 "Esperando respuesta…": "Waiting for a response…",
 "La respuesta quedó incompleta. ": "The response was incomplete. ",
 "Intentos: {used}/{limit}": "Attempts: {used}/{limit}",
 " · Tokens informados en esta solicitud: {tokens}": " · Reported tokens for this request: {tokens}",
 " No se realizó ningún reintento automático.": " No automatic retry was made.",
 "Conversación vaciada. El contador de intentos se conserva.": "Conversation cleared. The attempt count is retained.",
 "Conexión local cerrada. Si una solicitud ya llegó a OpenAI, puede terminar y generar cargos.": "Local connection closed. A request already received by OpenAI may finish and incur charges.",
 "El servidor no confirmó el cierre. Reinícialo para retirar las sesiones de su memoria.": "The server did not confirm disconnection. Restart it to remove sessions from memory.",
 "Este pedido ya tiene un recibo simulado.": "This order already has a simulated receipt.",
 "El pedido no fue entregado.": "The order has not been delivered.",
 "La solicitud no es válida.": "The request is invalid.",
 "La propuesta no está disponible.": "The proposal is unavailable.",
 "Se necesita el rol de revisor.": "The reviewer role is required.",
 "La decisión no es válida.": "The decision is invalid.",
 "Pendiente de aprobación": "Pending approval",
 "Bloqueado": "Blocked",
 "Consulta": "Read-only",
 "Aprobado": "Approved",
 "Rechazado": "Rejected",
 "Simulado": "Simulated",
 "Antes": "Before",
 "Después": "After",
 "Solicitud": "Request",
 "Decisión": "Decision",
 "Ejecución": "Execution",
 "Comprobando": "Checking",
 "Reintento sin duplicado": "Replay without duplicate",
 "Entregado": "Delivered"
};
 Object.assign(english,{"Escribe un encargo de entre 20 y 3.000 caracteres.": "Write a brief between 20 and 3,000 characters.", "Autoriza la solicitud antes de usar OpenAI.": "Authorize this request before using OpenAI.", "El contexto supera el límite. Reduce el encargo o inicia una pestaña nueva.": "Context exceeds the limit. Shorten the brief or start a new tab.", "El modelo agotó la salida. Revisa el límite de tokens antes de reintentar.": "The model reached the output limit. Review the token limit before retrying.", "La respuesta no cumple el formato del rol. No se guardó un entregable.": "The response does not match the role format. No deliverable was saved.", "Retira las credenciales del encargo o la documentación.": "Remove credentials from the brief or documentation.", "La salida contiene posibles credenciales y fue bloqueada.": "The output contains possible credentials and was blocked.", "Context7 requiere una clave válida.": "Context7 requires a valid key.", "Context7 informó un límite de uso.": "Context7 reported a rate limit.", "La conexión MCP caducó. Conecta de nuevo.": "The MCP connection expired. Connect again.", "No se completó la conexión MCP. No hubo reintento automático.": "The MCP connection failed. No automatic retry was made.", "Revisa la consulta. Para documentación, usa un identificador que comience con /.": "Check the query. For documentation, use an ID starting with /.", "Alcanzaste los 20 intentos de esta conexión MCP.": "You reached 20 attempts for this MCP connection.", "La conexión OpenAI caducó. Conecta de nuevo.": "The OpenAI connection expired. Connect again.", "Alcanzaste los 20 intentos de esta conexión OpenAI.": "You reached 20 attempts for this OpenAI connection.", "No se completó la operación. Consulta el código y revisa la conexión.": "The operation failed. Check the error code and connection.", "Modelo configurado: {model}. Límite de salida: {limit} tokens.": "Configured model: {model}. Output limit: {limit} tokens.", "OpenAI sin conectar. Puedes usar las plantillas locales.": "OpenAI is not connected. You can use local templates.", "Hooks: entrada · permiso · salida · evidencia": "Hooks: input · permission · output · evidence", "Plantilla local · sin modelo": "Local template · no model", "Pruebas del producto: no ejecutadas": "Product tests: not executed", "Descargar entregable (Markdown)": "Download deliverable (Markdown)", "Procesando el rol seleccionado.": "Processing the selected role.", "Entregable listo. Revisa el resultado antes de continuar.": "Deliverable ready. Review the result before continuing.", "Comprobando protocolo y herramientas MCP.": "Checking MCP protocol and tools.", "Context7 conectado. Herramientas descubiertas: {tools}": "Context7 connected. Discovered tools: {tools}", "Consultando Context7.": "Querying Context7.", "Consulta recibida con texto recortado. Intentos: {used}/20.": "Query received with truncated text. Attempts: {used}/20.", "Consulta completada. Intentos: {used}/20.": "Query completed. Attempts: {used}/20.", "Conexión MCP cerrada. La documentación consultada permanece en esta pestaña.": "MCP connection closed. Retrieved documentation remains in this tab.", "No se confirmó el cierre. Reinicia el servidor para retirar las sesiones.": "Disconnection was not confirmed. Restart the server to remove sessions.", "No se pudieron cargar los roles. Comprueba el servidor.": "Roles could not be loaded. Check the server.", "MCP sin conectar.": "MCP is not connected."});
 for(const node of document.querySelectorAll("[data-en]"))english[node.textContent.trim()]=node.dataset.en;
 const storageKey = "ai-implementation-lab.language";
 let language = "es";
 try { if(localStorage.getItem(storageKey)==="en") language="en"; } catch {}
 const translate=(source,values={}) => (language==="en" ? (Object.hasOwn(english,source) ? english[source] : source) : source)
   .replace(/\{(\w+)\}/g, (match,name)=>String(values[name] ?? match));
 // Capture only initial interface text; never inspect later user/model messages.
 const textBindings=[], attributeBindings=[], liveBindings=new Map();
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 while(walker.nextNode()){
  const node=walker.currentNode, source=node.nodeValue.trim();
  if(!source || node.parentElement.closest("script,style,#result,#chain,#chatStatus,#connectionStatus,#chatNotice,#messages"))continue;
  if(Object.hasOwn(english,source)){
   const offset=node.nodeValue.indexOf(source);
   textBindings.push({node,source,prefix:node.nodeValue.slice(0,offset),suffix:node.nodeValue.slice(offset+source.length)});
  }
 }
 for(const node of document.querySelectorAll("[aria-label],[placeholder],[title]"))
  for(const attribute of ["aria-label","placeholder","title"]){
   const source=node.getAttribute(attribute);
   if(source && Object.hasOwn(english,source))attributeBindings.push({node,attribute,source});
  }
 function renderBinding(node,parts){
  node.textContent=parts.map(part=>translate(part.source,part.values)).join("");
 }
 function bind(node,source,values={}){
  const parts=Array.isArray(source)?source:[{source,values}];
  liveBindings.set(node,parts);renderBinding(node,parts);
 }
 function render(){
  document.documentElement.lang=language;
  for(const entry of textBindings)entry.node.nodeValue=entry.prefix+translate(entry.source)+entry.suffix;
  for(const entry of attributeBindings)entry.node.setAttribute(entry.attribute,translate(entry.source));
  for(const [node,parts] of liveBindings){if(node.isConnected)renderBinding(node,parts);else liveBindings.delete(node);}
  document.getElementById("language").value=language;
 }
 function setLanguage(value){
  if(!["es","en"].includes(value))return;
  language=value;
  try{localStorage.setItem(storageKey,language);}catch{}
  render();window.dispatchEvent(new Event("languagechange"));
 }
 window.LabI18n={t:translate,bind,get language(){return language;}};
 document.getElementById("language").addEventListener("change",event=>setLanguage(event.target.value));
 render();
})();
