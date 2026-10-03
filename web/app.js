"use strict";
const byId = id => document.getElementById(id);
let scenarios = [], current = null, state = null;
const labels = {APPROVAL_REQUIRED:"Falta aprobación humana.", ABOVE_LIMIT:"Importe por encima del límite.",
OUTSIDE_WINDOW:"Fuera del plazo permitido.", ORDER_UNAVAILABLE:"Pedido no disponible en este espacio.",
TOOL_NOT_ALLOWED:"Herramienta fuera del alcance permitido.", SIMULATED_CONNECTOR_FAILURE:"Fallo simulado: no se generó un recibo. Puedes reintentar.",
STALE_PROPOSAL:"La propuesta ya no corresponde a los datos vigentes.", INVALID_TRANSITION:"Esta decisión ya no está disponible."};
async function call(path, body) {
 const response = await fetch(path, body === undefined ? {} : {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
 return response.json();
}
function show(result) {
 const reason = result.reason || result.error;
 const text = reason ? (labels[reason] || reason) : ({
 PENDING_APPROVAL:"Propuesta preparada. Importe: " + result.amount + " DEMO. Espera una decisión humana.",
 APPROVED:"Aprobada. Ahora puedes intentar la ejecución simulada.",
 REJECTED:"Rechazada. La ejecución permanecerá bloqueada.",
 SIMULATED:"Recibo simulado: " + result.id + ". No hubo operación real.",
 READ_ONLY:"Consulta completada: " + (result.order?.id || "") + " · " + (result.order?.status || "")
 }[result.status] || JSON.stringify(result));
 byId("result").textContent = text;
 byId("result").classList.toggle("blocked",!!reason);
}
async function refresh() {
 state = await call("/api/state");
 byId("receiptCount").textContent = String(state.receipts.length).padStart(2,"0");
 byId("chain").textContent = state.audit_chain_valid ? "CADENA COHERENTE" : "REVISAR CADENA";
 const rows = state.events.map(event => {
  const tr = document.createElement("tr");
  for (const key of ["sequence","phase","action","outcome"]) {const td=document.createElement("td");td.textContent=event[key];tr.append(td);}
  return tr;
 });
 byId("events").replaceChildren(...rows.reverse());
 if(current) {
  const p=state.proposals.find(p=>p.id===current);
  byId("approve").disabled = !p || p.status!=="PENDING_APPROVAL";
  byId("reject").disabled = !p || p.status!=="PENDING_APPROVAL";
 }
}
async function action(fn) {
 try {await fn();await refresh();} catch {byId("result").textContent="No se pudo contactar al servidor local. Comprueba que siga activo.";}
}
byId("propose").onclick=()=>action(async()=>{
 const chosen=scenarios.find(s=>s.id===byId("scenario").value);
 const result=await call("/api/request",chosen.request);show(result);
 current=result.id || null;byId("decisionBox").hidden=!current;
});
for (const decision of ["approve","reject"]) byId(decision).onclick=()=>action(async()=>show(await call("/api/decision",{proposal_id:current,decision})));
byId("execute").onclick=()=>action(async()=>show(await call("/api/execute",{proposal_id:current,fail_connector:byId("failure").checked})));
byId("export").onclick=()=>{
 if(!state)return;
 const url=URL.createObjectURL(new Blob([JSON.stringify(state,null,2)],{type:"application/json"}));
 const link=document.createElement("a");link.href=url;link.download="demo-evidence.json";link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
function selection(){current=null;byId("decisionBox").hidden=true;byId("failure").checked=false;byId("result").classList.remove("blocked");byId("result").textContent="Pulsa Analizar solicitud para revisar este caso.";const s=scenarios.find(s=>s.id===byId("scenario").value);byId("scenarioDetail").textContent=s.request.order_id+" · resultado esperado: "+s.expected;}
byId("scenario").onchange=selection;
action(async()=>{
 scenarios=await call("/api/scenarios");
 for(const s of scenarios){const opt=document.createElement("option");opt.value=s.id;opt.textContent=s.title;byId("scenario").append(opt);}
 selection();
});
