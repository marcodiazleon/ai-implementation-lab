"""R43a / D39: the Git revision a page was produced from, and fixed commits for historical records.

The build and the local server add these fields to the status data; web/evidence.js opens repository
files at `revision`, or at `pins[case_id]` for a case that cites a dated record. Without Git (an exported archive or a
shallow clone), the fields say so and the view falls back to the recorded revision or to live main.
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _git(root, *args):
    try:
        result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() if result.returncode == 0 else None

ACCEPTANCE = "specs/001-support-demo/acceptance.csv"

def historical_cases(root=ROOT):
    """Case ID to (evidence path, CSV line) for rows that cite a dated record instead of this run."""
    from scripts.check_evidence import acceptance_rows
    lines = {line.split(",", 1)[0]: line for line in (root / ACCEPTANCE).read_text(encoding="utf-8").splitlines()}
    cases = {}
    for row in acceptance_rows(root / ACCEPTANCE):
        path = row["evidence"]
        if re.fullmatch(r"[\w.-]+(/[\w.-]+)+", path) and not path.startswith("evidence/") and (root / path).is_file():
            cases[row["case_id"]] = (path, lines.get(row["case_id"], ""))
    return cases

def revision_info(root=ROOT):
    revision = _git(root, "rev-parse", "HEAD")
    if revision is None:
        return {"revision": None, "revision_dirty": None, "pins": {}, "pins_complete": False}
    dirty = bool(_git(root, "status", "--porcelain", "--untracked-files=no"))
    shallow = _git(root, "rev-parse", "--is-shallow-repository") == "true"
    # A historical case opens its file at the commit that recorded the case as it reads now, where the
    # cited report or entry exists in the version the record refers to.
    cases, pins = historical_cases(root), {}
    for case, (path, line) in ({} if shallow else cases).items():
        commits = (_git(root, "log", "--format=%H", "-S", line, "--", ACCEPTANCE) or "").splitlines() if line else []
        if not commits:
            continue
        if _git(root, "cat-file", "-e", commits[0] + ":" + path) is not None:
            pins[case] = commits[0]
            continue
        # The row was recorded before its report was committed: use the commit that added the report.
        added = (_git(root, "log", "--diff-filter=A", "--format=%H", "--", path) or "").splitlines()
        if added and _git(root, "merge-base", "--is-ancestor", commits[0], added[-1]) is not None:
            pins[case] = added[-1]
    return {"revision": revision, "revision_dirty": dirty, "pins": pins, "pins_complete": len(pins) == len(cases)}

def status_payload(root=ROOT):
    """docs/project-status.json plus what this checkout is: fingerprints (R42), revision and pins (R43)."""
    import json
    from scripts.check_evidence import record_fingerprint, source_fingerprint
    status = json.loads((root / "docs/project-status.json").read_text(encoding="utf-8"))
    return dict(status, source_fingerprint=source_fingerprint(root), record_fingerprint=record_fingerprint(root),
                **revision_info(root))
