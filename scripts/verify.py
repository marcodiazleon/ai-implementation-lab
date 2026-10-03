"""Run independent checks and write a public, environment-minimal evidence record."""
import hashlib
import io
import json
from pathlib import Path
import sys
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_data import validate
from scripts.publication_check import check, files
from src.lab.cli import evaluate

def main():
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    print(stream.getvalue())
    fixture_errors, publication_errors, evaluation = validate(), check(), evaluate()
    source = {}
    for p in files():
        rel = p.relative_to(ROOT).as_posix()
        if rel.split("/")[0] in {"src", "tests", "scripts", "data", "web"} or rel == "run.py":
            source[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    evidence = {
        "schema": 1, "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Local synthetic demonstration; not product acceptance or security certification",
        "tests": {"run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                  "skipped": len(result.skipped), "passed": result.wasSuccessful()},
        "fixture_validation": {"passed": not fixture_errors, "errors": fixture_errors},
        "publication_guard": {"passed": not publication_errors, "errors": publication_errors, "scope": "Limited file and pattern checks"},
        "scenario_evaluation": evaluation, "source_sha256": source,
        "limitations": ["No LLM evaluation", "No live MCP client integration", "No authenticated reviewer",
                        "No durable transaction recovery", "No external business integration"],
    }
    evidence["passed"] = result.wasSuccessful() and not fixture_errors and not publication_errors and evaluation["passed"]
    (ROOT / "evidence").mkdir(exist_ok=True)
    (ROOT / "evidence/latest.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": evidence["passed"], "tests": result.testsRun, "scenarios": len(evaluation["cases"])}))
    return 0 if evidence["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
