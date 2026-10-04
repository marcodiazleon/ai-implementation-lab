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
 execute:"Ejecución",CHECKING:"Comprobando",REPLAY:"Reintento sin duplicado",delivered:"Entregado"};
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
 ui("chain",state.audit_chain_valid?"CADENA COHERENTE":"REVISAR CADENA");
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
 show(result);current=result.id||null;byId("decisionBox").hidden=!current;
});
for(const decision of ["approve","reject"])byId(decision).onclick=()=>action(async()=>show(await call("/api/decision",{proposal_id:current,decision})));
byId("execute").onclick=()=>action(async()=>show(await call("/api/execute",{proposal_id:current,fail_connector:byId("failure").checked})));
byId("export").onclick=()=>{
 if(!state)return;
 const url=URL.createObjectURL(new Blob([JSON.stringify(state,null,2)],{type:"application/json"}));
 const link=document.createElement("a");link.href=url;link.download="demo-evidence.json";link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
function scenarioDetail(){
 const chosen=scenarios.find(s=>s.id===byId("scenario").value);
 if(chosen)ui("scenarioDetail","{id} · resultado esperado: {status}",{id:chosen.request.order_id,status:code(chosen.expected)});
}
function selection(){
 current=null;lastResult=null;selectionPrompt=true;byId("decisionBox").hidden=true;byId("failure").checked=false;
 byId("result").classList.remove("blocked");ui("result","Pulsa Analizar solicitud para revisar este caso.");scenarioDetail();
}
byId("scenario").onchange=selection;
window.addEventListener("languagechange",()=>{
 for(const option of byId("scenario").options){const scenario=scenarios.find(s=>s.id===option.value);option.textContent=t(scenario.title);}
 scenarioDetail();renderState();if(lastResult)show(lastResult);
});
ui("result","Selecciona una solicitud para comenzar.");ui("chain","Sin operaciones");
action(async()=>{
 scenarios=await call("/api/scenarios");
 for(const scenario of scenarios){const option=document.createElement("option");option.value=scenario.id;option.textContent=t(scenario.title);byId("scenario").append(option);}
 selection();
});
