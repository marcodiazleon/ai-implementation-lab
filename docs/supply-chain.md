# Supply chain, inventory and analysis coverage · Cadena de suministro, inventario y cobertura de análisis

U21 · introduced in S01 1.1 · R56, D47–D48. What code this lab runs and builds with, where it comes from, how it is pinned, and which analyses run where. `python scripts/security_check.py` recomputes the inventory and the pins on every verification; this page is checked against that output by tests, so it cannot drift silently.

## Runtime and build inventory · Inventario

| Component | Content | Source | Pinning |
|---|---|---|---|
| Python | Standard library only (3.11 or later; CI runs 3.11 and 3.13) | python.org distribution installed by the operator or `actions/setup-python` | No third-party package; a package manifest or a non-stdlib import fails the security check until a decision records it |
| Node | `node --check` over the interface scripts in CI (Node 22); optional browser scripts under `scripts/browser/` | nodejs.org distribution via `actions/setup-node`, or the implementer's environment | No package manifest; Playwright is not a repository dependency and is installed separately by whoever reruns the browser checks |
| GitHub Actions | Seven actions, listed below | github.com/actions, official upstream | Full commit SHA with the version in a comment |
| Runner images | `ubuntu-latest`, `windows-latest` | GitHub-hosted | GitHub's own rotation; not pinned (recorded as a limit) |

Standard-library modules imported by `src`, `scripts`, `run.py` and `tests` (computed): `argparse`, `ast`, `concurrent`, `contextlib`, `copy`, `csv`, `dataclasses`, `datetime`, `hashlib`, `html`, `http`, `io`, `json`, `os`, `pathlib`, `platform`, `re`, `secrets`, `shutil`, `socket`, `stat`, `subprocess`, `sys`, `tempfile`, `threading`, `time`, `unittest`, `urllib`, `uuid`. Inside `src/lab` the static rules forbid `subprocess`, `socket`, `urllib.request` and any network call other than `http.client.HTTPSConnection` to the three fixed hosts.

## GitHub Actions pinned by commit · Acciones fijadas por commit

Resolved on 2026-10-12 with `git ls-remote --tags https://github.com/<owner>/<action>.git`: each pin is the commit the floating major tag pointed to that day, so CI behavior is unchanged. Anyone can verify a row with the same command (the tag is lightweight, so the listed SHA is the commit).

| Action | Pinned commit | Tag that day | Maintainer |
|---|---|---|---|
| `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` | 11d5960a326750d5838078e36cf38b85af677262 | v4 = v4.4.0 | GitHub (actions org) |
| `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065` | a26af69be951a213d495a4c3e4e4022e16d87065 | v5 = v5.6.0 | GitHub (actions org) |
| `actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020` | 49933ea5288caeca8642d1e84afbd3f7d6820020 | v4 = v4.4.0 | GitHub (actions org) |
| `actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02` | ea165f8d65b6e75b540449e92b4886f43607fa02 | v4 = v4.6.2 | GitHub (actions org) |
| `actions/upload-pages-artifact@56afc609e74202658d3ffba0e8f6dda462b719fa` | 56afc609e74202658d3ffba0e8f6dda462b719fa | v3 = v3.0.1 | GitHub (actions org) |
| `actions/configure-pages@983d7736d9b0ae728b81ab479565c72886d7745b` | 983d7736d9b0ae728b81ab479565c72886d7745b | v5 = v5.0.0 | GitHub (actions org) |
| `actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e` | d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e | v4 = v4.0.5 | GitHub (actions org) |

Update policy (D47): resolve the new tag with the same command, read its release notes, change the pin and the comment in the same commit, and let CI run on it. A floating tag, a missing comment, a checkout without `persist-credentials: false`, a widened top-level permission, `pull_request_target` or a `secrets.*` expression fails `scripts/security_check.py`, which runs in every matrix job before anything else. The required check names of D37 are unchanged.

## Analysis coverage · Cobertura de análisis

| Analysis | Where it runs | What it covers | What it does not cover | State |
|---|---|---|---|---|
| Static rules (`scripts/security_check.py`) | `verify.py`, every CI job | `eval`, `exec`, `compile`, `__import__`, `os.system`/`popen`/`exec*`/`spawn*`, `subprocess` with a shell, `pickle`/`marshal`/`shelve`/`yaml` imports; `subprocess`, sockets and `urllib.request` inside `src/lab`; non-TLS or non-allowlisted network destinations; syntax errors | Taint tracking, injection analysis, logic flaws: these are named rules, not a general SAST | VERIFICADO (C292, C295) |
| Inventory | `verify.py`, every CI job | Every import is standard library or local; no package manifest | Vulnerabilities in the Python or Node runtimes themselves | VERIFICADO (C293, C294) |
| Workflow rules | `verify.py`, every CI job | Pins, comments, `persist-credentials`, permissions, `pull_request_target`, `secrets.*`, gate names | The content of the pinned actions and the runner image | VERIFICADO (C290, C291) |
| Secret scan (`scripts/publication_check.py`) | pre-commit hook (staged), `verify.py`, every CI job (worktree: every tracked file and every untracked file that is not ignored, hidden directories included; only untracked ignored caches and build output are excluded) | Named formats of src/lab/sensitive.py, credential-like file names, symlinks, `.local`, artifacts | Unknown formats, high-entropy strings, encrypted or encoded secrets; a bypassed hook; without Git the scan falls back to a walk that skips hidden tool directories, which is narrower | VERIFICADO (C270–C273, C305, C311, C312) |
| External SAST: ruff 0.16.8 with the bandit-derived `S` rules | Implementer's environment only, 2026-10-12 (reports/U21_SECURITY_2026-10-12.md) | Subprocess usage, hardcoded passwords, insecure functions as ruff defines them | Not executed in CI: Marco decided on 2026-10-13 not to adopt ruff as a dependency (D60) | NO_PROBADO in CI by decision; local evidence recorded (C297) |
| Dependency audit (pip-audit, npm audit or equivalent) | Nowhere | — | There is no third-party dependency to audit; the inventory check keeps it so | NO_PROBADO: not applicable today, planned the day a dependency is recorded |
| External secret scanner (gitleaks, trufflehog, GitHub secret scanning) | Nowhere by this repository | — | GitHub's own secret scanning on public repositories is an owner-side setting without evidence here | NO_PROBADO; plan: owner confirms the repository setting (C304), the repository keeps its own named-pattern guard |
| CodeQL or another hosted SAST | Nowhere | — | Would need a workflow with its own permissions and an owner decision | NO_PROBADO; plan: owner decision, then a pinned workflow with `security-events: write` only in that job |

Failure, skipped or cancelled matrix members fail both required gates (D37), and `scripts/check_evidence.py` rejects committed evidence whose `security_check` is missing or not passing, so an analysis that did not run never reads as green. CI never authorizes publication: a green run is a precondition that Marco's decision, recorded in docs/project-status.json, still has to follow.

## Resumen en español

El laboratorio ejecuta solo la biblioteca estándar de Python (3.11 o posterior) y usa Node únicamente para comprobar la sintaxis de los scripts del navegador; no hay paquetes de terceros ni manifiestos, y un import externo o un `requirements.txt` hace fallar la comprobación de seguridad hasta que una decisión lo registre. Las siete acciones de GitHub están fijadas por SHA completo de su upstream oficial, resuelto el 2026-10-12 con `git ls-remote --tags`; el comentario conserva la versión y la política de actualización es manual y verificable con el mismo comando.

Cobertura: reglas estáticas con nombre, inventario, reglas de flujos y escaneo de secretos corren en `verify.py` y en cada trabajo de CI; una ejecución ausente o fallida nunca produce verde. ruff (reglas derivadas de bandit) se ejecutó una vez en el entorno del implementador y queda NO_PROBADO en CI porque Marco decidió el 2026-10-13 no adoptarlo (D60); la auditoría de dependencias no aplica hoy; el escáner de secretos de GitHub y CodeQL dependen de ajustes del propietario. El CI nunca autoriza la publicación.
