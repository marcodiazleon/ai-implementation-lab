# S01 — Controlled after-sales demonstration

## Problem and intended reader
A prospective client or recruiter needs to inspect how an implementation strategist turns an ambiguous automation idea into a bounded working example. The exercise is a fictional shop; its rules are proposed for this demo, not a real merchant policy.

## User story
As a local demo operator, I can inspect a synthetic order, understand a proposed refund, approve or reject it and observe a simulated result, including failures and retries.

## Exercise rules
Orders must belong to sample-store, be delivered within 14 days and not exceed 100 DEMO units. No amount supplied by a caller can override the stored order. The eligible fixture is DEMO-101 for 85 DEMO units. Other fixtures intentionally violate individual conditions.

## Requirements
- R01: lookup returns only an in-scope synthetic order; foreign and unknown IDs are indistinguishable.
- R02: eligible refund requests create proposals; invalid fields, disallowed tools and ineligible requests block.
- R03: execute requires an approved proposal; rejection cannot execute.
- R04: order or policy changes invalidate the proposal before execution.
- R05: repeated/concurrent execution produces one local receipt; a changed proposal cannot compensate the same order again.
- R06: pre-effect connector failure creates no receipt and permits a later retry.
- R07: before/after hooks record allowed and blocked operations; pre-hook failure stops execution.
- R08: HTTP serves only loopback routes, rejects foreign origins and bounds JSON bodies.
- R09: MCP exposes two read-only tools and cannot approve or execute.
- R10: fixtures and staged publication content can be checked with executable scripts.
- R11: readers can navigate the guide, run the app and distinguish observed results from future capabilities.

## Acceptance and exclusions
See acceptance.csv. Automated checks prove the bounded example only. Human readability and interface observation are separate checks.
Excluded: real language model, real payments, authentication, durable storage, distributed transactions, production hosting, client data, browser/assistant credential access and automatic connector setup.

## Success signal
A reviewer can reproduce an approved simulation and a blocked action and identify the evidence supporting both. No revenue, efficiency or customer-impact metric is claimed.
