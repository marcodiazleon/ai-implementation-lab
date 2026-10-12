"""Publication guard over the worktree or the staged index; named patterns, not a comprehensive scanner (R10, R54b, D45).

Worktree mode walks every file except Git internals, caches, virtual environments and hidden tool directories
(any directory whose name starts with a dot other than .github, .githooks and .agents); .local and .runtime are
also skipped there because they never are publication candidates. Staged mode inspects every staged blob,
including those directories, and rejects staged symlinks. Both modes read the bytes they inspect, so a file that
was edited after staging is judged by its staged content.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.lab.sensitive import find_secrets, credential_file

EXCLUDED = {".git", "__pycache__", ".venv", ".runtime", ".local", "node_modules"}
HIDDEN_ALLOWED = {".github", ".githooks", ".agents"}


def files(root=ROOT):
    out = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        parts = p.relative_to(root).parts
        if any(x in EXCLUDED for x in parts):
            continue
        if any(part.startswith(".") and part not in HIDDEN_ALLOWED for part in parts[:-1]):
            continue
        out.append(p)
    return sorted(out)


def inspect(name, data):
    findings = []
    parts = Path(name).parts
    if ".local" in parts:
        findings.append("Private runtime definition cannot be published: " + name)
    if credential_file(name):
        findings.append("Credential-like file: " + name)
    text = data.decode("utf-8", errors="replace")
    for label in find_secrets(text):
        findings.append(label + " detected in " + name)
    return findings


def staged_entries(root):
    run = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                         check=True, capture_output=True)
    return [x.decode("utf-8") for x in run.stdout.split(b"\0") if x]


def check(root=ROOT, staged=False):
    findings = []
    if staged:
        for name in staged_entries(root):
            entry = subprocess.run(["git", "-C", str(root), "ls-files", "-s", "--", name], capture_output=True, check=True).stdout
            if entry.startswith(b"120000"):
                findings.append("Staged symlink: " + name)
                continue
            data = subprocess.run(["git", "-C", str(root), "show", ":" + name], check=True, capture_output=True).stdout
            findings.extend(inspect(name, data))
    else:
        for p in files(root):
            name = p.relative_to(root).as_posix()
            if p.is_symlink():
                findings.append("Symlink: " + name)
            else:
                findings.extend(inspect(name, p.read_bytes()))
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    findings = check(staged=args.staged)
    print("\n".join(findings) if findings else "Publication guard: PASS (named patterns only; see src/lab/sensitive.py)")
    raise SystemExit(bool(findings))
