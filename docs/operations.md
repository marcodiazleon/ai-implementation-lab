# Operation and maintenance

Owner and maintenance contact: Marco Díaz de León through the public GitHub profile.
Scope: public source sample plus local synthetic runtime. No hosted service or support SLA is offered.

## Start, stop and reset
Run python scripts/verify.py, then python run.py serve. Open the printed loopback address.
Stop with Ctrl+C. Restart creates a fresh in-memory session. The current UI has no reset action; this is EXP-M02.
If the port is occupied, choose another --port. If Python is missing, install it from its official distribution before running; this repo does not install a package catalog.

## Data lifecycle and recovery
Orders/policy/scenarios are versioned synthetic fixtures. Proposals/events/receipts live only in process memory.
The operator can export session JSON before stopping; that download is a record, not an importable backup. Keep only useful synthetic records and delete local exports when no longer needed.
Restoration of runtime state is not supported and is not required for the disposable session. Source restoration uses a known commit/clone. Real persistent operations require EXP-M05.

## Observe and respond
The browser displays blocked outcomes and server-contact errors. The event log and exported snapshot support local diagnosis.
There is no background alert channel. Marco owns issue triage; collaborators should report reproducible synthetic cases without sensitive data.
For a failure: preserve the synthetic request, expected result, version and error; reproduce locally; change the relevant requirement/code/test; regenerate affected evidence. A failed test remains a failure until a recorded successful rerun.
Do not turn a lost response from a future external service into an automatic repeat operation.

## Release checklist
1. Inspect active spec and git status; identify unrelated work.
2. Update requirement source, task and acceptance before behavior changes.
3. Run relevant checks; preserve PASS/FAIL/NO_PROBADO separately.
4. Review diff, documents, privacy, tools and known limitations.
5. Stage exact intended files; run the staged publication guard.
6. Commit/push only within the owner's publication scope.
7. Confirm remote commit, record notebook handoff and next task.

A failed release is corrected with an ordinary new commit, preserving history. No destructive reset or deletion is part of this procedure.

## Keeping the method current
At each requested change, compare relevant book changes with docs/sdd-adoption.md; record version and affected equivalences.
Update only the affected spec, plan, tasks, case results, capability register and notebook. A source change makes the corresponding old test result historical.
Review the expansion backlog when selecting a new milestone. Close an item only when all its acceptance conditions have evidence.
No recurring automation, monitoring process or continuous Notion synchronization is configured.

## Handoff
Read docs/project-status.json first. It names the active spec, backlog, current evidence and next task. Read docs/notebook.md for current decisions and unresolved items. A numbered newer spec is not automatically active.

## Arranque portable

Ejecuta `python scripts/check_environment.py` antes de `python run.py serve`, o usa `INICIAR_LAB.cmd`. [API y traslado](OPENAI_API.md). Las claves y conversaciones no se empaquetan.
