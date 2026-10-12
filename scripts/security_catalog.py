"""R57b / D49: the control catalog, validated against code and the acceptance records.

specs/001-support-demo/security-controls.json lists each control with the code behind it, its cases and a
recorded state. The state is derived here from the records, never typed by hand into a document:
  VERIFICADO  every listed case PASS, with at least one positive and one negative or limit case
  PARCIAL     some listed case PASS, or every case PASS without both polarities
  NO_PROBADO  cases exist and none is PASS
  FUTURO      no case: the control is planned, it never counts as passed
Codex's 175-item checklist stays outside the repository; `checklist` holds its item numbers as references only.

Usage: python scripts/security_catalog.py
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.requirement_matrix import code_exists, CODE_REFERENCE

CATALOG = "specs/001-support-demo/security-controls.json"
STATES = ("VERIFICADO", "PARCIAL", "NO_PROBADO", "FUTURO")


def load(root=ROOT):
    catalog = json.loads((root / CATALOG).read_text(encoding="utf-8"))
    with (root / "specs/001-support-demo/acceptance.csv").open(encoding="utf-8", newline="") as h:
        cases = {r["case_id"]: r for r in csv.DictReader(h)}
    kinds = json.loads((root / "specs/001-support-demo/case-kinds.json").read_text(encoding="utf-8"))["cases"]
    return catalog, cases, kinds


def derive(control, cases, kinds):
    ids = control.get("cases", [])
    if not ids:
        return "FUTURO"
    statuses = [cases[c]["status"] for c in ids if c in cases]
    polarities = {kinds.get(c, {}).get("polarity") for c in ids}
    passed = [s == "PASS" for s in statuses]
    if all(passed) and "positive" in polarities and polarities & {"negative", "limit"}:
        return "VERIFICADO"
    if any(passed):
        return "PARCIAL"
    return "NO_PROBADO"


def states(root=ROOT):
    """Control id -> derived state."""
    catalog, cases, kinds = load(root)
    return {c["id"]: derive(c, cases, kinds) for c in catalog["controls"]}


def validate(root=ROOT):
    catalog, cases, kinds = load(root)
    errors, seen = [], set()
    for control in catalog["controls"]:
        cid = control.get("id", "?")
        if cid in seen:
            errors.append(f"Duplicate control id: {cid}")
        seen.add(cid)
        for field in ("id", "boundary", "control", "code", "cases", "state", "limit", "checklist"):
            if field not in control:
                errors.append(f"Control {cid} lacks {field}")
        if control.get("state") not in STATES:
            errors.append(f"Control {cid} has an unknown state: {control.get('state')}")
        for reference in control.get("code", []):
            if not isinstance(reference, str) or not CODE_REFERENCE.match(reference) or not code_exists(root, reference):
                errors.append(f"Control {cid} cites code that does not exist: {reference}")
        for case in control.get("cases", []):
            if case not in cases:
                errors.append(f"Control {cid} cites a case that does not exist: {case}")
        derived = derive(control, cases, kinds)
        if control.get("state") != derived:
            errors.append(f"Control {cid} is recorded {control.get('state')} but the records give {derived}")
    return errors


def main():
    errors = validate()
    print("\n".join(errors) if errors else "Security catalog: PASS")
    for cid, state in states().items():
        print(f"{cid}: {state}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
