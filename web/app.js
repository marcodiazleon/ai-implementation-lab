"use strict";
const byId=id=>document.getElementById(id);
const t=(source,values)=>LabI18n.t(source,values);
const ui=(id,source,values)=>LabI18n.bind(byId(id),source,values);
let scenarios=[], current=null, state=null;
const labels={APPROVAL_REQUIRED:"Falta aprobación humana.",ABOVE_LIMIT:"Importe por encima del límite.",
 OUTSIDE_WINDOW:"Fuera del plazo permitido.",ORDER_UNAVAILABLE:"Pedido no disponible en este espacio.",
 TOOL_NOT_ALLOWED:"Herramienta fuera del alcance permitido.",SIMULATED_CONNECTOR_FAILURE:"Fallo simulado: no se generó un recibo. Puedes reintentar.",
 STALE_PROPOSAL:"La propuesta ya no corresponde a los datos vigentes.",INVALID_TRANSITION:"Esta decisión ya no está disponible.",
 ALREADY_COMPENSATED:"Este pedido ya tiene un recibo simulado.",NOT_DELIVERED:"El pedido no fue entregado.",
 INVALID_REQUEST:"La solicitud no es válida.",PROPOSAL_UNAVAILABLE:"La propuesta no está disponible.",
 REVIEWER_REQUIRED:"Se necesita el rol de revisor.",INVALID_DECISION:"La decisión no es válida."};
const codes={PENDING_APPROVAL:"Pendiente de aprobación",BLOCKED:"Bloqueado",READ_ONLY:"Consulta",APPROVED:"Aprobado",
 REJECTED:"Rechazado",SIMULATED:"Simulado",before:"Antes",after:"Después",request:"Solicitud",decision:"Decisión",
 execute:"Ejecución",CHECKING:"Comprobando",REPLAY:"Reintento sin duplicado",delivered:"Entregado",
 in_transit:"En tránsito",returned:"Devuelto",cancelled:"Cancelado"};
const code=value=>t(codes[value]||labels[value]||String(value));
async function call(path,body){
 const response=await fetch(path,body===undefined?{}:{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
 return response.json();
}
let lastResult=null, selectionPrompt=true;
function show(result){
 lastResult=result;selectionPrompt=false;
 const reason=result.reason||result.error;
 if(reason)ui("result",labels[reason]||reason);
 else if(result.status==="PENDING_APPROVAL")ui("result","Propuesta preparada. Importe: {amount} DEMO. Espera una decisión humana.",{amount:result.amount});
 else if(result.status==="APPROVED")ui("result","Aprobada. Ahora puedes intentar la ejecución simulada.");
 else if(result.status==="REJECTED")ui("result","Rechazada. La ejecución permanecerá bloqueada.");
 else if(result.status==="SIMULATED")ui("result","Recibo simulado: {id}. No hubo operación real.",{id:result.id});
 else if(result.status==="READ_ONLY")ui("result","Consulta completada: {id} · {status}",{id:result.order?.id||"",status:code(result.order?.status||"")});
 else ui("result",JSON.stringify(result));
 byId("result").classList.toggle("blocked",!!reason);
}
function renderState(){
 if(!state)return;
 byId("receiptCount").textContent=String(state.receipts.length).padStart(2,"0");
 ui("chain",!state.events.length?"Sin operaciones":state.audit_chain_valid?"CADENA COHERENTE":"REVISAR CADENA");
 const rows=state.events.map(event=>{
  const tr=document.createElement("tr");
  for(const key of ["sequence","phase","action","outcome"]){
   const td=document.createElement("td");td.textContent=key==="sequence"?event[key]:code(event[key]);td.title=String(event[key]);tr.append(td);
  }return tr;
 });
 byId("events").replaceChildren(...rows.reverse());
 if(current){const proposal=state.proposals.find(p=>p.id===current);byId("approve").disabled=!proposal||proposal.status!=="PENDING_APPROVAL";byId("reject").disabled=byId("approve").disabled;}
}
async function refresh(){state=await call("/api/state");renderState();}
async function action(fn){
 try{await fn();await refresh();}
 catch{lastResult=null;selectionPrompt=false;ui("result","No se pudo contactar al servidor local. Comprueba que siga activo.");}
}
byId("propose").onclick=()=>action(async()=>{
 const chosen=scenarios.find(s=>s.id===byId("scenario").value);if(!chosen)return;
 const result=await call("/api/request",chosen.request);
 if(chosen.id!==byId("scenario").value)return;
 show(result);current=result.id||null;byId("decisionBox").hidden=!current;byId("execute").disabled=!current;
});
for(const decision of ["approve","reject"])byId(decision).onclick=()=>action(async()=>show(await call("/api/decision",{proposal_id:current,decision})));
byId("execute").onclick=()=>action(async()=>show(await call("/api/execute",{proposal_id:current,fail_connector:byId("failure").checked})));
function download(name,data){
 const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:"application/json"}));
 const link=document.createElement("a");link.href=url;link.download=name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
byId("export").onclick=()=>{if(state)download("demo-evidence.json",state);};
// R28: explicit reset with confirmation; the native dialog closes on Escape without changing anything.
const resetDialog=byId("resetDialog");
byId("resetSession").onclick=()=>resetDialog.showModal();
// Focus returns to the reset button explicitly; the close listener also covers Escape.
const closeReset=()=>{resetDialog.close();byId("resetSession").focus();};
byId("resetCancel").onclick=closeReset;
resetDialog.addEventListener("close",()=>byId("resetSession").focus());
async function resetSession(exportFirst){
 // state is refreshed after every action, so the download holds the evidence shown on screen.
 if(exportFirst&&state)download("demo-evidence.json",state);
 closeReset();
 await action(async()=>{await call("/api/reset",{});selection();ui("result","Sesión reiniciada.");});
}
byId("resetExport").onclick=()=>resetSession(true);
byId("resetConfirm").onclick=()=>resetSession(false);
// R29: per-condition explanation; a pure query that creates no proposal, receipt or event.
let lastExplain=null;
const conditionText={NOT_DELIVERED:"Estado del pedido: {observed} · requerido: {limit}",
 OUTSIDE_WINDOW:"Días desde la entrega: {observed} · máximo: {limit}",ABOVE_LIMIT:"Importe: {observed} DEMO · máximo: {limit} DEMO"};
function renderExplain(){
 const result=lastExplain?.result;
 byId("exportExplain").disabled=result?.status!=="EXPLAINED";
 byId("verdict").classList.toggle("blocked",!!result&&!result.eligible);
 if(!result)return ui("verdict","Pulsa Evaluar condiciones para ver el resultado de cada condición.");
 if(result.status!=="EXPLAINED"){byId("conditions").replaceChildren();ui("verdict",labels[result.reason]||result.reason||result.error);return;}
 byId("conditions").replaceChildren(...result.conditions.map(c=>{
  const li=document.createElement("li"),mark=document.createElement("span"),text=document.createElement("span");
  const shown=value=>c.rule==="NOT_DELIVERED"?code(value):value;
  li.className=c.ok?"ok":"fail";mark.setAttribute("aria-hidden","true");mark.textContent=c.ok?"✓":"✕";
  text.textContent=t(conditionText[c.rule]||c.rule,{observed:shown(c.observed),limit:shown(c.limit)})+" — "+(c.ok?t("cumple"):t("no cumple")+". "+t(labels[c.rule]||c.rule));
  li.append(mark,text);return li;
 }));
 ui("verdict",result.eligible?"Elegible para propuesta":"No elegible");
}
byId("explainForm").onsubmit=event=>{
 event.preventDefault();
 const input={amount:Number(byId("explainAmount").value),days_since_delivery:Number(byId("explainDays").value),status:byId("explainStatus").value};
 return action(async()=>{lastExplain={input,result:await call("/api/explain",input)};renderExplain();});
};
byId("exportExplain").onclick=()=>{
 const result=lastExplain?.result;if(result?.status!=="EXPLAINED")return;
 download("demo-explanation.json",{input:lastExplain.input,eligible:result.eligible,conditions:result.conditions,policy_version:result.policy_version,generated_at:new Date().toISOString()});
};
function scenarioDetail(){
 const chosen=scenarios.find(s=>s.id===byId("scenario").value);
 if(chosen)ui("scenarioDetail","{id} · resultado esperado: {status}",{id:chosen.request.order_id,status:code(chosen.expected)});
}
function selection(){
 current=null;lastResult=null;selectionPrompt=true;byId("decisionBox").hidden=true;byId("failure").checked=false;
 for(const id of ["approve","reject","execute"])byId(id).disabled=true;
 byId("result").classList.remove("blocked");ui("result","Pulsa Analizar solicitud para revisar este caso.");scenarioDetail();
}
byId("scenario").onchange=selection;
window.addEventListener("languagechange",()=>{
 for(const option of byId("scenario").options){const scenario=scenarios.find(s=>s.id===option.value);option.textContent=t(scenario.title);}
 scenarioDetail();renderState();if(lastResult)show(lastResult);renderExplain();
});
ui("result","Selecciona una solicitud para comenzar.");ui("chain","Sin operaciones");renderExplain();
action(async()=>{
 scenarios=await call("/api/scenarios");
 for(const scenario of scenarios){const option=document.createElement("option");option.value=scenario.id;option.textContent=t(scenario.title);byId("scenario").append(option);}
 selection();
});
