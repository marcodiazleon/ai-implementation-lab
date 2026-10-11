# U18 browser and link check — 2026-10-11

Scope: S01 1.1, branch `claude/laughing-rubin-6e32ve-entry`, revision `f15562d1f0cffe63fda01b52c780748e1856f28e` (clean tree), source fingerprint `17c2039d8d0b`, record fingerprint `6be0d1ea2146`. The implementing assistant ran it. This is not an independent review, an owner acceptance or a test with a new visitor.

Environment: Linux, Playwright Chromium, the public build of that revision served by `python -m http.server` under `/ai-implementation-lab/` and `python run.py serve` on loopback. Reduced motion was on. The raw output is in [u18/check.json](u18/check.json).

The commit that records this check changes only tests/test_u18.py among the sources (an uncommitted historical case may fall back to the build revision), so its source fingerprint differs from the one above; web/, src/ and scripts/ are identical to f15562d.

## Results

| Case | Check | Observed |
|---|---|---|
| C211 (R44) | Language ES → EN → ES on the public build and the local server | Public: footer "Vista pública · Agentes en esta pestaña · API en versión local" → "Public preview · Agents in this tab · API in the local version" → Spanish again; footer role, sidebar note, chat status ("Vista pública"/"Public preview") and the connection notice followed in both directions. Local: "Sesión en memoria · API opcional · Uso local" → "In-memory session · Optional API · Local use" → Spanish; "Sin conexión"/"Not connected" likewise. `html lang` followed. No page errors |
| C214 (R43) | Every repository link of the candidate build | 165 links collected from the method view, the status block and the cases of every requirement. 163 file links open their file at the recorded revision: 141 at f15562d and 22 historical cases at the commit that recorded them (97775f5, 9a187ad, 2092ac6, 723b24e, a103497, 1c36f90, 63061b7, 5a11d8f, 2be5cee). `git cat-file -e` passes for all 163. Over HTTP, each of the 18 distinct URLs returned 200 on github.com, except the Actions run page of C175, which returned 403 to an anonymous request from this environment (run read through the API instead). The only link to main is the one labeled "main en vivo / live main" |
| C202 (R40) | Check runs of f15562d | Runs 38183623455 (push) and 38183626007 (pull request): `verify (ubuntu-latest)` and `verify (windows-latest)` success, each after `verify (ubuntu-latest, Python 3.11)`, `verify (ubuntu-latest, Python 3.13)` and `verify (windows-latest, Python 3.13)` succeeded. The gate log prints each platform and `PASS: verify (windows-latest) requires every matrix member on every platform to succeed` |
| — | Overflow | Document overflow 0 px in Session, How it is built and Evidence at 375, 390 and 1360 px in Spanish and English (18 measurements). At 375/390 px the worked-result table scrolls inside its own region; the result column needs a horizontal swipe |

## Screenshots

Public build of f15562d, in [reports/u18/](u18/): `f15562d1f0cf-{entry,tour}-{es,en}-{1360,390,375}.jpg` and `f15562d1f0cf-evidence-{es,en}-{1360,390}.jpg`. The tour images show the worked result; the evidence images show the revision line and R11 PARCIAL.

## Not executed

A test with a person who does not know the project (C170), an injected-defect CI run (C176), a route review by another person (C177), a screen-reader pass, a live API call, a run on another PC and any check on the published Pages URL, which still serves main 81dfced.
