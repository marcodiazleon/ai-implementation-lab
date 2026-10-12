"""R51 / D42: the requirement matrix, generated from the records and a reviewed classification.

sdd_check verifies structure and identifiers. This script asks a different question for every active
requirement: is there a behavior-level positive case, a negative or limit case, named code that exists
and exact evidence? The answer comes from specs/001-support-demo/acceptance.csv plus
specs/001-support-demo/case-kinds.json, which classifies each case (kind and polarity) and names the
code and observable behavior of each requirement. Structural cases never count as the behavior-level
positive (R51b). Nothing is marked executed by inspection: manual cases keep their recorded status.

Usage:
  python scripts/requirement_matrix.py            validate and print gaps
  python scripts/requirement_matrix.py --write    also write docs/requirements-matrix.md
"""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.sdd_check import requirement_rows

KINDS = {"behavior", "structure", "document", "manual"}
POLARITIES = {"positive", "negative", "limit"}
VERIFICATIONS = {"code", "interface", "document", "measurement"}
ACCEPTANCE = "specs/001-support-demo/acceptance.csv"
CLASSIFICATION = "specs/001-support-demo/case-kinds.json"

def load(root=ROOT):
    with (root / ACCEPTANCE).open(encoding="utf-8", newline="") as h:
        cases = list(csv.DictReader(h))
    kinds = json.loads((root / CLASSIFICATION).read_text(encoding="utf-8"))
    requirements = requirement_rows((root / "specs/001-support-demo/spec.md").read_text(encoding="utf-8"))
    return cases, kinds, requirements

def code_exists(root, reference):
    """'path' or 'path::text': the file exists and, when given, contains the text."""
    path, _, text = reference.partition("::")
    target = root / path
    if not target.is_file():
        return False
    return not text or text in target.read_text(encoding="utf-8", errors="replace")

def classify(cases, kinds):
    rows = {}
    for case in cases:
        entry = kinds["cases"].get(case["case_id"])
        if entry is None:
            continue
        rows[case["case_id"]] = dict(case, kind=entry["kind"], polarity=entry["polarity"])
    return rows

def validate(root=ROOT):
    cases, kinds, requirements = load(root)
    errors = []
    ids = {c["case_id"] for c in cases}
    for case_id, entry in kinds["cases"].items():
        if case_id not in ids:
            errors.append(f"Classified case does not exist: {case_id}")
        if entry.get("kind") not in KINDS or entry.get("polarity") not in POLARITIES:
            errors.append(f"Invalid classification for {case_id}")
    for case_id in sorted(ids - set(kinds["cases"])):
        errors.append(f"Unclassified case: {case_id}")
    rows = classify(cases, kinds)
    for req in requirements:
        rid = req["id"]
        spec = kinds["requirements"].get(rid)
        if spec is None:
            errors.append(f"Requirement without classification: {rid}")
            continue
        if spec.get("verification") not in VERIFICATIONS or not spec.get("behavior"):
            errors.append(f"Requirement {rid} needs a verification kind and an observable behavior")
            continue
        for reference in spec.get("code", []):
            if not code_exists(root, reference):
                errors.append(f"Requirement {rid} cites code that does not exist: {reference}")
        own = [r for r in rows.values() if r["requirement_id"] == rid and r["status"] != "NO_APLICA"]
        automated = [r for r in own if r["kind"] in {"behavior", "structure", "document"}]
        behavior_positive = [r for r in own if r["kind"] == "behavior" and r["polarity"] == "positive"]
        negative = [r for r in own if r["polarity"] in {"negative", "limit"}]
        browser = [r for r in own if r["kind"] == "manual" and r["status"] == "PASS" and r["evidence"].strip()]
        kind = spec["verification"]
        if kind == "code":
            if not behavior_positive:
                errors.append(f"Requirement {rid} (code) has no behavior-level positive case")
            if not [r for r in negative if r["kind"] == "behavior"]:
                errors.append(f"Requirement {rid} (code) has no behavior-level negative or limit case")
        elif kind == "interface":
            if not automated:
                errors.append(f"Requirement {rid} (interface) has no automated case")
            if not browser:
                errors.append(f"Requirement {rid} (interface) has no passing browser case with evidence")
        elif kind == "document":
            if not [r for r in automated if r["polarity"] == "positive"]:
                errors.append(f"Requirement {rid} (document) has no automated positive case")
        elif kind == "measurement":
            if not [r for r in own if r["kind"] == "manual"]:
                errors.append(f"Requirement {rid} (measurement) has no recorded measurement case")
        for r in own:
            if r["status"] == "PASS" and not r["evidence"].strip():
                errors.append(f"Case {r['case_id']} is PASS without evidence")
    return errors

def gaps(root=ROOT):
    """Open items that are not validation errors: pending manual cases and older browser evidence."""
    cases, kinds, _ = load(root)
    rows = classify(cases, kinds)
    out = []
    for r in rows.values():
        if r["status"] in {"NO_PROBADO", "BLOQUEADO"}:
            out.append(f"{r['case_id']} ({r['requirement_id']}, {r['kind']}): {r['status']} — {r['test_id']}")
    return out

def render(root=ROOT):
    cases, kinds, requirements = load(root)
    rows = classify(cases, kinds)
    lines = ["# Requirement matrix · Matriz de requisitos", "",
             "Generated by `python scripts/requirement_matrix.py --write` from acceptance.csv and case-kinds.json (R51, D42). "
             "Do not edit by hand. Each requirement lists its observable behavior, the code behind it, its positive and "
             "negative or limit cases with kind, status and the evidence recorded for the version in the `product_version` column. "
             "Structural cases (text or markup inspection) are marked and never count as the behavior-level positive. "
             "Manual cases keep their recorded status; nothing here is marked executed by inspection.", "",
             "Kinds: behavior = executes code and checks results; structure = inspects markup, text or files; "
             "document = validator over the records; manual = a person or a recorded browser run.", ""]
    for req in requirements:
        rid = req["id"]; spec = kinds["requirements"][rid]
        own = [r for r in rows.values() if r["requirement_id"] == rid]
        lines += [f"## {rid} — {req['text']}", "",
                  f"- Source {req['source']} · {req['cu']} · verification: **{spec['verification']}**",
                  f"- Observable behavior: {spec['behavior']}",
                  "- Code: " + (", ".join("`" + c + "`" for c in spec.get("code", [])) or "—"), "",
                  "| Case | Kind | Polarity | Status | Test | Evidence | Version |", "|---|---|---|---|---|---|---|"]
        for r in own:
            lines.append(f"| {r['case_id']} | {r['kind']} | {r['polarity']} | {r['status']} | `{r['test_id']}` | {r['evidence'] or '—'} | {r['product_version']} |")
        lines.append("")
    open_items = gaps(root)
    lines += ["## Open items · Pendientes", ""] + [f"- {g}" for g in open_items] + [""]
    return "\n".join(lines)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    errors = validate()
    print("\n".join(errors) if errors else "Requirement matrix: PASS")
    if args.write and not errors:
        (ROOT / "docs/requirements-matrix.md").write_text(render(), encoding="utf-8", newline="\n")
        print("Wrote docs/requirements-matrix.md")
    for g in gaps():
        print("open:", g)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
