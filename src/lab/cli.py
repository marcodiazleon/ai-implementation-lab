import argparse
import json
import sys
from .controller import Lab, load_data
from .models import RuleError

def evaluate():
    results = []
    for scenario in load_data("scenarios.json"):
        observed = Lab().request(scenario["request"])["status"]
        results.append({"case": scenario["id"], "expected": scenario["expected"],
                        "observed": observed, "passed": observed == scenario["expected"]})
    return {"mode": "DETERMINISTIC_DEMO", "model_calls": 0, "cases": results,
            "passed": all(r["passed"] for r in results)}

# U17 / R35b: the refund case as a local walkthrough (U13 keeps it out of the visible app).
TOUR_TEXT = {
    "es": {"title": "Recorrido determinista: solicitud de devolución ficticia (sin modelo, sin dinero real)",
           "steps": ["Analizar el pedido elegible DEMO-101: el laboratorio genera una propuesta simulada",
                     "Intentar ejecutar sin aprobación", "Aprobar como revisor", "Ejecutar con fallo simulado del conector",
                     "Reintentar la ejecución", "Repetir la ejecución"],
           "controls": ["Reglas de elegibilidad y una sola propuesta por pedido y política (R01, R02)",
                        "Ninguna acción sin aprobación humana (R03)", "Decisión explícita del revisor (R03)",
                        "Un fallo no crea recibo y conserva la aprobación (R06)",
                        "El reintento crea exactamente un recibo simulado (R05)", "Repetir devuelve el mismo recibo (R05)"],
           "receipts": "Recibos simulados", "chain": "Cadena de auditoría válida", "reset": "Cada ejecución usa un laboratorio nuevo en memoria; no hay estado que limpiar.",
           "limits": "Límites: datos ficticios, recibo local simulado, revisor sin autenticación real, estado solo en memoria."},
    "en": {"title": "Deterministic walkthrough: fictional refund request (no model, no real money)",
           "steps": ["Analyze eligible order DEMO-101: the lab generates a simulated proposal",
                     "Try to execute without approval", "Approve as reviewer", "Execute with a simulated connector failure",
                     "Retry the execution", "Repeat the execution"],
           "controls": ["Eligibility rules and one proposal per order and policy (R01, R02)",
                        "No action without human approval (R03)", "Explicit reviewer decision (R03)",
                        "A failure creates no receipt and keeps the approval (R06)",
                        "The retry creates exactly one simulated receipt (R05)", "Repeating returns the same receipt (R05)"],
           "receipts": "Simulated receipts", "chain": "Audit chain valid", "reset": "Every run uses a fresh in-memory lab; there is no state to clear.",
           "limits": "Limits: fictional data, simulated local receipt, reviewer without real authentication, memory-only state."},
}

def tour():
    """Run the six tour steps in a fresh Lab and record the receipt count right after each one."""
    lab = Lab()
    pid = None
    def attempt(fn):
        try:
            return fn()
        except RuleError as exc:
            return {"status": "BLOCKED", "reason": exc.code}
    actions = [lambda: lab.request({"order_id": "DEMO-101", "intent": "refund"}),
               lambda: lab.execute(pid),
               lambda: lab.decide(pid, "approve", "human_reviewer"),
               lambda: lab.execute(pid, fail_connector=True),
               lambda: lab.execute(pid),
               lambda: lab.execute(pid)]
    steps = []
    for index, action in enumerate(actions):
        outcome = attempt(action)
        if index == 0:
            pid = outcome["id"]
        steps.append({"step": index + 1, "result": outcome.get("reason") or outcome.get("status"),
                      "receipts": len(lab.receipts),
                      "receipt_id": outcome.get("id") if outcome.get("status") == "SIMULATED" else None})
    snapshot = lab.snapshot()
    return {"mode": "DETERMINISTIC_DEMO", "model_calls": 0, "real_effects": 0, "steps": steps,
            "audit_chain_valid": snapshot["audit_chain_valid"], "proposal_status": snapshot["proposals"][0]["status"]}

def print_tour(language="es"):
    text, result = TOUR_TEXT[language], tour()
    print(text["title"])
    for row, step, control in zip(result["steps"], text["steps"], text["controls"]):
        receipt = f" | {row['receipt_id']}" if row["receipt_id"] else ""
        print(f"{row['step']}. {step}\n   -> {row['result']} | {text['receipts']}: {row['receipts']}{receipt}\n   {control}")
    print(f"{text['chain']}: {result['audit_chain_valid']}\n{text['reset']}\n{text['limits']}")
    return result

def main():
    parser = argparse.ArgumentParser(description="AI Implementation Lab: synthetic and offline.")
    parser.add_argument("command", choices=["serve", "demo", "evaluate", "mcp", "tour"])
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--lang", choices=["es", "en"], default="es")
    args = parser.parse_args()
    if args.command == "serve":
        from .server import serve
        serve(args.port)
    elif args.command == "mcp":
        from .mcp_server import serve
        serve()
    elif args.command == "evaluate":
        result = evaluate()
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result["passed"] else 1)
    elif args.command == "tour":
        # R41a: ASCII separators, and a console that cannot encode an accent gets "?" instead of a traceback.
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(errors="replace")
        print_tour(args.lang)
    else:
        lab = Lab()
        proposal = lab.request({"order_id": "DEMO-101", "intent": "refund"})
        lab.decide(proposal["id"], "approve", "human_reviewer")
        lab.execute(proposal["id"])
        print(json.dumps(lab.snapshot(), indent=2))
