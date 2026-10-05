# Security boundaries

This repository is a local educational engineering sample with synthetic data. Do not expose its HTTP server to a network or use it for real financial operations.

## Controls demonstrated
Explicit tool and route allowlists, same-origin/Host checks, request size/type checks, synthetic workspace scope, approval sequencing, stale-proposal checks and local retry protection.

## Controls not supplied
Real authentication or user isolation, encryption/key management, persistent audit storage, tamper-resistant signing, durable transaction recovery, distributed idempotency, external connector authentication, LLM prompt-injection defenses and independent security certification.

The browser approval is a simulated role; any local process can send that request. A local Git hook can be bypassed and detects only a few patterns. A valid event hash chain does not prove who produced it or prevent full recomputation.

Never paste sensitive information into issues or the demo. For a potential vulnerability, contact the owner through the GitHub profile to arrange a suitable disclosure channel before sharing sensitive details.

## Conexión API opcional

La clave se introduce explícitamente y permanece en memoria del servidor local. No se lee del entorno ni de archivos. Destino fijo api.openai.com; no hay redirecciones ni URL arbitraria. Sesiones, caducidad, límites y privacidad: [guía API](docs/OPENAI_API.md). Este servidor local no proporciona autenticación multiusuario ni aislamiento frente a otros procesos del mismo equipo; no se debe exponer en red. Las pruebas no utilizan credenciales reales.

## Public review and source integrity
See [evaluation rights](LICENSE.md), [review policy](CONTRIBUTING.md) and [repository protection review](docs/repository-security.md). Public visitors are not granted write access to the original repository. A proposed PR is untrusted input, not executable approval. Do not run external scripts or workflows from feedback.
The public Pages site is static and has no shared write/upload API. Local evaluation runs on loopback with Host/Origin checks; custom agent definitions are local state and grant no shell tools. These boundaries reduce specific risks and do not establish immunity to malicious activity. Do not expose the local server to a network or use real customer data.
Administrative branch protections and collaborator/Actions audits are separate from source files; their confirmed or blocked state is recorded in the security review. A legal notice or CODEOWNERS file does not enforce permissions.
