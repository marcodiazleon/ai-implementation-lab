# Security runbook · Guía de operación de seguridad

U21 · introduced in S01 1.1 · R58, D49. Who does what when something goes wrong in this lab, how patches and reports are handled, and which settings still need the owner's evidence. Nothing here enables a setting, invents a contact or describes a real incident; the only exercise is the synthetic drill at the end.

Owner of every decision below: Marco Díaz de León. Implementer: the assistant named in docs/project-status.json, acting only within an authorized increment. Reviewer: Codex, when Marco asks for an independent review.

## Reporting · Reporte

Contact: Marco's public GitHub profile is the only address this repository publishes; ask there for a private channel before sending any detail, and do not open a public issue with sensitive content. The profile is a public contact, not evidence of an operative private channel: until GitHub's private vulnerability reporting or another private route is confirmed by the owner, this step is a request for one. GitHub's private vulnerability reporting is a repository setting that may or may not be enabled; its state is NO_PROBADO here until the owner records read-only evidence (C304). Never include a real key, a real customer or personal data in a report; a synthetic reproduction is enough.

## Severity · Severidad

| Severity | Examples in this lab | Owner | First response | Resolution target |
|---|---|---|---|---|
| S1 critical | A real credential committed or published; CI permissions widened; the public site serving tampered code | Marco | Same day: revoke, remove from the published revision, record | 3 days: ordinary commit on main, new Pages run, notebook entry |
| S2 high | The local server accepting requests from another origin or host; a guard that lets a named credential format through; an action pin pointing to unverified code | Marco decides, implementer fixes | 2 days | 7 days |
| S3 medium | A limit not enforced (body size, timeout, concurrency, budget); a document that overstates a control | Implementer | 7 days | Next increment |
| S4 low | Wording, a missing case in the catalog, a stale pin comment | Implementer | Next increment | Next increment |

## Patch policy · Política de parches

- Python and Git are installed by the operator from their official distributions; the README states 3.11 or later. A security release of Python is adopted by updating the version used in CI and the README in the same commit.
- GitHub Actions: pins are updated by hand after resolving the upstream tag (docs/supply-chain.md); the comment carries the version. A security advisory on an action is S2.
- The lab has no third-party package. The day one is recorded by a decision, this policy gains a dependency audit step before it is merged.
- Fixes are ordinary commits on a branch, verified by `python scripts/verify.py` twice, reviewed, and merged by Marco; history is never rewritten.

## Detection · Detección

- Pre-commit hook over staged bytes (`.githooks/pre-commit`); `python scripts/publication_check.py --staged` by hand before a release.
- `python scripts/security_check.py` in every verification and CI job: static rules, inventory, workflow pins and permissions, worktree secrets.
- `python scripts/check_evidence.py` on every CI job: committed evidence must describe the exact sources and carry a passing security check.
- The Evidence view and `/api/status`: a build whose content differs from the accepted or published revision says so.
- GitHub notifications on pushes, pull requests and workflow runs; the owner reads them, nothing is automated.

## Containment · Contención

- Credential exposure: disconnect the session (the key reference is emptied), stop the server (Ctrl+C clears process memory references), and treat the credential as compromised regardless. An idle session is pruned when another operation is served after 30 minutes, not at the exact minute, so disconnecting or stopping is the action, never waiting.
- A commit with sensitive content on a branch: do not push; remove the content with a new commit and run the staged guard; if it was pushed, go to Revocation and then remove it from the published revision with an ordinary commit (history stays, the secret is revoked).
- A suspicious pull request or action change: do not merge; CI must stay red on it (the security check fails on floating tags and widened permissions).
- A suspected exposure of the local server to a network: stop it; it is loopback-only by construction and has no authentication.

## Revocation · Revocación

- Provider keys: revoke and recreate them in the OpenAI or Anthropic console; Context7 keys in its dashboard. The lab stores none of them, so nothing has to be cleaned locally except `.local/agents.json` if a key was pasted into a definition (the store rejects named formats, but review it anyway).
- GitHub tokens or deploy credentials: `persist-credentials: false` means the workflows keep none; a leaked personal token is revoked in the GitHub settings by its owner.
- Sessions of the local server: `POST /api/cloud/disconnect` and `/api/mcp/disconnect`, or stop the server.

## Recovery · Recuperación

- Source: `git revert` of the offending commit (never a force push) and a new verification run; the published site follows the next push to main through the Pages workflow, which Marco authorizes.
- Records: regenerate evidence with `python scripts/verify.py` twice and compare with `python scripts/check_evidence.py --against`; update the acceptance case that caught the failure.
- Local state: restart the server; there is no durable state except `.local/agents.json`.
- Rollback of a bad publication: revert on main and let the Pages workflow deploy the reverted revision; the deployment record in docs/project-status.json is updated with the new run.

## Follow-up · Seguimiento

- Record the event in docs/notebook.md with date, revision, what was detected, what was done and what remains; link the acceptance case.
- Add or correct the control in specs/001-support-demo/security-controls.json and the case in acceptance.csv; the catalog state follows the records.
- Review whether the named patterns, limits or rules need a change; a new pattern is a code change with a negative test, never a note.
- No scheduled process is implied: the owner decides when to revisit.

## Pending owner evidence · Evidencia pendiente del propietario

The following are settings of the owner's accounts and providers. The implementer cannot read or change them, and this repository records them as NO_PROBADO until Marco supplies read-only evidence (a screenshot or an exported setting without credentials): two-factor authentication on the GitHub account, branch protection on main (the required check names of D37 are known, the protection itself is not verified here), private vulnerability reporting, GitHub secret scanning on the repository, the Pages source and custom domain settings, and provider-side spending limits on the API keys. Owner decision 2026-10-13: Marco enables private vulnerability reporting and GitHub secret scanning, confirms two-factor authentication and the protection of main, and sends read-only evidence; until it is recorded these stay NO_PROBADO and the contact route stays his public profile.

## Synthetic drill DRILL-2026-10-12-01 · Simulacro sintético

Scenario (fictional, no real key involved): an operator pastes a provider key into an agent brief, saves a note with it, types it into a custom agent definition and wants to export that definition. The technical steps are executed by `tests/test_u21.py::CatalogTests.test_synthetic_incident_drill` against fakes and a temporary repository on every verification run:

1. Detection: the executor rejects the brief with AGENT_SENSITIVE_INPUT (C274); the store rejects the definition with AGENT_SENSITIVE_INPUT, so there is nothing to export (C274, C276).
2. Containment: the pre-commit hook blocks the staged note naming the format (C273); the worktree guard names the file.
3. Revocation: the local session is disconnected and its key reference emptied (C277); the operator revokes the key at the provider (outside the lab, not simulated).
4. Recovery: the note is sanitized and the guard passes; the notebook records the drill.
5. Follow-up: the catalog keeps SC-01 to SC-05 with the cases that caught each step.

The drill is synthetic and is not evidence that a real incident was handled; it shows that the technical controls fire in the order the runbook expects.

## Resumen en español

Reporte: contacto privado a través del perfil público de Marco en GitHub, sin direcciones inventadas; el reporte privado de vulnerabilidades de GitHub queda NO_PROBADO hasta que el propietario aporte evidencia. Severidades S1–S4 con responsable, primera respuesta y plazo. Parches: Python y Git desde sus distribuciones oficiales; acciones fijadas por SHA y actualizadas a mano; sin paquetes de terceros. Detección: hook de pre-commit, `security_check.py` y `check_evidence.py` en cada verificación y en CI, la vista Evidencia y las notificaciones de GitHub. Contención: desconectar, detener el servidor, no empujar ni fusionar. Revocación: en la consola del proveedor o en los ajustes de GitHub; el laboratorio no guarda claves. Recuperación: `git revert`, verificación doble, nueva publicación autorizada por Marco. Seguimiento: bitácora, catálogo y casos. El simulacro DRILL-2026-10-12-01 es sintético y se ejecuta contra dobles en cada verificación.
