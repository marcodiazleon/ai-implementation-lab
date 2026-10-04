"""Small publication guard; not a comprehensive secret scanner or approval."""
import argparse
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {".git", "__pycache__", ".venv", ".runtime", ".local"}
# Split spellings keep scanner examples from triggering their own detector.
PATTERNS = [
    ("private key", re.compile(r"-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"(?:gh[pousr]_" + r"[A-Za-z0-9]{30,}|github_pat_" + r"[A-Za-z0-9_]{40,})")),
    ("local personal path", re.compile(r"[A-Za-z]:\\Users\\" + r"[^\\\s]+", re.I)),
]

def files(root=ROOT):
    return sorted(p for p in root.rglob("*") if p.is_file() and not any(x in EXCLUDED for x in p.relative_to(root).parts))

def inspect(name, data):
    findings = []
    p = Path(name)
    if ".local" in p.parts:
        findings.append("Private runtime definition cannot be published: " + name)
    if p.name == ".env" or (p.name.startswith(".env.") and p.name != ".env.example") or p.suffix.lower() in {".pem", ".pfx", ".key"}:
        findings.append("Credential-like file: " + name)
    text = data.decode("utf-8", errors="replace")
    for label, pattern in PATTERNS:
        if pattern.search(text):
            findings.append(label + " detected in " + name)
    return findings

def check(root=ROOT, staged=False):
    findings = []
    if staged:
        run = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
                             check=True, capture_output=True)
        names = [x.decode("utf-8") for x in run.stdout.split(b"\0") if x]
        for name in names:
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
    print("\n".join(findings) if findings else "Publication guard: PASS (limited checks)")
    raise SystemExit(bool(findings))
