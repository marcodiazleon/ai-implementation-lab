# Security boundaries

This repository is a local educational engineering sample with synthetic data. Do not expose its HTTP server to a network or use it for real financial operations.

## Controls demonstrated
Explicit tool and route allowlists, same-origin/Host checks (a browser boundary, not authentication against local processes), request size, type, nesting, read-timeout and concurrency limits with fixed error codes, synthetic workspace scope, approval sequencing, stale-proposal checks, local retry protection, one shared detector for named credential formats in the publication guard, the agent executor, the agent store and the interface, GitHub Actions pinned by commit SHA, and a standard-library security gate inside every verification and CI job. The threat model, the data inventory, the endpoint matrix and the control catalog with derived states (VERIFICADO, PARCIAL, NO_PROBADO, FUTURO) are in [docs/threat-model.md](docs/threat-model.md); the inventory and analysis coverage in [docs/supply-chain.md](docs/supply-chain.md); reporting, severities, patches, revocation, rollback and the synthetic drill in [docs/security-runbook.md](docs/security-runbook.md).

## Controls not supplied
Real authentication or user isolation, encryption/key management, persistent audit storage, tamper-resistant signing, durable transaction recovery, distributed idempotency, external connector authentication, LLM prompt-injection defenses and independent security certification.

The browser approval is a simulated role; any local process can send that request. A local Git hook can be bypassed and detects named patterns only (no entropy analysis). A valid event hash chain does not prove who produced it or prevent full recomputation.

Never paste sensitive information into issues or the demo. For a potential vulnerability, contact the owner through the GitHub profile to arrange a suitable disclosure channel before sharing sensitive details ([runbook](docs/security-runbook.md)). Owner-side settings such as two-factor authentication, branch protection and private vulnerability reporting are recorded as NO_PROBADO until the owner supplies read-only evidence.

## Conexión API opcional

La clave se introduce explícitamente y permanece en memoria del servidor local. No se lee del entorno ni de archivos. Destinos fijos api.openai.com y api.anthropic.com; no hay redirecciones ni URL arbitraria. Las respuestas de error, la salida estándar de errores y las exportaciones nunca llevan la clave; una excepción inesperada produce un código fijo sin mensaje. Sesiones, caducidad, límites y privacidad: [guía API](docs/OPENAI_API.md). Este servidor local no proporciona autenticación multiusuario ni aislamiento frente a otros procesos del mismo equipo; no se debe exponer en red. Las pruebas no utilizan credenciales reales.
