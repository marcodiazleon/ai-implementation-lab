"""R56 / D48: named security rules with the standard library; not a general SAST, SCA or secret scanner.

Rules, each printed by name when it fails:
  static      ast rules over src, scripts, run.py and tests: eval, exec, compile, __import__, os.system, os.popen,
              os.exec*/spawn*, subprocess with shell=True, pickle/marshal/shelve/yaml imports; subprocess, sockets or
              urllib.request inside src/lab; non-TLS or non-allowlisted network destinations anywhere, loopback literals in tests excepted.
  inventory   every import is standard library or local; no package manifest exists (a new dependency needs a decision).
  workflows   every external action pinned to a 40-character SHA with a version comment; persist-credentials: false on
              every checkout; top-level permissions contents: read; pages/id-token write only in the deploy job;
              no pull_request_target and no secrets.* expressions; the gate job names of D37 present.
  secrets     the publication guard over the worktree (src/lab/sensitive.py patterns).
Allowances are printed, never silent. The result is embedded in evidence/latest.json by scripts/verify.py and
required by scripts/check_evidence.py, so a skipped or absent run never reads as green.

Usage: python scripts/security_check.py [--json]
"""
import argparse
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.publication_check import check as publication_findings

ALLOWED_HOSTS = {"api.openai.com", "api.anthropic.com", "mcp.context7.com"}
DANGEROUS_CALLS = {"eval", "exec", "compile", "__import__"}
DANGEROUS_ATTRS = {("os", "system"), ("os", "popen"), ("os", "execv"), ("os", "execvp"), ("os", "execl"),
                   ("os", "spawnv"), ("os", "spawnl"), ("os", "startfile")}
DANGEROUS_MODULES = {"pickle", "marshal", "shelve", "yaml", "dill", "cPickle"}
NETWORK_CALLS = {"HTTPConnection", "urlopen", "create_connection", "urlretrieve"}
# File-level allowances, each with its reason; printed on every run (D48: no silent exclusion).
ALLOWANCES = {
    "scripts/check_environment.py": "socket.connect_ex to 127.0.0.1 only: read-only port probe (U05 portable start)",
}
LOCAL_TOP_LEVEL = {"src", "scripts", "tests"}
MANIFESTS = ["requirements.txt", "requirements-dev.txt", "pyproject.toml", "setup.py", "setup.cfg", "Pipfile",
             "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"]
SCANNED = ("src", "scripts", "tests")
SHA = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses:\s*([^\s#]+)(.*)$")


def python_files(root):
    out = [root / "run.py"]
    for folder in SCANNED:
        out += sorted((root / folder).rglob("*.py"))
    return [p for p in out if p.is_file()]


def _name(node):
    """Dotted name of a call target: os.system -> ('os','system'); eval -> ('eval',)."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return tuple(reversed(parts))
    return ()


LOOPBACK = {"127.0.0.1", "localhost"}


def _loopback(call):
    """True when the first argument names the loopback address literally (tests talk to the isolated server)."""
    target = call.args[0] if call.args else None
    if isinstance(target, ast.Tuple) and target.elts:
        target = target.elts[0]
    return isinstance(target, ast.Constant) and target.value in LOOPBACK


def static_rules(root):
    errors = []
    for path in python_files(root):
        rel = path.relative_to(root).as_posix()
        in_runtime = rel.startswith("src/")
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            errors.append(f"static: {rel}:{exc.lineno}: syntax error")
            continue
        hosts = {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)
                 and re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", n.value) and "/" not in n.value and " " not in n.value}
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                full = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
                for dotted in full:
                    name = dotted.split(".")[0]
                    if name in DANGEROUS_MODULES:
                        errors.append(f"static: {rel}:{node.lineno}: import of {name} is not allowed")
                    if in_runtime and name in {"subprocess", "socket", "ftplib", "smtplib", "telnetlib"}:
                        errors.append(f"static: {rel}:{node.lineno}: {name} is not allowed inside src/lab")
                    if in_runtime and dotted.startswith("urllib.request"):
                        errors.append(f"static: {rel}:{node.lineno}: urllib.request is not allowed inside src/lab")
            if isinstance(node, ast.Call):
                name = _name(node.func)
                if name and name[-1] in DANGEROUS_CALLS and len(name) == 1:
                    errors.append(f"static: {rel}:{node.lineno}: call to {name[-1]}()")
                if len(name) >= 2 and (name[-2], name[-1]) in DANGEROUS_ATTRS:
                    errors.append(f"static: {rel}:{node.lineno}: call to {name[-2]}.{name[-1]}()")
                if name and name[0] == "subprocess" or (len(name) == 1 and name[0] in {"run", "Popen", "call", "check_output", "check_call"}):
                    for kw in node.keywords:
                        if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                            errors.append(f"static: {rel}:{node.lineno}: subprocess with shell=True")
                if name and name[-1] in NETWORK_CALLS and rel not in ALLOWANCES and not _loopback(node):
                    errors.append(f"static: {rel}:{node.lineno}: {name[-1]} is not an allowed network call (TLS to a fixed host, or loopback in tests)")
                if name and name[-1] == "HTTPSConnection":
                    target = node.args[0] if node.args else None
                    if isinstance(target, ast.Constant):
                        if target.value not in ALLOWED_HOSTS:
                            errors.append(f"static: {rel}:{node.lineno}: HTTPSConnection to {target.value!r} is outside the fixed destinations")
                    else:
                        outside = sorted(h for h in hosts if h not in ALLOWED_HOSTS)
                        if outside or not hosts:
                            errors.append(f"static: {rel}:{node.lineno}: HTTPSConnection with a non-literal host and candidates {outside or 'none'} outside the fixed destinations")
                if name and name[-1] == "connect" and in_runtime:
                    errors.append(f"static: {rel}:{node.lineno}: raw socket connect inside src/lab")
    return errors


def inventory(root):
    """Standard-library modules used, local packages and external imports (which are errors)."""
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    used, external = set(), []
    for path in python_files(root):
        rel = path.relative_to(root).as_posix()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [(a.name.split(".")[0], node.lineno) for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    continue
                names = [((node.module or "").split(".")[0], node.lineno)]
            else:
                continue
            for name, line in names:
                if name in stdlib:
                    used.add(name)
                elif name not in LOCAL_TOP_LEVEL:
                    external.append(f"inventory: {rel}:{line}: import of {name} is not standard library or local")
    manifests = [m for m in MANIFESTS if (root / m).exists()]
    errors = external + [f"inventory: package manifest present without a recorded decision: {m}" for m in manifests]
    return {"python_stdlib_modules": sorted(used), "local_packages": sorted(LOCAL_TOP_LEVEL & {p.name for p in root.iterdir()}),
            "package_manifests": manifests, "node": "syntax checks in CI and optional browser scripts under scripts/browser (Playwright is not a repository dependency)"}, errors


def workflow_rules(root):
    errors, actions = [], {}
    folder = root / ".github/workflows"
    for path in sorted(folder.glob("*.yml")) if folder.is_dir() else []:
        rel = path.relative_to(root).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        text = "\n".join(lines)
        if "pull_request_target" in text:
            errors.append(f"workflows: {rel}: pull_request_target is not allowed")
        if "secrets." in text:
            errors.append(f"workflows: {rel}: secrets.* expressions are not allowed")
        if not re.search(r"^permissions:\n  contents: read\n", text, re.M):
            errors.append(f"workflows: {rel}: top-level permissions must be exactly contents: read")
        for index, line in enumerate(lines, 1):
            match = USES.match(line)
            if not match:
                continue
            ref, rest = match.group(1), match.group(2)
            if ref.startswith("./"):
                continue
            action, _, sha = ref.partition("@")
            if not SHA.match(sha):
                errors.append(f"workflows: {rel}:{index}: {action} is not pinned to a 40-character commit SHA")
            if not re.search(r"#\s*v\d", rest):
                errors.append(f"workflows: {rel}:{index}: {action} has no version comment")
            actions[action] = sha
            if action == "actions/checkout":
                block = []
                for following in lines[index:]:
                    if re.match(r"^\s*-\s", following) or re.match(r"^  [\w-]+:", following):
                        break
                    block.append(following)
                if "persist-credentials: false" not in "\n".join(block):
                    errors.append(f"workflows: {rel}:{index}: checkout without persist-credentials: false")
        for scope in ("pages: write", "id-token: write"):
            count = text.count(scope)
            if rel.endswith("verify.yml") and count:
                errors.append(f"workflows: {rel}: {scope} is not allowed in the verification workflow")
            if rel.endswith("pages.yml") and (count != 1 or text.index(scope) < text.index("  deploy:")):
                errors.append(f"workflows: {rel}: {scope} must appear once, inside the deploy job")
    verify = folder / "verify.yml"
    if verify.is_file():
        text = verify.read_text(encoding="utf-8")
        for name in ("name: verify (ubuntu-latest)", "name: verify (windows-latest)"):
            if name not in text:
                errors.append(f"workflows: verify.yml: required check {name[6:]} missing (D37)")
    return actions, errors


def check(root=ROOT):
    errors = static_rules(root)
    inv, inventory_errors = inventory(root)
    actions, workflow_errors = workflow_rules(root)
    secret_errors = ["secrets: " + f for f in publication_findings(root)]
    errors += inventory_errors + workflow_errors + secret_errors
    return {"passed": not errors, "errors": errors,
            "allowances": [f"{path}: {reason}" for path, reason in sorted(ALLOWANCES.items())],
            "inventory": inv, "actions": actions,
            "scope": "Named rules with the standard library (static, inventory, workflows, secrets); not a general SAST, SCA or secret scanner (D48)"}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = check()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for line in result["allowances"]:
            print("allowed:", line)
        print("\n".join(result["errors"]) if result["errors"] else
              f"Security check: PASS ({len(result['inventory']['python_stdlib_modules'])} stdlib modules, {len(result['actions'])} pinned actions; {result['scope']})")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
