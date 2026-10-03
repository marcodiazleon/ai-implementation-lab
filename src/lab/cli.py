import argparse
import json
from .controller import Lab, load_data

def evaluate():
    results = []
    for scenario in load_data("scenarios.json"):
        observed = Lab().request(scenario["request"])["status"]
        results.append({"case": scenario["id"], "expected": scenario["expected"],
                        "observed": observed, "passed": observed == scenario["expected"]})
    return {"mode": "DETERMINISTIC_DEMO", "model_calls": 0, "cases": results,
            "passed": all(r["passed"] for r in results)}

def main():
    parser = argparse.ArgumentParser(description="AI Implementation Lab: synthetic and offline.")
    parser.add_argument("command", choices=["serve", "demo", "evaluate", "mcp"])
    parser.add_argument("--port", type=int, default=8765)
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
    else:
        lab = Lab()
        proposal = lab.request({"order_id": "DEMO-101", "intent": "refund"})
        lab.decide(proposal["id"], "approve", "human_reviewer")
        lab.execute(proposal["id"])
        print(json.dumps(lab.snapshot(), indent=2))
