# Decision record

| ID | Decision | Reason | Trade-off / revisit trigger |
|---|---|---|---|
| D01 | Fictional after-sales workflow | Shows business rules, human control and integration failure in one understandable journey | Exercise limits are not validated merchant requirements |
| D02 | Deterministic planner first | Repeatable baseline, no keys or model spend | No claim about language understanding or LLM quality |
| D03 | Python standard library | Reviewers can run a small application without package setup | Development HTTP server, not public hosting |
| D04 | In-memory state | Makes the sample easy to reset and inspect | No restart recovery; add durable storage before a pilot |
| D05 | Read-only MCP subset | Demonstrates a tool boundary without delegating execution | Actual assistant-client interoperability remains untested |
| D06 | Human-facing approval UI | Makes the control visible | Role is simulated, so real identity and RBAC remain required |
| D07 | Local evidence and optional Git hook | Repeatable verification with no cloud automation | Hook must be installed explicitly; it is bypassable |
| D08 | No general code reuse license in v0.1 | Publication and licensing are separate owner decisions | Decide licensing before distributing reusable packages |

The repo name, scenario and interface are initial design choices. They can evolve without claiming that an external stakeholder approved the fictional business policy.
