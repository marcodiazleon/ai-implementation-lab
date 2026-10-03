# Working in this repository

Read docs/project-status.json for the active spec, then docs/constitution.md, that spec's spec.md/plan.md/tasks.md, and docs/notebook.md. Keep the current folder structure and preserve unrelated changes.

- Link each behavior change to a requirement, source, task and expected case before implementation.
- Keep synthetic data and offline execution. Real providers, costs or customer effects need their own explicit scope.
- Use docs/tools-and-capabilities.md to select tools and distinguish manual reading, automatic discovery, configuration and tested behavior.
- Run python scripts/sdd_check.py for documentation/traceability changes and python scripts/verify.py for relevant implementation changes. Inspect failures and per-case evidence.
- Use .agents/skills/data-quality/SKILL.md for fixture work and .agents/skills/implementation-review/SKILL.md for requirement/review work.
- Keep source history and evidence. Passing tests does not establish owner acceptance or authorize extra publication.
- Write direct descriptive text; preserve factual attribution of AI-assisted work.
- Update decisions, affected acceptance records, expansion status and notebook at the end of a change. No scheduled process is implied.
