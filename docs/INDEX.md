# Documentation index · Índice de documentación

Current revision: the S01 version selected in [project-status.json](project-status.json). Documents marked historical keep the version and date they were written for; they are not descriptions of the current application.

## Three routes · Tres rutas

| Time | Route | What you get |
|---|---|---|
| 30 seconds | Open the [public demo](https://marcodiazleon.github.io/ai-implementation-lab/) and read the presentation at the top of Session | Who Marco is, what he contributes and what is pending |
| 3 minutes | In the demo, open How it is built and follow the tour; optionally run `python run.py tour` locally | A fictional case, its controls and where each one is tested |
| Technical review | This index: specification, architecture, decisions, tests and evidence | The full chain from need to evidence and the state of every record |

## Technical review · Revisión técnica

| Topic | Read |
|---|---|
| Specification: sources, use cases, requirements | [spec.md](../specs/001-support-demo/spec.md) |
| Plan and tasks | [plan.md](../specs/001-support-demo/plan.md) · [tasks.md](../specs/001-support-demo/tasks.md) |
| Acceptance cases and their status | [acceptance.csv](../specs/001-support-demo/acceptance.csv) |
| Architecture | [architecture.md](architecture.md) |
| Decisions | [decisions.md](decisions.md) |
| ID registry for open pull requests | [id-registry.json](id-registry.json) |
| Tests | [tests/](../tests/) |
| Evidence of this revision | [evidence/latest.json](../evidence/latest.json) · [sdd-check.json](../evidence/sdd-check.json) |
| Project records: verification, review, acceptance, integration, deployment | [project-status.json](project-status.json) |
| Working method and Marco's role | [engineering-guide.md](engineering-guide.md) · [sdd-adoption.md](sdd-adoption.md) |
| Operation, startup and handoff | [operations.md](operations.md) |
| Capabilities and limits (canonical table) | [capabilities.md](capabilities.md) |
| Security boundaries | [SECURITY.md](../SECURITY.md) |
| Spanish guide | [START_HERE_ES.md](START_HERE_ES.md) |

Outside the main route: [API connection guide](OPENAI_API.md), [agents and MCP guide](WORKBENCH.md), [tool register](tools-and-capabilities.md), [roadmap](roadmap.md) and the [expansion backlog](../specs/002-expansion/spec.md).

## One requirement from need to evidence · Un requisito de la necesidad a la evidencia

| Link | Where | Content |
|---|---|---|
| Need | [spec.md](../specs/001-support-demo/spec.md), sources U01 and D01 | A public working example; a fictional shop where nothing is refunded before a person approves |
| Requirement | spec.md, R03 | While approval is absent or rejected, block execution; reject invalid decision transitions |
| Task | [tasks.md](../specs/001-support-demo/tasks.md), T02 | Review transitions and stale-data check |
| Code | [controller.py](../src/lab/controller.py), `Lab.execute` | Raises `APPROVAL_REQUIRED` unless the proposal is `APPROVED` |
| Test | [test_lab.py](../tests/test_lab.py), `test_execute_requires_approval` | A pending proposal cannot execute and creates no receipt |
| Case | [acceptance.csv](../specs/001-support-demo/acceptance.csv), C018 | Expected `APPROVAL_REQUIRED; no receipt`, with status and evidence file |
| Evidence | [evidence/latest.json](../evidence/latest.json), `test_lab.WorkflowTests.test_execute_requires_approval` | Status of this revision's run; the same entry at the published revision: [latest.json @ 81dfced](https://github.com/marcodiazleon/ai-implementation-lab/blob/81dfced59cc85231e25732137859923b39a2beed/evidence/latest.json) |

`python run.py tour` shows the same control at step 2, and the Evidence view shows R03 with its cases.

## Historical documents · Documentos históricos

Kept as written. Each one describes the version named here, not the current application.

| Document | Date | Version or scope |
|---|---|---|
| [demo-script.md](demo-script.md) | 2026-10-03 | Visible refund exercise, before U13 removed it from the interface |
| [VISUAL_REVIEW_2026-10-03.md](../reports/VISUAL_REVIEW_2026-10-03.md) | 2026-10-03 | written for S01 0.3 |
| [MENU_API_REVIEW_2026-10-03.md](../reports/MENU_API_REVIEW_2026-10-03.md) | 2026-10-03 | written for S01 0.4 |
| [AGENTS_REVIEW_2026-10-03.md](../reports/AGENTS_REVIEW_2026-10-03.md) | 2026-10-03 | written for S01 0.6 |
| [STUDIO_REVIEW_2026-10-03.md](../reports/STUDIO_REVIEW_2026-10-03.md) | 2026-10-03 | written for S01 0.7 |
| [SESSION_UI_REVIEW_2026-10-03.md](../reports/SESSION_UI_REVIEW_2026-10-03.md) | 2026-10-03 | written for S01 0.8 |
| [LANGUAGE_REVIEW_2026-10-03.md](../reports/LANGUAGE_REVIEW_2026-10-03.md) | 2026-10-03 | Language selector, U06 |
| [EDITORIAL_REVIEW.md](../reports/EDITORIAL_REVIEW.md) | 2026-10-03 | Wording review of that date |
| [PUBLICATION.md](../reports/PUBLICATION.md) | 2026-10-03 | Publication record of that date |
| [SDD_REVIEW.md](../reports/SDD_REVIEW.md) | 2026-10-03 | Method completion review of that date |
| [VALIDATION.md](../reports/VALIDATION.md) | 2026-10-03 | Validation report of that date |
| [U17_BROWSER_CHECK_2026-10-11.md](../reports/U17_BROWSER_CHECK_2026-10-11.md) | 2026-10-11 | written for S01 1.1, source fingerprint 890277c7c704 |
| [U18_BROWSER_CHECK_2026-10-11.md](../reports/U18_BROWSER_CHECK_2026-10-11.md) | 2026-10-11 | written for S01 1.1, revision f15562d, source fingerprint 17c2039d8d0b |
| [investigacion.md](investigacion.md), [INVESTIGACION_EXPANSION_2026-10-03.md](INVESTIGACION_EXPANSION_2026-10-03.md), [INVESTIGACION_PRODUCTO_INTERACTIVO_2026-10-03.md](INVESTIGACION_PRODUCTO_INTERACTIVO_2026-10-03.md), [PLAN_PRODUCTO_Y_DISENO.md](PLAN_PRODUCTO_Y_DISENO.md) | 2026-10-03 | Research and plans; proposals, not implemented features |
| [notebook.md](notebook.md) | Running log | Dated entries; each describes its own moment |
