"""Validate synthetic fixture contracts without loading external data."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate(root=ROOT):
    orders = json.loads((root / "data/orders.json").read_text(encoding="utf-8"))
    policy = json.loads((root / "data/policy.json").read_text(encoding="utf-8"))
    errors, seen = [], set()
    for row in orders:
        expected = {"id", "workspace", "status", "days_since_delivery", "amount", "version"}
        if set(row) != expected:
            errors.append("Order fields differ from synthetic contract")
            continue
        if not isinstance(row["id"], str) or not row["id"].startswith("DEMO-") or row["id"] in seen:
            errors.append("Invalid or duplicate synthetic ID")
        seen.add(row["id"])
        if row["workspace"] not in {"sample-store", "other-store"} or row["status"] not in {"delivered", "in_transit"}:
            errors.append("Invalid synthetic classification")
        for key in ("amount", "days_since_delivery", "version"):
            if type(row[key]) is not int or row[key] < (1 if key == "version" else 0):
                errors.append("Invalid numeric field: " + key)
    if policy.get("currency") != "DEMO":
        errors.append("Only DEMO currency is permitted")
    for key in ("max_refund", "window_days"):
        if type(policy.get(key)) is not int or policy[key] < 0:
            errors.append("Invalid policy limit")
    return errors

if __name__ == "__main__":
    errors = validate()
    print(json.dumps({"passed": not errors, "errors": errors}, indent=2))
    raise SystemExit(bool(errors))
