# Review and authorized maintenance

This is a portfolio demonstration for inspection and local evaluation under [LICENSE.md](LICENSE.md). External code contributions are not accepted. Visitors may read the documentation, install Python and run a local copy to test the demonstration. They may describe non-sensitive feedback, but must not submit executable payloads, credentials, client information or private source.

A fork or pull request does not grant permission to modify the original repository, run code in its privileged workflows, merge changes or deploy the application. Source modifications and reuse require Marco's prior written authorization. Evaluation-only runtime state and agent definitions do not constitute source contributions.

## Authorized maintainers
Marco controls write access and integration. Read [AGENTS.md](AGENTS.md), the active specification and the [security review](docs/repository-security.md) before changes. Follow source -> requirement -> task -> verification -> evidence. Work on a branch, inspect every diff, run the appropriate checks and submit a PR. Passing CI is not a malicious-code certification or owner acceptance. Never approve or run an unknown external workflow simply because its tests appear successful.

Run:

```sh
python scripts/verify.py
```

Keep local hooks as supplemental, bypassable checks. Do not introduce paid/external services, dependencies or permission changes without their own explicit scope. No visitor is granted write access by this document.
