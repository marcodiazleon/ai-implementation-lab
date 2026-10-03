"""Check document relationships; this is not semantic or owner acceptance."""
import ast
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["README.md", "AGENTS.md", "docs/constitution.md", "docs/decisions.md",
 "docs/notebook.md", "docs/investigacion.md", "docs/sdd-adoption.md", "docs/project-status.json",
 "docs/tools-and-capabilities.md", "docs/operations.md",
 "specs/001-support-demo/spec.md", "specs/001-support-demo/plan.md",
 "specs/001-support-demo/tasks.md", "specs/001-support-demo/acceptance.csv",
 "specs/002-expansion/spec.md", "specs/002-expansion/plan.md",
 "specs/002-expansion/tasks.md", "specs/002-expansion/acceptance.csv"]

def test_ids(root):
    ids = set()
    for p in (root / "tests").glob("test_*.py"):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for method in cls.body:
                if isinstance(method, ast.FunctionDef) and method.name.startswith("test_"):
                    ids.add(p.stem + "." + cls.name + "." + method.name)
    return ids

def validate(root=ROOT):
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append("Missing artifact: " + name)
    if errors:
        return errors
    status = json.loads((root / "docs/project-status.json").read_text(encoding="utf-8"))
    if status.get("active_spec") != "specs/001-support-demo/spec.md" or status.get("expansion_state") != "BACKLOG":
        errors.append("Active specification or backlog state changed without matching validator contract")
    spec = (root / status["active_spec"]).read_text(encoding="utf-8")
    requirements = set(re.findall(r"^\| (R\d+) \|", spec, flags=re.M))
    if requirements != {"R" + str(i).zfill(2) for i in range(1, 15)}:
        errors.append("Unexpected core requirement set")
    core = root / "specs/001-support-demo"
    with (core / "acceptance.csv").open(encoding="utf-8", newline="") as handle:
        cases = list(csv.DictReader(handle))
    seen, covered, mapped = set(), set(), set()
    known = test_ids(root)
    for case in cases:
        ident = case.get("case_id", "")
        if not ident or ident in seen:
            errors.append("Duplicate or empty case ID: " + ident)
        seen.add(ident)
        for field in ("requirement_id", "profile", "precondition", "action", "expected",
                      "observed", "status", "product_version", "environment", "authority", "test_id"):
            if not case.get(field, "").strip():
                errors.append("Missing " + field + " in " + ident)
        requirement = case.get("requirement_id")
        if requirement not in requirements:
            errors.append("Unknown requirement in " + ident)
        covered.add(requirement)
        test = case.get("test_id", "")
        if test.startswith("test_"):
            mapped.add(test)
            if test not in known:
                errors.append("Unknown test: " + test)
        if case.get("status") not in {"PASS", "FAIL", "NO_PROBADO", "BLOQUEADO", "NO_APLICA"}:
            errors.append("Invalid status: " + ident)
        if case.get("status") == "PASS" and not case.get("evidence"):
            errors.append("PASS without evidence: " + ident)
    if requirements - covered:
        errors.append("Requirements without cases: " + ",".join(sorted(requirements - covered)))
    if known - mapped:
        errors.append("Tests without acceptance mapping: " + ",".join(sorted(known - mapped)))
    tasks = (core / "tasks.md").read_text(encoding="utf-8")
    task_requirements = set(re.findall(r"\bR\d{2}\b", tasks))
    if requirements - task_requirements:
        errors.append("Requirements without task reference")
    for row in tasks.splitlines():
        if re.match(r"^\| T\d+", row):
            columns = [x.strip() for x in row.split("|")[1:-1]]
            if len(columns) != 7 or not all(columns):
                errors.append("Incomplete task fields: " + columns[0])
    expansion = root / "specs/002-expansion"
    expected = {"EXP-" + prefix + str(i).zfill(2) for prefix in ("A", "M") for i in range(1, 11)}
    definitions = set(re.findall(r"^\| (EXP-[AM]\d+) \|", (expansion / "spec.md").read_text(encoding="utf-8"), re.M))
    if definitions != expected:
        errors.append("Expansion must contain exactly the 20 researched requirements")
    with (expansion / "acceptance.csv").open(encoding="utf-8", newline="") as handle:
        future = list(csv.DictReader(handle))
    if len(future) != 20 or {r["requirement_id"] for r in future} != expected:
        errors.append("Expansion acceptance mapping differs from the 20 requirements")
    future_tasks = (expansion / "tasks.md").read_text(encoding="utf-8")
    if set(re.findall(r"^\| E-([AM]\d+) \|", future_tasks, re.M)) != {x[4:] for x in expected}:
        errors.append("Expansion tasks differ from requirements")
    for p in root.rglob("*.md"):
        if any(x in {".git", ".venv", "__pycache__"} for x in p.relative_to(root).parts):
            continue
        for target in re.findall(r"\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
            if target.startswith(("https:", "http:", "#", "mailto:")):
                continue
            target = target.split("#")[0]
            if not (p.parent / target).exists():
                errors.append("Broken local link in " + p.relative_to(root).as_posix() + ": " + target)
    return errors

def main():
    errors = validate()
    result = {"passed": not errors, "errors": errors,
              "scope": "Artifact, ID, case, task and local-link checks; not semantic or owner acceptance"}
    (ROOT / "evidence").mkdir(exist_ok=True)
    (ROOT / "evidence/sdd-check.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(main())
