# Implementation plan

1. Define synthetic fixtures and explicit controller contracts.
2. Implement request, decision and simulated execution with local idempotency.
3. Add browser and limited read-only MCP adapters around the same controller.
4. Test failure paths, concurrency, stale data and scope.
5. Add fixture validation, staged-content guard and source-hashed evidence.
6. Write audience-specific documentation and conduct a browser walkthrough.
7. Inspect publication contents, then publish only this isolated sample.

Dependencies: Python 3.11+, Git, a local browser for human inspection. No third-party runtime packages or model providers.
