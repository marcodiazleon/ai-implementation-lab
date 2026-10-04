# Four-role workbench and Context7 review

Date: 2026-10-03, America/Mexico_City. Live MCP observations occurred at 2026-10-04 01:12 UTC.

Scope: U07, S01 0.6, R18-R20, T25-T27. Review by the implementing assistant; not independent acceptance.

## Observed behavior

- Browser: Project Manager, Researcher, Implementer and Quality Reviewer ran locally; successive outputs carried preceding artifacts for the same brief. Reviewer reported all three preceding roles present.
- Spanish/English switch translated role cards, forms and notices while preserving original brief and document text. Language persistence was covered in the preceding language review.
- Model route: a local injected transport returned a structured response and 71 fixture tokens. Missing consent was blocked visibly, then explicit consent allowed one request. This was not an OpenAI inference.
- Context7: initial network-restricted preview failed safely. The normal local server with network access completed initialize, initialized notification, discovery, resolve-library-id for Python, and query-docs for `/python/cpython`. Query text: `How do I validate a JSON request?`. UI reported 2/20 tool attempts and returned Python documentation with source URLs. No key was supplied. Disconnect closed local access; retained documentation was explicitly attached to a local researcher run.
- Downloads: Markdown and JSON files were created by the browser. The download-event automation was unavailable; filesystem inspection confirmed the saved files. The JSON was parsed and its document SHA-256 verified; no session token or API key is present. See [browser export](../evidence/agent-browser-export.json). JSON is delivered as an attachment MIME type for browser compatibility.
- Four role cards and the resulting review were visually inspected in the dark interface. No broad accessibility/mobile certification is claimed.

Automated evidence: [latest.json](../evidence/latest.json), with per-case results; [acceptance.csv](../specs/001-support-demo/acceptance.csv) separates automated and manual cases. Offline tests cover model context isolation, shared budget, stale brief rejection, credential patterns, malformed/truncated output, MCP discovery, tool allowlist, consent, expiry, revocation, remote errors, JSON/SSE parsing and HTTP boundaries.

## Remaining limits

Real OpenAI inference and its content quality are NOT_EXECUTED. Destination-PC startup is NOT_EXECUTED. Hashes and hook PASS do not establish product correctness or customer acceptance. Local templates produce a useful outline but do not substitute for an investigation or implementation.
