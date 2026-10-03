"""Generate case-level evidence and update observed acceptance results."""
import csv
import hashlib
import io
import json
import platform
from pathlib import Path
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_data import validate
from scripts.publication_check import check, files
from scripts.sdd_check import validate as validate_sdd
from src.lab.cli import evaluate

class CaseResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cases = []
        self.started = {}

    def startTest(self, test):
        self.started[test.id()] = time.perf_counter()
        super().startTest(test)

    def record(self, test, status, observed):
        existing = next((r for r in self.cases if r["test_id"] == test.id()), None)
        row = {"test_id": test.id(), "status": status, "observed": observed,
               "duration_seconds": round(time.perf_counter() - self.started[test.id()], 6)}
        if existing is None:
            self.cases.append(row)
        elif status != "PASS":
            existing.update(row)

    def addSuccess(self, test):
        super().addSuccess(test)
        self.record(test, "PASS", "Test assertions passed against the specified case")
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.record(test, "FAIL", "Assertion failed; inspect local runner output")
    def addError(self, test, err):
        super().addError(test, err)
        self.record(test, "FAIL", "Execution error; inspect local runner output")
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.record(test, "NO_PROBADO", "Runner skipped the case")
    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            self.record(test, "FAIL", "A subcase failed; inspect local runner output")

def git_value(*args):
    result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "UNAVAILABLE"

def main():
    input_revision = git_value("rev-parse", "HEAD")
    input_dirty = bool(git_value("status", "--porcelain"))
    environment = {"python": platform.python_version(), "os": platform.system(),
                   "machine": platform.machine(), "git": git_value("--version")}
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1, resultclass=CaseResult).run(
        unittest.defaultTestLoader.discover(str(ROOT / "tests")))
    print(stream.getvalue())
    fixture_errors, publication_errors, sdd_errors = validate(), check(), validate_sdd()
    evaluation = evaluate()
    source = {}
    for p in files():
        rel = p.relative_to(ROOT).as_posix()
        if rel.split("/")[0] in {"src", "tests", "scripts", "data", "web"} or rel == "run.py":
            source[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    source_id = hashlib.sha256(json.dumps(source, sort_keys=True).encode()).hexdigest()
    by_test = {r["test_id"]: r for r in result.cases}
    path = ROOT / "specs/001-support-demo/acceptance.csv"
    with path.open(encoding="utf-8", newline="") as h:
        reader = csv.DictReader(h)
        fields = reader.fieldnames
        cases = list(reader)
    for row in cases:
        test = row["test_id"]
        observed = by_test.get(test)
        if test.startswith("test_") and observed is None:
            observed = {"status": "NO_PROBADO", "observed": "No result from this run"}
        if test == "DOCUMENT:sdd":
            observed = {"status": "FAIL" if sdd_errors else "PASS",
                        "observed": "Structural check failed" if sdd_errors else "Required artifact and reference checks passed"}
        if observed:
            row.update(status=observed["status"], observed=observed["observed"],
                       evidence="evidence/latest.json" if test.startswith("test_") else "evidence/sdd-check.json",
                       product_version="source:" + source_id, environment=environment["os"] + " / Python " + environment["python"])
    with path.open("w", encoding="utf-8", newline="") as h:
        writer = csv.DictWriter(h, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(cases)
    spec_hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (ROOT / "specs").rglob("*") if p.is_file()}
    sdd_record = {"passed": not sdd_errors, "errors": sdd_errors,
                  "scope": "Structural checks; not semantic review or owner acceptance",
                  "source_id": source_id, "spec_sha256": spec_hashes}
    (ROOT / "evidence/sdd-check.json").write_text(json.dumps(sdd_record, indent=2) + "\n", encoding="utf-8")
    evidence = {
        "schema": 2, "generated_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Local synthetic demonstration; not product acceptance or security certification",
        "input_revision": input_revision, "input_worktree_dirty": input_dirty,
        "source_id": source_id, "environment": environment,
        "tests": {"run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                  "skipped": len(result.skipped), "passed": result.wasSuccessful()},
        "test_results": result.cases,
        "fixture_validation": {"passed": not fixture_errors, "errors": fixture_errors},
        "publication_guard": {"passed": not publication_errors, "errors": publication_errors, "scope": "Limited patterns"},
        "sdd_check": {"passed": not sdd_errors, "errors": sdd_errors},
        "scenario_evaluation": evaluation, "source_sha256": source, "spec_sha256": spec_hashes,
        "acceptance_states": {s: sum(c["status"] == s for c in cases) for s in ("PASS", "FAIL", "NO_PROBADO", "BLOQUEADO", "NO_APLICA")},
        "limitations": ["Manual acceptance retains its original evidence/version", "No LLM evaluation",
                       "No live MCP client integration", "No authenticated reviewer",
                       "No durable transaction recovery", "No external business integration"]}
    evidence["passed"] = result.wasSuccessful() and not fixture_errors and not publication_errors and not sdd_errors and evaluation["passed"]
    (ROOT / "evidence/latest.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": evidence["passed"], "tests": result.testsRun, "scenarios": len(evaluation["cases"]), "sdd_errors": sdd_errors}))
    return 0 if evidence["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
