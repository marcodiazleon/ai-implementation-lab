# Visual review — 2026-10-03

Scope: U04, S01 0.3, R11/R13 and C052/C053. Internal review by the implementing assistant. Product extensions remain planned.

## Delivered view
Black canvas (#080808), off-white text (#FAFAFA), dark panels, personal header, anchored navigation and keyboard skip link. The request, review criteria and activity log have separate visual areas. Existing browser IDs/event handlers and all domain/API behavior are retained.

## Observed browser checks
Environment: Codex in-app browser on Windows, desktop 1280×720 and narrow viewport 390×844. Exact browser-engine version was not recorded.

| Case | Expected | Observed | Result |
|---|---|---|---|
| C052 / appearance | Black canvas, white text, readable actions | Computed body background rgb(8,8,8), text rgb(250,250,250); visible personal header and panels | PASS |
| C052 / decision flow | No execution before approval | UI displayed approval-required message; no receipt | PASS |
| C052 / failure and retry | No receipt on injected failure; one on retry | Failure message and counter 00; successful retry and replay both returned the same receipt, counter 01 | PASS |
| C053 / narrow layout | Single work column; no page-wide overflow | One 335px work column at 390px viewport; scroll width 375px; table has its own scroll area | PASS |
| C053 / keyboard | Reach controls, activate action, see focus | Tab from select reached Analyze; focus outline white 2px with 4px offset; Enter analyzed the late case and showed the expected block | PASS |
| C053 / skip link | Skip to workspace | Enter on skip link moved focus to workspace | PASS |

No browser error/warning entries were returned during the checked session. These observations cover the described paths; screen-reader and full accessibility conformance audits were not performed.

A separate loopback server at port 8766 provided the synthetic checks. The original server at 8765 was not restarted or reset; its tab was reloaded after the change. Final screenshots show the retained test-session receipt count and event history; reloading resets the selected form context, not the server's data.

## Version and evidence
Base revision: 97775f51ea701808cff656de6ed58f0680d1eef6.
S01 version: 0.3. Browser-tested artifacts:
- web/index.html SHA256: 820aa669268eaea292aad4dfcb416c19760b55248cee1cd9aea1a56017b97c4d
- web/style.css SHA256: 8dd5a9cc65f2dd54881237ed8745217ccef675810fed0c6df63b1e74d3eaa415

[Desktop capture](../docs/assets/demo-dark-20261003.jpg) · [Narrow capture](../docs/assets/demo-dark-mobile-20261003.jpg).
Machine checks and individual test results: [latest evidence](../evidence/latest.json). The report is not owner acceptance.

## Remaining work
M02's selected-case state issue, explicit reset and language coverage remain pending. This visual change does not claim those functional fixes. The [product plan](../docs/PLAN_PRODUCTO_Y_DISENO.md) prioritizes the selection correction before editable analysis. Commercial workflow, model integration and public application hosting remain planned.

## Automated regression result
46/46 tests and 7/7 scenarios passed. Fixture, limited publication-pattern and SDD structural checks passed. The core matrix records 52 PASS and one NO_PROBADO (visitor comprehension); the twenty expansion cases remain separate. Machine source identity: bdb020ff54c52e3a115f30385b472d961aae1fd8b905aa9f2ebdffb9bba82ed6.
