# Architecture and contracts

## MVC is not MCP
MVC organizes application responsibilities. MCP defines a client-to-tool protocol. This sample uses both for different purposes.

| Responsibility | Implementation |
|---|---|
| Model | `models.py`, synthetic fixtures and proposal state |
| Controller | `controller.py`: eligibility, decisions, scope and retry rules |
| View | `web/`: selection, reviewer controls and event trace |
| HTTP adapter | `server.py`: explicit routes on loopback |
| MCP adapter | `mcp_server.py`: two read-only tools over stdio |
| Hooks | `hooks.py`: before/after application events |

```mermaid
flowchart LR
    U[Browser operator] --> H[Loopback HTTP adapter]
    H --> C[Controller]
    C --> D[Synthetic orders and exercise policy]
    C --> P[Proposal]
    P --> R[Simulated reviewer decision]
    R --> X[Local receipt simulation]
    C --> A[Before and after hooks]
    M[MCP client] --> T[Read-only stdio tools]
    T --> C
```

The MCP client has no approve or execute tool. HTTP review buttons exercise a workflow gate; they do not authenticate a person. The local operator has full demo authority.

## State and failures
A proposal starts PENDING_APPROVAL and can become APPROVED or REJECTED. Execution requires approval and unchanged order/policy digests. A successful simulation becomes SIMULATED. A retry returns the same stored receipt. A changed proposal cannot create a second receipt for an already compensated order in that process.

A simulated connector failure occurs **before** writing a receipt. This demonstrates safe retry for a known pre-effect failure. It does not solve an external provider timing out after a real effect, crash recovery, database atomicity or distributed concurrency.

An RLock serializes controller operations in one process. Memory is cleared by restart. After-hook failures following a state change are not transactionally rolled back; production would need a transactional outbox or equivalent durable design.

## MCP subset
Protocol version: **2025-11-25**, deliberately pinned, not a claim of latest-version support.
Transport: newline-delimited JSON-RPC over stdin/stdout.
Methods: initialize, notifications/initialized, ping, tools/list, tools/call.
Tools: lookup_demo_order(order_id), read_demo_policy().
Not included: HTTP transport, authentication, subscriptions, pagination, resources, prompts, cancellation, live client configuration or certification.

Run `python run.py mcp` from the repository. A client would launch that command with the repository as working directory. No connector is installed or connected automatically.
