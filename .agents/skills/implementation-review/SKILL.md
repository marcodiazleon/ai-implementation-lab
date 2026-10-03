---
name: implementation-review
description: Review a proposed capability or behavior change against the sample's requirements, tests and public claims.
---
# Review a bounded increment

Read docs/constitution.md, specs/001-support-demo/spec.md and acceptance.csv in that spec directory.
Identify the changed requirement, the user-visible outcome and one relevant failure case.
Inspect the affected controller, adapter or view and the tests that exercise the boundary.
Run `python scripts/verify.py` when execution is appropriate.
Compare documentation claims with actual evidence. Mark unexecuted checks explicitly.
Deliver a short result: requirement, observed behavior, evidence, unresolved limitation and next action.
This procedure is not an authorization to publish, enable providers or contact third parties.
