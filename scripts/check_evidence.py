"""R39b: the committed evidence must describe the checked-out sources (D32).

Usage:
  python scripts/check_evidence.py                     fingerprint and overall result of evidence/latest.json
  python scripts/check_evidence.py --save FILE         copy the committed evidence before a verification run
  python scripts/check_evidence.py --against FILE      compare every test status of the new run with FILE
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.publication_check import files

SOURCE_DIRS = {"src", "tests", "scripts", "data", "web"}

def source_hashes(root=ROOT):
    """Per-file SHA-256 of everything that can change a test result; scripts/verify.py records the same map."""
    hashes = {}
    for p in files(root):
        rel = p.relative_to(root).as_posix()
        if rel.split("/")[0] in SOURCE_DIRS or rel == "run.py":
            hashes[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return hashes

def source_fingerprint(root=ROOT):
    return hashlib.sha256(json.dumps(source_hashes(root), sort_keys=True).encode()).hexdigest()

def check_committed(root=ROOT):
    evidence = json.loads((root / "evidence/latest.json").read_text(encoding="utf-8"))
    errors = []
    current = source_fingerprint(root)
    if evidence.get("source_id") != current:
        changed = sorted(k for k, v in source_hashes(root).items() if evidence.get("source_sha256", {}).get(k) != v)
        removed = sorted(set(evidence.get("source_sha256", {})) - set(source_hashes(root)))
        errors.append("Committed evidence describes other sources: " + ", ".join((changed + removed)[:8]))
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
    print("\n".join(errors) if errors else "Evidence check: PASS")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
