# Working in this repository

This is a public, synthetic engineering sample. Start with README.md, docs/constitution.md and specs/001-support-demo/spec.md.

- Keep real customer data, credentials, private source and local machine paths out of the repository.
- Keep the deterministic/offline mode working. Do not silently enable providers or external actions.
- A proposal cannot bypass the controller's approval and stale-data checks.
- Describe simulated identity, in-memory state and MCP subset limits accurately.
- Run python scripts/verify.py after relevant changes. Review evidence/latest.json; a generated PASS is not production approval.
- For data changes use .agents/skills/data-quality/SKILL.md.
- For requirement and acceptance changes use .agents/skills/implementation-review/SKILL.md.
- Update the acceptance matrix for changed behavior. Do not rewrite the entire specification for an unrelated small fix.
