# U17 browser check — 2026-10-11

Scope: S01 1.1, branch `claude/laughing-rubin-6e32ve-entry`, source fingerprint `890277c7c704` (the `source_id` in evidence/latest.json of the same commit). Executed by the implementing assistant; this is not an independent review, an owner acceptance or a test with a new visitor.

Environment: Linux, Playwright Chromium 1194, the public build served by `python -m http.server` under `/ai-implementation-lab/` and the local server on loopback. Reduced motion was enabled for screenshots.

## Results

| Case | Check | Observed |
|---|---|---|
| C171 (R34) | First screen of Session at 1360, 390 and 375 px, Spanish and English | Name as the only h1, positioning, contribution, AI attribution, tour button and demo/local/pending line above the composer; English eyebrow, lead, button, scope line and skip link |
| C172 (R35) | Draft through the tour; links to requirements | Draft "Borrador de prueba U17" kept after #method, #evidence/R03, #agents and back to Session; #evidence/R03 selected R03 with PASS; tour headings in both languages |
| C173 (R36) | Evidence status | Five separate records; review LIMITED with bilingual scope; owner acceptance not recorded; not integrated; not deployed; baseline and fingerprint shown and matching; R11 PARCIAL 1 of 2 |
| C174 (R38) | Overflow, keyboard, contrast | Document overflow 0 px in Session, How it is built and Evidence at 375, 390 and 1360 px; collapsed rail with text labels; first Tab reaches the skip link; Enter focuses the message box from Session and from How it is built |
| — | Console | No page errors; the only failed request is the missing favicon, which also fails on main |

Two defects were found and fixed during the check: the skip link moved focus to the view heading instead of the message box, and three secondary grays were below 4.5:1 (3.54, 4.22 and 4.47). Both fixes are in the commit that holds this report.

## Contrast measured on rendered text

Every visible text node in the three views, grouped by text color, background color, size and weight. Background is the first opaque ancestor. Thresholds: 4.5:1, or 3:1 for 24 px and larger or 18.66 px bold. This covers these three views in their default state; it is not a full WCAG evaluation.

| View | Distinct pairs | Lowest ratio | Lowest pair | Below threshold |
|---|---|---|---|---|
| Session | 31 | 4.65 | #797983 on #080808, 12 px | 0 |
| How it is built | 27 | 4.86 | #80808a on #101012, 8 px | 0 |
| Evidence (R11) | 31 | 4.86 | #80808a on #101012, 8 px | 0 |

Before the fix, Session had three pairs below 4.5:1: the "About models" summary (#666672, 3.54), the model hint (#72727e, 4.22) and the footer (#777777, 4.47). They now use #85858f (5.48 on the page background).

## Screenshots

Public build of this revision, in [reports/u17/](u17/):

| View | Desktop 1360 px | Mobile 390 px |
|---|---|---|
| Entry (Session) | [890277c7c704-entry-1360.jpg](u17/890277c7c704-entry-1360.jpg) | [890277c7c704-entry-390.jpg](u17/890277c7c704-entry-390.jpg) |
| Tour (How it is built) | [890277c7c704-tour-1360.jpg](u17/890277c7c704-tour-1360.jpg) | [890277c7c704-tour-390.jpg](u17/890277c7c704-tour-390.jpg) |
| Partial evidence (R11) | [890277c7c704-evidence-partial-1360.jpg](u17/890277c7c704-evidence-partial-1360.jpg) | [890277c7c704-evidence-partial-390.jpg](u17/890277c7c704-evidence-partial-390.jpg) |

## Not executed

A test with a person who does not know the project (C170), the CI run with an injected defect (C176), a screen-reader pass, and any check on the published GitHub Pages URL, which still serves main.
