# Engineering method adoption

Version 0.2, reviewed 2026-10-03. Owner: Marco Díaz de León.
Current scope: S01 1.0 conversation-only Session (U12), existing local provider backend and retained historical synthetic implementation; S02 is the planned expansion.
The first release preceded completion of its specification. That historical deviation remains recorded; this revision completes the current project's method documents and checks their relationships.

## Source and interpretation
Reference: author's engineering book, base 1.0 and portable extension 1.1 (2026-09-30), adoption/course update and master entry prompt (2026-10-03).
The current index and relevant chapters were read directly. Public documentation is original project-specific writing; private book text, screenshots, identifiers and unrelated project examples are not copied here.
An older source note describes a provisional course-layer scheme. The corrected chapter 01 and later chapter 13 take precedence: layers 00–05 with judgment across them. No changes were made to the source book.

## Chapter equivalences
| Chapter / obligation | Project artifact | Application or justified exception |
|---|---|---|
| 01 Method and criteria | active spec, plan, tasks, acceptance; this map | Requirements lead subsequent changes; initial chronology preserved |
| 02 Start and recover context | notebook, decisions, project-status.json | User's known purpose/repo/destination recovered; no repeated interview |
| 03 Research and use cases | investigacion.md, tools-and-capabilities.md, spec CU01–CU07 | Compare only choices relevant to local example |
| 04 Agents, hooks, skills, MCP | tools-and-capabilities.md, capabilities.md, architecture.md | Runtime agent not needed; development executor described separately |
| 05 Rules and SDD templates | AGENTS, constitution, spec/plan/tasks/acceptance | Existing paths reused; structured fields completed |
| 06 Executor adaptation | tools-and-capabilities.md, CLAUDE.md | Manual rule/skill reading used; native discovery in other clients not claimed |
| 07 QA and evidence | tests, verify.py, acceptance.csv, reports and evidence | Per-case expected/observed, environment and version; self-review identified |
| 08 Decisions and continuity | decisions.md, notebook.md, operations.md | Owners, sources, next task and pending decisions retained |
| 09 Domain example | No imported artifact | Not applicable: another teaching domain, not this project's requirement source |
| 10 Sources and versions | investigacion.md, tools register, evidence hashes | Local versions measured; older conflicting layer note superseded |
| 11 Portable stages 0–5 | stage map below; operations.md | Current shell/browser workflow documented; other machines unverified |
| 12 Separate QA-project example | No imported artifact | Not applicable: project-specific example, not inherited policy or permissions |
| 13 Course/adoption | engineering-guide.md, current equivalence map | Knowledge layers separated from delivery stages |
| 14 Single entry and active spec | AGENTS.md → project-status.json | Active S01 selected explicitly; expansion S02 cannot silently replace it |

## Stage map
| Stage | Input and action | Exit artifact |
|---|---|---|
| 0A Open | Identify repo, executor, method, permitted tools | notebook opening record; tool register |
| 0B Recover | Read rules/continuity; inspect Git | preserved changes; explicit active spec |
| 0C Define | Owner purpose and audience; first useful example | sources U01–U03, CU01–CU07, exclusions |
| 1 Mode | Local browser, offline fixtures, disposable state | spec attributes; operations guide |
| 2 Research | Relevant alternatives and primary references | research and tool selection records |
| 3A Constitution | Stable authority/data/quality principles | constitution.md |
| 3B Specify | Actor, trigger, preconditions, errors, result, source | spec.md and acceptance definitions |
| 3C Plan | Components, contracts, recovery, tool choice | plan.md and architecture.md |
| 3D Tasks | Requirement, dependency, owner and done criterion | tasks.md |
| 4A Environment | Versions, rules/manual skills, commands | tool register and run environment |
| 4B Implement | Bounded task and expected case | code/doc diff |
| 5A Validate | Positive/negative cases and UI where relevant | per-case evidence; manual states retained |
| 5B Review | Traceability, source/privacy and complete diff | internal review report; no independent-review claim |
| 5C Deliver | Version, commands, known issues, public scope | README, report, publication commit |
| 5D Maintain | Next task, owners, affected evidence | notebook, operations, expansion backlog |

## Loading and controls
During this update the assistant explicitly read project AGENTS, constitution, active spec, plan/tasks, notebook and both project skills. Their prescribed checks were executed.
This records manual application, not native skill discovery or proof of universal instruction obedience. Hook and protocol behavior have separate executable evidence. The CLAUDE adapter's automatic import in another session remains NOT_TESTED.

## Review result and boundaries
Current document coverage and relationships are checked by scripts/sdd_check.py; see evidence/sdd-check.json and reports/SDD_REVIEW.md.
The map covers all book areas through concrete artifacts or explained scope exclusions. Structural coverage does not certify production readiness, owner acceptance, all browser accessibility or every executor's native loading.
Owner comprehension, live-client MCP compatibility and other expansion guarantees retain their actual status. This update does not claim retroactive SDD compliance.
