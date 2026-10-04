"use strict";
(() => {
 const el=id=>document.getElementById(id), t=(es,en)=>LabI18n.language==='en'?en:es;
 let session=null,busy=false,generation=0;
 const notices={};
 const providers={openai:{name:'OpenAI',host:'api.openai.com',console:'https://platform.openai.com/api-keys'},anthropic:{name:'Claude / Anthropic',host:'api.anthropic.com',console:'https://platform.claude.com/settings/keys'}};
 function note(id,es,en){notices[id]=[es,en];el(id).textContent=t(es,en);}
 const errors={CONSENT_REQUIRED:['Confirma la autorización para conectar.','Confirm authorization to connect.'],API_KEY_REJECTED:['El proveedor rechazó la clave.','The provider rejected the key.'],MODEL_UNAVAILABLE:['El modelo no está disponible para esta clave.','The model is unavailable for this key.'],SESSION_EXPIRED:['La sesión caducó. Conecta de nuevo.','The session expired. Connect again.'],SESSION_REQUEST_LIMIT:['Alcanzaste los 20 intentos. Revisa el uso antes de reconectar.','You reached 20 attempts. Review usage before reconnecting.'],API_LIMIT:['El proveedor informó un límite de uso.','The provider reported a rate limit.'],API_CONNECTION_FAILED:['No se completó la conexión. Sin reintento automático.','Connection failed. No automatic retry.'],AGENT_NOT_FOUND:['El agente ya no está disponible. Selecciona otro.','The agent is unavailable. Choose another.']};
 function error(id,e){const pair=errors[e.code]||['No se completó la operación. Revisa la configuración.','The operation failed. Check the configuration.'];note(id,pair[0]+' ('+(e.code||'CONNECTION_ERROR')+')',pair[1]+' ('+(e.code||'CONNECTION_ERROR')+')');}
 async function request(action,body){let response;try{response=await fetch('/api/cloud/'+action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});}catch{throw {code:'LOCAL_CONNECTION_FAILED'};}const result=await response.json();if(!response.ok)throw {code:result.error};return result;}
 function controls(){
  const provider=providers[session?.provider||el('apiProvider').value];
  el('connectApi').disabled=busy||!!session;
  for(const id of ['apiProvider','apiKey','apiModel','tokenLimit','apiConsent'])el(id).disabled=busy||!!session;
  for(const id of ['sendQuestion','clearChat','question'])el(id).disabled=busy||!session;
  el('chatAgent').disabled=busy;el('disconnectApi').disabled=!session;el('disconnectChat').disabled=!session;
  el('chatStatus').textContent=session?`${provider.name} · ${session.model}`:t('Conecta tu IA para empezar a conversar.','Connect your AI to start a conversation.');
  el('providerDestination').textContent=t('Destino: ','Destination: ')+provider.host;
  el('providerConsent').textContent=t('Autorizo comprobar el acceso y enviar los mensajes, el contexto reciente y el prompt del agente seleccionado a ','I authorize checking access and sending messages, recent context and the selected agent prompt to ')+provider.name+t('. Entiendo que puede generar cargos de API.','. I understand API charges may apply.');
  el('providerGuide').href=provider.console;
  window.dispatchEvent(new Event('cloudchange'));
 }
 function message(role,text){const article=document.createElement('article');article.className='message';article.dataset.role=role;const label=document.createElement('strong');LabI18n.bind(label,role==='user'?'Tú':providers[session?.provider||'openai'].name);const p=document.createElement('p');p.textContent=text;article.append(label,p);el('messages').append(article);el('messages').scrollTop=el('messages').scrollHeight;}
 el('apiProvider').onchange=()=>{el('apiConsent').checked=false;el('apiKey').value='';el('apiModel').value='';controls();};
 el('connectionForm').onsubmit=async event=>{
  event.preventDefault();if(busy||session)return;busy=true;const attempt=++generation;controls();note('connectionStatus','Comprobando el acceso al modelo…','Checking model access…');
  const body={provider:el('apiProvider').value,api_key:el('apiKey').value.trim(),model:el('apiModel').value.trim(),max_output_tokens:Number(el('tokenLimit').value),consent:el('apiConsent').checked};el('apiKey').value='';
  try{const result=await request('connect',body);if(attempt!==generation)return;session=result;el('messages').replaceChildren();note('connectionStatus','Conexión comprobada. Ya puedes conversar en Demostración.','Connection checked. You can now chat in Demonstration.');note('chatNotice','','');location.hash='demo';}
  catch(e){error('connectionStatus',e);}finally{body.api_key='';if(attempt===generation){busy=false;controls();}}
 };
 el('chatForm').onsubmit=async event=>{
  event.preventDefault();if(!session||busy)return;const text=el('question').value.trim();if(!text)return;const attempt=generation;busy=true;controls();message('user',text);el('question').value='';note('chatNotice','Esperando respuesta…','Waiting for a response…');
  try{const result=await request('ask',{session_id:session.session_id,message:text,agent_id:el('chatAgent').value});if(attempt!==generation)return;message('assistant',result.text);const stats=`${result.requests_used}/${result.request_limit} · ${result.usage?.total_tokens??'—'} tokens`;note('chatNotice',(result.incomplete?'Respuesta incompleta. ':'')+'Intentos: '+stats,(result.incomplete?'Incomplete response. ':'')+'Attempts: '+stats);}
  catch(e){if(attempt===generation){error('chatNotice',e);if(e.code==='SESSION_EXPIRED')session=null;}}
  finally{if(attempt===generation){busy=false;controls();}}
 };
 el('chatAgent').onchange=async()=>{
  if(busy)return;el('messages').replaceChildren();
  if(session){const attempt=generation;busy=true;controls();try{await request('clear',{session_id:session.session_id});}catch(e){if(attempt===generation){error('chatNotice',e);await disconnect();}return;}finally{if(attempt===generation){busy=false;controls();}}}
  note('chatNotice','Al cambiar de agente comienza un contexto nuevo. Tu borrador se conserva.','Changing agents starts a new context. Your draft is preserved.');
 };
 el('clearChat').onclick=async()=>{if(!session||busy)return;const attempt=generation;busy=true;controls();try{await request('clear',{session_id:session.session_id});if(attempt===generation){el('messages').replaceChildren();note('chatNotice','Conversación vaciada. El contador de intentos se conserva.','Conversation cleared. The attempt count is preserved.');}}catch(e){if(attempt===generation)error('chatNotice',e);}finally{if(attempt===generation){busy=false;controls();}}};
 async function disconnect(){if(!session)return;const token=session.session_id;generation++;session=null;busy=true;controls();el('messages').replaceChildren();el('apiConsent').checked=false;try{await request('disconnect',{session_id:token});for(const id of ['connectionStatus','chatNotice'])note(id,'Conexión cerrada. Las solicitudes ya enviadas pueden terminar en el proveedor.','Connection closed. Already sent requests may finish at the provider.');}catch(e){for(const id of ['connectionStatus','chatNotice'])note(id,'No se confirmó el cierre. Reinicia el servidor para retirar las sesiones.','Disconnection was not confirmed. Restart the server to remove sessions.');}finally{busy=false;controls();}}
 el('disconnectApi').onclick=disconnect;el('disconnectChat').onclick=disconnect;
 window.LabCloud={status:()=>({connected:!!session,busy,provider:session?.provider,model:session?.model})};
 addEventListener('languagechange',()=>{for(const [id,pair] of Object.entries(notices))el(id).textContent=t(...pair);controls();});
 note('connectionStatus','Sin conexión.','Not connected.');controls();
})();
