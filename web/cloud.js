"use strict";
(() => {
 const el = id => document.getElementById(id);
 const views = ["demo","chat","connection","method"];
 function route(focus=false) {
  const hash=location.hash.slice(1), view=views.includes(hash)?hash:"demo";
  document.querySelectorAll("[data-panel]").forEach(node=>{node.hidden=node.dataset.panel!==view;});
  document.querySelectorAll("[data-view]").forEach(node=>{
   if(node.dataset.view===view)node.setAttribute("aria-current","page");else node.removeAttribute("aria-current");
  });
  if(focus && !["workspace","trace"].includes(hash)){
   const title=el("view-"+view).querySelector("h1");title.tabIndex=-1;title.focus();
  }
 }
 addEventListener("hashchange",()=>route(true));route();
 let session=null, busy=false, generation=0;
 const errors={
 CONSENT_REQUIRED:"Confirma la autorización antes de conectar.", INVALID_KEY_FORMAT:"Revisa el formato de la clave.",
 INVALID_MODEL:"Revisa el identificador del modelo.", API_KEY_REJECTED:"OpenAI rechazó la clave.",
 API_ACCESS_DENIED:"Tu proyecto no tiene acceso a este recurso.", MODEL_UNAVAILABLE:"El modelo no está disponible para esta clave.",
 API_LIMIT:"OpenAI informó un límite de uso. Revisa tu cuenta antes de reintentar.",
 API_FAILURE:"OpenAI no completó la solicitud. El modelo puede no admitir estos parámetros.",
 API_CONNECTION_FAILED:"No se completó la conexión. No se reintentó automáticamente.",
 API_NO_TEXT:"La API no devolvió texto utilizable. Revisa el modelo y el límite de salida.",
 API_RESPONSE_TOO_LARGE:"La respuesta excedió el tamaño permitido.",
 SESSION_EXPIRED:"La conexión caducó o se cerró. Conecta de nuevo.",
 SESSION_CAPACITY:"Hay demasiadas sesiones locales. Espera su caducidad o reinicia el servidor.",
 SESSION_REQUEST_LIMIT:"Alcanzaste los 20 intentos de esta conexión. Revisa tu uso antes de volver a conectar.",
 REQUEST_IN_PROGRESS:"Ya hay una solicitud en curso.", INVALID_MESSAGE:"Escribe una pregunta de hasta 2.000 caracteres."
 };
 async function request(action, body) {
  let response;
  try {response=await fetch("/api/cloud/"+action,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});}
  catch {throw new Error("No se pudo contactar al servidor local.");}
  let data;
  try {data=await response.json();}catch {throw new Error("El servidor no devolvió una respuesta válida.");}
  if(!response.ok){const err=new Error(errors[data.error]||"No se pudo completar la operación.");err.code=data.error;throw err;}
  return data;
 }
 function controls(){
  el("connectApi").disabled=busy||!!session;
  for(const id of ["apiKey","apiModel","tokenLimit","apiConsent"])el(id).disabled=busy||!!session;
  el("sendQuestion").disabled=busy||!session;el("clearChat").disabled=busy||!session;el("question").disabled=busy||!session;
  el("disconnectApi").disabled=!session;el("disconnectChat").disabled=!session;
  el("chatStatus").textContent=session?"Conectado · "+session.model+" · máximo "+session.max_output_tokens+" tokens de salida":"Sin conexión. Configura tu clave y modelo en Conexión API.";
 }
 function message(role,text){
  const node=document.createElement("article");node.className="message";node.dataset.role=role;
  const label=document.createElement("strong");label.textContent=role==="user"?"Tú":"OpenAI";
  const content=document.createElement("p");content.textContent=text;node.append(label,content);el("messages").append(node);
  el("messages").scrollTop=el("messages").scrollHeight;
 }
 el("connectionForm").onsubmit=async event=>{
  event.preventDefault();if(busy||session)return;
  busy=true;const attempt=++generation;controls();el("connectionStatus").textContent="Comprobando acceso al modelo…";
  const body={api_key:el("apiKey").value.trim(),model:el("apiModel").value.trim(),max_output_tokens:Number(el("tokenLimit").value),consent:el("apiConsent").checked};
  el("apiKey").value="";
  try {
   const result=await request("connect",body);
   if(attempt!==generation)return;
   session=result;el("messages").replaceChildren();el("chatNotice").textContent="";
   el("connectionStatus").textContent="Conexión comprobada. El modelo todavía no ha generado una respuesta.";
   location.hash="chat";
  }catch(error){el("connectionStatus").textContent=error.message;}
  finally{body.api_key="";if(attempt===generation){busy=false;controls();}}
 };
 el("chatForm").onsubmit=async event=>{
  event.preventDefault();if(busy||!session)return;
  const text=el("question").value.trim();if(!text)return;
  const attempt=generation, token=session.session_id;
  busy=true;controls();message("user",text);el("question").value="";el("chatNotice").textContent="Esperando respuesta…";
  try{
   const result=await request("ask",{session_id:token,message:text});
   if(attempt!==generation)return;
   message("assistant",result.text);
   const tokens=result.usage?.total_tokens;
   el("chatNotice").textContent=(result.incomplete?"La respuesta quedó incompleta. ":"")+"Intentos: "+result.requests_used+"/"+result.request_limit+(Number.isInteger(tokens)?" · Tokens informados en esta solicitud: "+tokens:"");
  }catch(error){
   if(attempt!==generation)return;
   el("chatNotice").textContent=error.message+" No se realizó ningún reintento automático.";
   if(error.code==="SESSION_EXPIRED")session=null;
  }finally{if(attempt===generation){busy=false;controls();}}
 };
 el("clearChat").onclick=async()=>{
  if(!session||busy)return;
  const attempt=generation;busy=true;controls();
  try{await request("clear",{session_id:session.session_id});if(attempt===generation){el("messages").replaceChildren();el("chatNotice").textContent="Conversación vaciada. El contador de intentos se conserva.";}}
  catch(error){if(attempt===generation)el("chatNotice").textContent=error.message;}
  finally{if(attempt===generation){busy=false;controls();}}
 };
 async function disconnect(){
  if(!session)return;
  const token=session.session_id;generation++;session=null;busy=true;controls();
  el("messages").replaceChildren();el("question").value="";el("apiConsent").checked=false;
  const notice="Conexión local cerrada. Si una solicitud ya llegó a OpenAI, puede terminar y generar cargos.";
  el("chatNotice").textContent=notice;el("connectionStatus").textContent=notice;
  try{await request("disconnect",{session_id:token});}
  catch{const failed="El servidor no confirmó el cierre. Reinícialo para retirar las sesiones de su memoria.";el("connectionStatus").textContent=failed;el("chatNotice").textContent=failed;}
  finally{busy=false;controls();}
 }
 el("disconnectApi").onclick=disconnect;el("disconnectChat").onclick=disconnect;controls();
})();
