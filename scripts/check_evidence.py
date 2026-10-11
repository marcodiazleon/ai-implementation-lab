"""R39b / R42: the committed evidence must describe the checked-out files (D32, D38).

Two manifests over disjoint file sets. Neither contains evidence/, so no file holds its own fingerprint.
  Sources: code, tests, fixtures, interface, agent roles and workflows (SOURCE_DIRS, run.py).
  Records: specs (acceptance.csv without its run-environment column), project status and ID registry.
They cover what the test suite executes and the SDD records it is checked against. Other documents
(README, docs/*.md, reports) are read by some tests but are not fingerprinted; a test that reads them
still has to pass in the run.

Usage:
  python scripts/check_evidence.py                     both fingerprints and the overall result of evidence/latest.json
  python scripts/check_evidence.py --save FILE         copy the committed evidence before a verification run
  python scripts/check_evidence.py --against FILE      compare test statuses, counts, records and cases of the new run with FILE
"""
import argparse
import csv
import hashlib
import io
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.publication_check import files

SOURCE_DIRS = {"src", "tests", "scripts", "data", "web", "agents", ".github"}
SOURCE_FILES = {"run.py"}
RECORD_DIRS = {"specs"}
RECORD_FILES = {"docs/project-status.json", "docs/id-registry.json"}
# Written by scripts/verify.py from the machine it runs on; the same run on another platform differs only here.
RUN_ENVIRONMENT_COLUMN = "environment"
CASE_FIELDS = ("requirement_id", "test_id", "expected", "status")

def _digest(value):
    return hashlib.sha256(value).hexdigest()

def _fingerprint(hashes):
    return _digest(json.dumps(hashes, sort_keys=True).encode())

def _selected(root, dirs, names):
    for p in files(root):
        rel = p.relative_to(root).as_posix()
        if rel.split("/")[0] in dirs or rel in names:
            yield rel, p

def acceptance_rows(path):
    with path.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))

def source_hashes(root=ROOT):
    """Per-file SHA-256 of the source manifest; scripts/verify.py records the same map."""
    return {rel: _digest(p.read_bytes()) for rel, p in _selected(root, SOURCE_DIRS, SOURCE_FILES)}

def record_hashes(root=ROOT):
    """Per-file SHA-256 of the record manifest. acceptance.csv is hashed as its rows without the environment column."""
    hashes = {}
    for rel, p in _selected(root, RECORD_DIRS, RECORD_FILES):
        if p.name == "acceptance.csv":
            rows = [{k: v for k, v in r.items() if k != RUN_ENVIRONMENT_COLUMN} for r in acceptance_rows(p)]
            hashes[rel] = _digest(json.dumps(rows, sort_keys=True, ensure_ascii=False).encode())
        else:
            hashes[rel] = _digest(p.read_bytes())
    return hashes

def source_fingerprint(root=ROOT):
    return _fingerprint(source_hashes(root))

def record_fingerprint(root=ROOT):
    return _fingerprint(record_hashes(root))

def case_map(path):
    """Case ID to requirement, test, expected result and status: what a reader relies on per case."""
    return {r["case_id"]: {k: r[k] for k in CASE_FIELDS} for r in acceptance_rows(path)}

def _diff(label, recorded, current):
    changed = sorted(k for k in set(recorded) | set(current) if recorded.get(k) != current.get(k))
    return [f"{label}: " + ", ".join(changed[:8]) + (f" and {len(changed) - 8} more" if len(changed) > 8 else "")] if changed else []

def check_committed(root=ROOT):
    evidence = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
    errors = []
    if evidence.get("source_id") != source_fingerprint(root):
        errors += _diff("Committed evidence describes other sources", evidence.get("source_sha256", {}), source_hashes(root))
    if "record_id" not in evidence:
        errors.append("Committed evidence has no record fingerprint")
    elif evidence["record_id"] != record_fingerprint(root):
        errors += _diff("Committed evidence describes other records", evidence.get("record_sha256", {}), record_hashes(root))
    if evidence.get("passed") is not True:
        errors.append("Committed evidence is not a passing run")
    return errors

def compare_statuses(committed, current):
    old = {r["test_id"]: r["status"] for r in committed.get("test_results", [])}
    new = {r["test_id"]: r["status"] for r in current.get("test_results", [])}
    errors = [f"Status drift: {t} {old.get(t, 'ABSENT')} -> {new.get(t, 'ABSENT')}"
              for t in sorted(set(old) | set(new)) if old.get(t) != new.get(t)]
    if committed.get("acceptance_states") != current.get("acceptance_states"):
        errors.append("Acceptance state counts drift")
    errors += _diff("Record drift", committed.get("record_sha256", {}), current.get("record_sha256", {}))
    old_cases, new_cases = committed.get("acceptance_cases", {}), current.get("acceptance_cases", {})
    for case in sorted(set(old_cases) | set(new_cases)):
        a, b = old_cases.get(case, {}), new_cases.get(case, {})
        for field in CASE_FIELDS:
            if a.get(field) != b.get(field):
                errors.append(f"Case drift: {case} {field} {a.get(field, 'ABSENT')!r} -> {b.get(field, 'ABSENT')!r}")
    return errors

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--save")
    parser.add_argument("--against")
    args = parser.parse_args(argv)
    if args.save:
        shutil.copy(ROOT / "evidence/latest.json", args.save)
    if args.against:
        errors = compare_statuses(json.loads(Path(args.against).read_text(encoding="utf-8")),
                                  json.loads((ROOT / "evidence/latest.json").read_text(encoding="utf-8")))
    else:
        errors = check_committed()
        if not errors:
            print(f"Sources {source_fingerprint()[:12]} and records {record_fingerprint()[:12]} match evidence/latest.json")
    print("\n".join(errors) if errors else "Evidence check: PASS")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
