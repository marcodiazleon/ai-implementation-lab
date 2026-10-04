"use strict";
(() => {
 const el=id=>document.getElementById(id), tr=s=>LabI18n.t(s), bind=(id,s,v)=>LabI18n.bind(el(id),s,v);
 let roles=[], runs=[], failures=[], running=false, mcp=null, mcpBusy=false, mcpGeneration=0, documentation=null;
 const errors={AGENT_INVALID_BRIEF:"Escribe un encargo de entre 20 y 3.000 caracteres.",AGENT_CONSENT_REQUIRED:"Autoriza la solicitud antes de usar OpenAI.",AGENT_CONTEXT_LIMIT:"El contexto supera el límite. Reduce el encargo o inicia una pestaña nueva.",AGENT_INCOMPLETE_OUTPUT:"El modelo agotó la salida. Revisa el límite de tokens antes de reintentar.",AGENT_INVALID_OUTPUT:"La respuesta no cumple el formato del rol. No se guardó un entregable.",AGENT_SENSITIVE_INPUT:"Retira las credenciales del encargo o la documentación.",AGENT_SENSITIVE_OUTPUT:"La salida contiene posibles credenciales y fue bloqueada.",MCP_AUTH_REQUIRED:"Context7 requiere una clave válida.",MCP_RATE_LIMIT:"Context7 informó un límite de uso.",MCP_SESSION_EXPIRED:"La conexión MCP caducó. Conecta de nuevo.",MCP_CONNECTION_FAILED:"No se completó la conexión MCP. No hubo reintento automático.",MCP_INVALID_ARGUMENTS:"Revisa la consulta. Para documentación, usa un identificador que comience con /.",MCP_REQUEST_LIMIT:"Alcanzaste los 20 intentos de esta conexión MCP.",SESSION_EXPIRED:"La conexión OpenAI caducó. Conecta de nuevo.",SESSION_REQUEST_LIMIT:"Alcanzaste los 20 intentos de esta conexión OpenAI."};
 async function post(path,body){
  let response;try{response=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});}catch{throw Object.assign(new Error("LOCAL_CONNECTION_FAILED"),{code:"LOCAL_CONNECTION_FAILED"});}
  const result=await response.json();if(!response.ok)throw Object.assign(new Error(result.error),{code:result.error});return result;
 }
 function errorText(error){return errors[error.code]||"No se completó la operación. Consulta el código y revisa la conexión.";}
 function save(value,name,type){const url=URL.createObjectURL(new Blob([value],{type}));const a=document.createElement("a");a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
 function controls(){
  const cloud=window.LabCloud?.status(), model=el("agentMode").value==="openai";
  el("agentSendDetails").hidden=!model;
  el("runAgent").disabled=running||!roles.length||(model&&(!cloud?.connected||cloud.busy));
  for(const id of ["agentBrief","agentRole","agentMode","agentDocs","agentConsent","nextAgent"])el(id).disabled=running;
  bind("agentConnection",cloud?.connected?"Modelo configurado: {model}. Límite de salida: {limit} tokens.":"OpenAI sin conectar. Puedes usar las plantillas locales.",{model:cloud?.model,limit:cloud?.limit});
  el("exportAgents").disabled=!(runs.length||failures.length);
  el("connectMcp").disabled=mcpBusy||!!mcp;el("mcpKey").disabled=mcpBusy||!!mcp;el("mcpConnectConsent").disabled=mcpBusy||!!mcp;
  el("disconnectMcp").disabled=!mcp;el("resolveMcp").disabled=mcpBusy||!mcp;el("queryMcp").disabled=mcpBusy||!mcp;
 }
 function renderRoles(){
  const selected=el("agentRole").value,lang=LabI18n.language;
  el("agentRole").replaceChildren();el("agentCards").replaceChildren();
  roles.forEach((role,index)=>{const option=new Option(role.name[lang],role.id);el("agentRole").append(option);const card=document.createElement("article");card.className="panel agent-card";const n=document.createElement("span");n.className="number";n.textContent=String(index+1).padStart(2,"0");const title=document.createElement("h2");title.textContent=role.name[lang];const mission=document.createElement("p");mission.textContent=role.mission[lang];const list=document.createElement("ul");for(const text of role.obligations[lang]){const li=document.createElement("li");li.textContent=text;list.append(li);}const hook=document.createElement("small");hook.textContent=tr("Hooks: entrada · permiso · salida · evidencia");card.append(n,title,mission,list,hook);el("agentCards").append(card);});
  if(selected)el("agentRole").value=selected;
 }
 function renderRuns(){
  el("agentResults").replaceChildren();
  for(const run of [...runs].reverse()){
   const box=document.createElement("article");box.className="artifact";const title=document.createElement("h3");title.textContent=roles.find(r=>r.id===run.agent)?.name[LabI18n.language]||run.agent;
   const meta=document.createElement("p");meta.className="muted";meta.textContent=(run.mode==="local"?tr("Plantilla local · sin modelo"):"OpenAI")+" · "+tr("Pruebas del producto: no ejecutadas")+" · "+(run.usage?.total_tokens!==undefined?run.usage.total_tokens+" tokens":"");
   const pre=document.createElement("pre");pre.textContent=run.text;
   const hooks=document.createElement("p");hooks.textContent=run.hooks.map(h=>h.hook+": "+h.status).join(" · ");
   const button=document.createElement("button");button.textContent=tr("Descargar entregable (Markdown)");button.onclick=()=>save(run.text,run.filename,"text/markdown");
   box.append(title,meta,hooks,pre,button);el("agentResults").append(box);
  }
 }
 el("agentForm").onsubmit=async event=>{
  event.preventDefault();if(running)return;
  const brief=el("agentBrief").value.trim(),mode=el("agentMode").value;
  if(mode==="openai"&&!el("agentConsent").checked){bind("agentStatus",errors.AGENT_CONSENT_REQUIRED);return;}
  const latest=new Map();for(const run of runs)if(run.brief===brief)latest.set(run.agent,run);
  const artifacts=[...latest.values()].map(({agent,brief_hash,text})=>({agent,brief_hash,text}));
  const body={agent:el("agentRole").value,brief,mode,language:LabI18n.language,artifacts,documentation:el("agentDocs").checked&&documentation?documentation:"",consent:mode==="openai"&&el("agentConsent").checked};
  running=true;controls();bind("agentStatus","Procesando el rol seleccionado.");
  try{const result=mode==="openai"?await window.LabCloud.runAgent(body):await post("/api/agents/run",body);runs.push({...result,brief});renderRuns();bind("agentStatus","Entregable listo. Revisa el resultado antes de continuar.");}
  catch(error){failures.push({agent:body.agent,mode,code:error.code||"REQUEST_FAILED",created_at_utc:new Date().toISOString()});bind("agentStatus",[{source:errorText(error)},{source:" ({code})",values:{code:error.code||"REQUEST_FAILED"}}]);}
  finally{running=false;el("agentConsent").checked=false;controls();}
 };
 el("agentMode").onchange=()=>{el("agentConsent").checked=false;controls();};
 for(const id of ["agentBrief","agentRole","agentDocs"])el(id).addEventListener("input",()=>{el("agentConsent").checked=false;});
 el("nextAgent").onclick=()=>{const select=el("agentRole");select.selectedIndex=(select.selectedIndex+1)%roles.length;el("agentConsent").checked=false;};
 el("exportAgents").onclick=()=>save(JSON.stringify({runs,failures,product_tests:"NOT_EXECUTED",release_approval:false},null,2),"agent-session.json","application/octet-stream");
 el("mcpConnectForm").onsubmit=async event=>{
  event.preventDefault();if(mcpBusy||mcp)return;const gen=++mcpGeneration;const body={api_key:el("mcpKey").value.trim(),consent:el("mcpConnectConsent").checked};el("mcpKey").value="";mcpBusy=true;controls();bind("mcpStatus","Comprobando protocolo y herramientas MCP.");
  try{const result=await post("/api/mcp/connect",body);if(gen===mcpGeneration){mcp=result;bind("mcpStatus","Context7 conectado. Herramientas descubiertas: {tools}",{tools:result.tools.join(", ")});}}
  catch(error){bind("mcpStatus",[{source:errorText(error)},{source:" ({code})",values:{code:error.code}}]);}
  finally{body.api_key="";mcpBusy=false;controls();}
 };
 el("mcpQueryForm").onsubmit=async event=>{
  event.preventDefault();if(!mcp||mcpBusy)return;const tool=event.submitter?.id==="queryMcp"?"query-docs":"resolve-library-id",gen=mcpGeneration;
  const args={query:el("mcpQuery").value.trim(),[tool==="query-docs"?"libraryId":"libraryName"]:el("mcpLibrary").value.trim()};
  mcpBusy=true;controls();bind("mcpStatus","Consultando Context7.");
  try{const result=await post("/api/mcp/call",{session_id:mcp.session_id,tool,arguments:args,consent:el("mcpQueryConsent").checked});if(gen!==mcpGeneration)return;
   const provenance=JSON.stringify({source:result.source,tool,arguments:args,retrieved_at_utc:new Date().toISOString(),truncated:result.truncated});
   el("mcpResult").textContent=provenance+"\n\n"+result.text;
   if(tool==="query-docs"){documentation=(provenance+"\n\n"+result.text).slice(0,12000);el("agentDocs").checked=false;el("agentConsent").checked=false;}
   bind("mcpStatus",result.truncated?"Consulta recibida con texto recortado. Intentos: {used}/20.":"Consulta completada. Intentos: {used}/20.",{used:result.requests_used});
  }catch(error){if(gen===mcpGeneration){bind("mcpStatus",[{source:errorText(error)},{source:" ({code})",values:{code:error.code}}]);if(error.code==="MCP_SESSION_EXPIRED")mcp=null;}}
  finally{el("mcpQueryConsent").checked=false;mcpBusy=false;controls();}
 };
 el("disconnectMcp").onclick=async()=>{
  if(!mcp)return;const token=mcp.session_id;mcp=null;mcpGeneration++;mcpBusy=true;controls();el("mcpConnectConsent").checked=false;
  try{await post("/api/mcp/disconnect",{session_id:token});bind("mcpStatus","Conexión MCP cerrada. La documentación consultada permanece en esta pestaña.");}catch{bind("mcpStatus","No se confirmó el cierre. Reinicia el servidor para retirar las sesiones.");}finally{mcpBusy=false;controls();}
 };
 addEventListener("languagechange",()=>{renderRoles();renderRuns();controls();});addEventListener("cloudchange",controls);
 fetch("/api/agents").then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{roles=data;renderRoles();controls();}).catch(()=>bind("agentStatus","No se pudieron cargar los roles. Comprueba el servidor."));
 bind("mcpStatus","MCP sin conectar.");controls();
})();
