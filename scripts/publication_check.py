"""Publication guard over the worktree or the staged index; named patterns, not a comprehensive scanner (R10, R54b, D45, D53).

Worktree mode with Git available scans every versioned candidate: tracked files plus untracked files that are not
ignored, hidden directories included; only untracked ignored files (caches, build output, .local) are excluded.
Without Git it falls back to a walk that skips Git internals, caches, virtual environments and hidden tool
directories (any directory whose name starts with a dot other than .github, .githooks and .agents); that fallback is
narrower and is documented as such. Staged mode inspects every staged blob and rejects staged symlinks. Both modes
read the bytes they inspect, so a file that was edited after staging is judged by its staged content.
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


def candidates(root=ROOT):
    """Versioned candidates from Git: tracked and untracked-not-ignored paths, or None when Git cannot answer (D53)."""
    try:
        tracked = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, timeout=60)
        others = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--others", "--exclude-standard"], capture_output=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if tracked.returncode or others.returncode:
        return None
    names = {x.decode("utf-8") for x in tracked.stdout.split(b"\0") + others.stdout.split(b"\0") if x}
    return sorted(root / name for name in names if (root / name).is_file() or (root / name).is_symlink())


def walk(root=ROOT):
    """Fallback without Git: every file except Git internals, caches and hidden tool directories."""
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


def files(root=ROOT):
    found = candidates(root)
    return walk(root) if found is None else found


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
