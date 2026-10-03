# Validation report — 2026-10-03

## Scope
Local, synthetic implementation sample. This is not a production review or independent security audit.

## Automated evidence
Run `python scripts/verify.py`. The resulting [evidence/latest.json](../evidence/latest.json) records the exact count, failures, scenario outcomes and hashes of tested source files.

Covered: business-rule denials, request contract, workspace scope, approval/rejection, stale order/policy, one local receipt across concurrent retries, pre-effect connector failure, hook failure, event-chain edits, HTTP boundaries, MCP stdio exchange, fixture contract and staged-content scanning. The Git hook is tested by creating a temporary repository and observing a blocked commit followed by an accepted clean commit.

## Browser observation
The local interface was exercised through browser automation on 2026-10-03:
- An eligible synthetic request displayed PENDING_APPROVAL.
- Execution before approval displayed APPROVAL_REQUIRED with zero receipts.
- Approval enabled the workflow's next step.
- A simulated connector failure produced zero receipts.
- Retrying without the simulated failure created one receipt.
- Repeating execution returned the same receipt; the counter remained one and the trace displayed REPLAY.
- The full-page screenshot shows the resulting UI: [original walkthrough](../docs/assets/demo-original-20261003.jpg).

This is a browser observation by the development assistant, not an operator acceptance session or a broad accessibility/cross-browser audit.

## Still unverified
Owner/recruiter comprehension; a real assistant client using MCP; LLM quality; authenticated authorization; durable crash recovery; real connector outcomes; production deployment.
