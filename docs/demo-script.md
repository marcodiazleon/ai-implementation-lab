# Ten-minute walkthrough

## Prepare
Run `python scripts/verify.py`, then `python run.py serve`. Open the loopback URL printed by the server. Do not enter real data.

## Demonstrate the happy path and the control
1. Choose the eligible order and analyze it. Expect PENDING_APPROVAL.
2. Attempt execution before approving. Expect APPROVAL_REQUIRED and zero receipts.
3. Approve. Expect APPROVED.
4. Enable the simulated connector failure and execute. Expect SIMULATED_CONNECTOR_FAILURE and zero receipts.
5. Disable the simulated failure and execute again. Expect one SIMULATED receipt.
6. Execute again. Expect the same receipt and count of one.
7. Export the trace. The downloaded JSON describes the local session, not production evidence.

## Demonstrate boundaries
Select the expired-window, above-limit, foreign-workspace and unknown-order cases. Each must block. The foreign and unknown order return the same public reason. Select read-only lookup: it must return an order without creating a proposal. The disallowed-tool case must be rejected before it can act.

To demonstrate rejection instead of approval, restart the local server for a fresh session, analyze the eligible order, reject it and attempt execution. No receipt is created.

## Explain the business connection
The sample makes responsibility visible: a planner suggests, policy constrains, an operator decides and a connector returns a result. A real client engagement must validate the policy with business owners and add authenticated identity, durable state and integration-specific recovery.

## Questions to ask a reviewer
Can you identify who decides? Can you explain why an action was blocked? Can you reproduce the evidence? Which missing control would prevent your organization from piloting this?
