"use strict";
(() => {
 const el=id=>document.getElementById(id),bind=(id,s,v)=>LabI18n.bind(el(id),s,v);
 let mcp=null,mcpBusy=false,mcpGeneration=0,documentation=null;
 const errors={MCP_AUTH_REQUIRED:"Context7 requiere una clave válida.",MCP_RATE_LIMIT:"Context7 informó un límite de uso.",MCP_SESSION_EXPIRED:"La conexión MCP caducó. Conecta de nuevo.",MCP_CONNECTION_FAILED:"No se completó la conexión MCP. No hubo reintento automático.",MCP_INVALID_ARGUMENTS:"Revisa la consulta. Para documentación, usa un identificador que comience con /."};
 function errorText(e){return errors[e.code]||"No se completó la operación. Consulta el código y revisa la conexión.";}
 async function post(path,body){let response;try{response=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});}catch{throw {code:"LOCAL_CONNECTION_FAILED"};}const result=await response.json();if(!response.ok)throw {code:result.error};return result;}
 function controls(){for(const id of ["connectMcp","mcpKey","mcpConnectConsent"])el(id).disabled=mcpBusy||!!mcp;el("disconnectMcp").disabled=!mcp;el("resolveMcp").disabled=mcpBusy||!mcp;el("queryMcp").disabled=mcpBusy||!mcp;}
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
   if(tool==="query-docs"){documentation=(provenance+"\n\n"+result.text).slice(0,12000);}
   bind("mcpStatus",result.truncated?"Consulta recibida con texto recortado. Intentos: {used}/20.":"Consulta completada. Intentos: {used}/20.",{used:result.requests_used});
  }catch(error){if(gen===mcpGeneration){bind("mcpStatus",[{source:errorText(error)},{source:" ({code})",values:{code:error.code}}]);if(error.code==="MCP_SESSION_EXPIRED")mcp=null;}}
  finally{el("mcpQueryConsent").checked=false;mcpBusy=false;controls();}
 };
 el("disconnectMcp").onclick=async()=>{
  if(!mcp)return;const token=mcp.session_id;mcp=null;mcpGeneration++;mcpBusy=true;controls();el("mcpConnectConsent").checked=false;
  try{await post("/api/mcp/disconnect",{session_id:token});bind("mcpStatus","Conexión MCP cerrada. La documentación consultada permanece en esta pestaña.");}catch{bind("mcpStatus","No se confirmó el cierre. Reinicia el servidor para retirar las sesiones.");}finally{mcpBusy=false;controls();}
 };

 bind("mcpStatus","MCP sin conectar.");controls();
})();
