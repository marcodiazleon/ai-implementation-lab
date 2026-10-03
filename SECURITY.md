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
