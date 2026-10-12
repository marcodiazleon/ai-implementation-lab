"use strict";
(() => {
 const el=id=>document.getElementById(id),t=(es,en)=>LabI18n.language==='en'?en:es;
 let session=null,busy=false,generation=0,catalog=[],catalogReady=false;
 const notices={};
 const publicPreview=document.documentElement.classList.contains('public-demo');
 function openConnection(){const dialog=el('connectionDialog');if(!dialog.open)dialog.showModal();}
 el('openConnection').onclick=openConnection;
 const providers={openai:{name:'OpenAI',host:'api.openai.com',console:'https://platform.openai.com/api-keys'},anthropic:{name:'Claude / Anthropic',host:'api.anthropic.com',console:'https://platform.claude.com/settings/keys'}};
 const levels={default:['Automático','Automatic'],none:['Sin razonamiento','No reasoning'],low:['Bajo','Low'],medium:['Medio','Medium'],high:['Alto','High'],xhigh:['Muy alto','Very high'],max:['Máximo','Maximum']};
 function note(id,es,en){notices[id]=[es,en];el(id).textContent=t(es,en);}
 const errors={CONSENT_REQUIRED:['Confirma la autorización para conectar.','Confirm authorization to connect.'],API_KEY_REJECTED:['El proveedor rechazó la clave.','The provider rejected the key.'],MODEL_UNAVAILABLE:['El modelo no está disponible para esta clave.','The model is unavailable for this key.'],SESSION_EXPIRED:['La sesión caducó. Conecta de nuevo.','The session expired. Connect again.'],SESSION_REQUEST_LIMIT:['Alcanzaste los 20 intentos. Revisa el uso antes de reconectar.','You reached 20 attempts. Review usage before reconnecting.'],API_LIMIT:['El proveedor informó un límite de uso.','The provider reported a rate limit.'],API_CONNECTION_FAILED:['No se completó la conexión. Sin reintento automático.','Connection failed. No automatic retry.'],AGENT_NOT_FOUND:['El agente no está disponible. Selecciona otro.','The agent is unavailable. Choose another.'],EFFORT_UNSUPPORTED:['Este modelo no admite ese nivel de esfuerzo.','This model does not support that effort level.']};
 function error(id,e){const p=errors[e.code]||['No se completó la operación. Revisa la configuración.','The operation failed. Check the configuration.'];note(id,p[0]+' ('+(e.code||'CONNECTION_ERROR')+')',p[1]+' ('+(e.code||'CONNECTION_ERROR')+')');}
 async function request(action,body){let response;try{response=await fetch('/api/cloud/'+action,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});}catch{throw {code:'LOCAL_CONNECTION_FAILED'};}const result=await response.json();if(!response.ok)throw {code:result.error};return result;}
 const modelRow=()=>catalog.find(x=>x.provider===el('sessionProvider').value&&x.id===el('sessionModel').value);
 function effortOptions(value='default'){
  const row=modelRow(),available=['default',...(row?.efforts||[])];
  for(const id of ['sessionEffort','apiEffort']){el(id).replaceChildren();for(const v of available)el(id).append(new Option(v==='default'&&!row?.efforts.length?t('Estándar','Standard'):t(...levels[v]),v));el(id).value=available.includes(value)?value:'default';}
 }
 function renderModels(preferred){
  const provider=el('sessionProvider').value,select=el('sessionModel');select.replaceChildren();
  for(const row of catalog.filter(x=>x.provider===provider))select.append(new Option(row.name,row.id));
  if(preferred&&!catalog.some(x=>x.provider===provider&&x.id===preferred))select.append(new Option(preferred,preferred));
  if(preferred)select.value=preferred;
  el('apiModel').value=select.value;
  const list=el('modelSuggestions');list.replaceChildren();for(const row of catalog.filter(x=>x.provider===provider)){const o=document.createElement('option');o.value=row.id;o.label=row.name;list.append(o);}
  effortOptions();
 }
 function stateLayout(){const has=!!el('messages').children.length;el('view-chat').classList.toggle('has-messages',has);document.body.classList.toggle('chat-has-messages',has);}
 function controls(){
  const provider=providers[el('sessionProvider').value],row=modelRow();
  el('connectApi').disabled=publicPreview||busy||!!session;
  for(const id of ['apiProvider','apiKey','apiModel','tokenLimit','apiConsent','apiEffort'])el(id).disabled=publicPreview||busy||!!session;
  for(const id of ['sessionProvider','sessionModel','chatAgent'])el(id).disabled=busy||!catalogReady;
  el('sessionEffort').disabled=busy||!row?.efforts.length;el('apiEffort').disabled=publicPreview||busy||!!session||!row?.efforts.length;
  el('question').disabled=busy;
  el('sendQuestion').disabled=busy||!catalogReady;el('sendQuestion').type=session?'submit':'button';el('sendQuestion').textContent=busy?'…':'↑';el('sendQuestion').setAttribute('aria-label',session?t('Enviar mensaje','Send message'):t('Conectar IA','Connect AI'));el('sendQuestion').title=session?t('Enviar mensaje','Send message'):t('Conectar IA','Connect AI');
  el('clearChat').disabled=busy||!session;el('disconnectApi').disabled=busy||!session;el('disconnectChat').disabled=busy||!session;
  el('chatStatus').textContent=publicPreview?t('Vista pública','Public preview'):session?t('Conectado','Connected'):t('Sin conexión','Not connected');el('chatStatus').classList.toggle('connected',!!session);
  el('providerDestination').textContent=t('Destino: ','Destination: ')+provider.host;
  el('providerConsent').textContent=t('Autorizo comprobar acceso a los modelos que seleccione y enviar mis mensajes, contexto y prompt del agente a ','I authorize access checks for models I select and sending my messages, context and agent prompt to ')+provider.name+t('. Los mensajes pueden generar cargos de API.','. Messages may incur API charges.');el('providerGuide').href=provider.console;
  el('modelHint').textContent=(row?row.profile[LabI18n.language]:t('Modelo propio · esfuerzo estándar','Custom model · standard effort'))+(session?' · '+session.max_output_tokens+t(' tokens de salida máx.',' max output tokens'):'');
  stateLayout();window.dispatchEvent(new Event('cloudchange'));
 }
 function message(role,text){const article=document.createElement('article');article.className='message';article.dataset.role=role;const label=document.createElement('strong');label.textContent=role==='user'?t('Tú','You'):providers[session?.provider||'openai'].name;const p=document.createElement('p');p.textContent=text;article.append(label,p);el('messages').append(article);stateLayout();el('messages').scrollTop=el('messages').scrollHeight;}
 async function disconnect(){if(!session)return;const token=session.session_id;generation++;session=null;busy=true;controls();el('messages').replaceChildren();el('apiConsent').checked=false;try{await request('disconnect',{session_id:token});note('connectionStatus','Conexión cerrada.','Connection closed.');note('chatNotice','','');}catch{note('connectionStatus','No se confirmó el cierre. Reinicia el servidor para retirar la sesión anterior.','Closure was not confirmed. Restart the server to remove the previous session.');}finally{busy=false;controls();}}
 async function providerChanged(value){if(busy)return;if(session)await disconnect();el('sessionProvider').value=value;el('apiProvider').value=value;el('apiConsent').checked=false;el('apiKey').value='';renderModels();note('chatNotice','','');controls();}
 el('sessionProvider').onchange=()=>providerChanged(el('sessionProvider').value);
 el('apiProvider').onchange=()=>providerChanged(el('apiProvider').value);
 async function configure(){
  el('apiModel').value=el('sessionModel').value;el('apiEffort').value=el('sessionEffort').value;
  if(!session){controls();return;}const attempt=generation;busy=true;controls();
  try{const result=await request('configure',{session_id:session.session_id,model:el('sessionModel').value,effort:el('sessionEffort').value});if(attempt!==generation)return;session={...session,...result};if(result.history_cleared)el('messages').replaceChildren();note('chatNotice',result.history_cleared?'Modelo cambiado. Nuevo contexto; borrador conservado.':'Esfuerzo actualizado para el próximo mensaje.',result.history_cleared?'Model changed. New context; draft preserved.':'Effort updated for the next message.');}
  catch(e){if(attempt===generation){renderModels(session.model);effortOptions(session.effort);error('chatNotice',e);}}
  finally{if(attempt===generation){busy=false;controls();}}
 }
 el('sessionModel').onchange=()=>{effortOptions();configure();};
 el('sessionEffort').onchange=configure;
 el('apiModel').onchange=()=>{renderModels(el('apiModel').value.trim());controls();};
 el('apiEffort').onchange=()=>{el('sessionEffort').value=el('apiEffort').value;};
 el('sendQuestion').onclick=()=>{if(!session&&!busy)openConnection();};
 el('connectionForm').onsubmit=async event=>{
  event.preventDefault();if(publicPreview||busy||session)return;busy=true;const attempt=++generation;controls();note('connectionStatus','Comprobando acceso…','Checking access…');
  const body={provider:el('apiProvider').value,api_key:el('apiKey').value.trim(),model:el('apiModel').value.trim(),effort:el('apiEffort').value,max_output_tokens:Number(el('tokenLimit').value),consent:el('apiConsent').checked};el('apiKey').value='';
  try{const result=await request('connect',body);if(attempt!==generation)return;session=result;renderModels(result.model);effortOptions(result.effort);el('messages').replaceChildren();note('connectionStatus','Conexión comprobada. Puedes volver a Sesión.','Connection checked. You can return to Session.');note('chatNotice','','');el('connectionDialog').close();location.hash='session';}
  catch(e){if(attempt===generation)error('connectionStatus',e);}finally{body.api_key='';if(attempt===generation){busy=false;controls();}}
 };
 el('chatForm').onsubmit=async event=>{
  event.preventDefault();if(!session||busy)return;const text=el('question').value.trim();if(!text)return;const attempt=generation;busy=true;controls();message('user',text);el('question').value='';note('chatNotice','Preparando respuesta…','Preparing a response…');
  try{const result=await request('ask',{session_id:session.session_id,message:text,agent_id:el('chatAgent').value});if(attempt!==generation)return;message('assistant',result.text);const stats=`${result.requests_used}/${result.request_limit} · ${result.usage?.total_tokens??'—'} tokens`;note('chatNotice',(result.incomplete?'Respuesta incompleta. ':'')+stats,(result.incomplete?'Incomplete response. ':'')+stats);}
  catch(e){if(attempt===generation){error('chatNotice',e);if(e.code==='SESSION_EXPIRED')session=null;}}
  finally{if(attempt===generation){busy=false;controls();}}
 };
 async function clearHistory(agentChange=false){if(busy)return;if(!session){el('messages').replaceChildren();controls();return;}const attempt=generation;busy=true;controls();try{await request('clear',{session_id:session.session_id});if(attempt===generation){el('messages').replaceChildren();note('chatNotice',agentChange?'Agente cambiado. Contexto nuevo.':'Conversación vaciada. Se conserva el contador de uso.',agentChange?'Agent changed. New context.':'Conversation cleared. Usage counter is preserved.');}}catch(e){if(attempt===generation){error('chatNotice',e);if(agentChange)await disconnect();}}finally{if(attempt===generation){busy=false;controls();}}}
 el('chatAgent').onchange=()=>clearHistory(true);el('clearChat').onclick=()=>clearHistory();
 el('disconnectApi').onclick=disconnect;el('disconnectChat').onclick=disconnect;
 window.LabCloud={openConnection,status:()=>({connected:!!session,busy,provider:session?.provider,model:session?.model})};
 addEventListener('languagechange',()=>{const effort=el('sessionEffort').value;effortOptions(effort);for(const[id,pair]of Object.entries(notices))el(id).textContent=t(...pair);controls();});
 fetch('/api/model-catalog').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{catalog=data.models;catalogReady=true;renderModels();controls();}).catch(()=>note('chatNotice','No se pudo cargar el catálogo. Revisa que el servidor esté actualizado.','Could not load the catalog. Check that the server is updated.'));
 if(publicPreview){note('connectionStatus','Para conectar tu API y conversar, ejecuta la versión local desde el repositorio. Esta vista pública permite explorar los modelos y crear agentes.','Run the local version from the repository to connect your API and chat. This public preview lets you explore models and create agents.');}else{note('connectionStatus','Sin conexión.','Not connected.');}controls();

 // Animate decorative copy only. Drafts and accessible labels are never rewritten.
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),greeting=el('animatedGreeting');
 let phrase=0,position=0,erasing=false,timer;
 const phrases=()=>LabI18n.language==='en'?['Tell me what you want to solve','Let’s build something incredible','What’s the plan for today?']:['Cuéntame qué quieres resolver','Creemos algo increíble','¿Cuál es el plan de hoy?'];
 function animate(){clearTimeout(timer);const items=phrases();if(reduced.matches){greeting.textContent=items[0];return;}if(document.hidden||el('view-demo').hidden||el('question')===document.activeElement||el('question').value||el('messages').children.length){greeting.textContent=items[phrase%items.length];timer=setTimeout(animate,700);return;}const word=items[phrase%items.length];position+=erasing?-1:1;position=Math.max(0,Math.min(position,word.length));greeting.textContent=word.slice(0,position);let delay=erasing?26:55;if(position===word.length&&!erasing){erasing=true;delay=2500;}else if(position===0&&erasing){erasing=false;phrase++;delay=300;}timer=setTimeout(animate,delay);}
 function resetAnimation(){clearTimeout(timer);phrase=0;position=phrases()[0].length;erasing=false;greeting.textContent=phrases()[0];timer=setTimeout(animate,2500);}
 reduced.addEventListener('change',resetAnimation);addEventListener('languagechange',resetAnimation);resetAnimation();
})();
