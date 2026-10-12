#!/bin/sh
# C278 / C289: build the public site, start the fake-provider local server and a static server, run security.js.
# Meant to run inside scripts/sandbox/run_isolated.sh (SBX_AS=0 so Chromium can reserve address space):
#   SBX_PIDS=256 scripts/sandbox/run_isolated.sh SCRATCH -- sh scripts/browser/security_run.sh   (result exported as security-browser.json)
set -u
OUT="${1:-/work/export/security-browser.json}"; mkdir -p "$(dirname "$OUT")"
python3 scripts/build_pages.py >/dev/null || exit 1
python3 scripts/browser/security_server.py 18765 & LOCAL=$!
(cd _site && python3 -m http.server 18766 --bind 127.0.0.1 >/dev/null 2>&1) & STATIC=$!
sleep 2
node scripts/browser/security.js http://127.0.0.1:18765 http://127.0.0.1:18766 > "$OUT"; STATUS=$?
kill $LOCAL $STATIC 2>/dev/null; wait $LOCAL $STATIC 2>/dev/null
cat "$OUT"; exit $STATUS
