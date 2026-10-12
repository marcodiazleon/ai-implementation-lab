#!/bin/sh
# Payload for scripts/sandbox/run_isolated.sh: run verify.py, check_evidence and the catalog inside the copy and
# leave the regenerated files and the log in /work/export, from where the runner copies the allowlisted names out.
OUT="${1:-/work/export}"; mkdir -p "$OUT"
python3 scripts/verify.py > "$OUT/verify.log" 2>&1; STATUS=$?
echo "verify exit=$STATUS" >> "$OUT/verify.log"
python3 scripts/check_evidence.py >> "$OUT/verify.log" 2>&1
python3 scripts/security_catalog.py >> "$OUT/verify.log" 2>&1
cp evidence/latest.json evidence/sdd-check.json specs/001-support-demo/acceptance.csv docs/requirements-matrix.md "$OUT/"
tail -5 "$OUT/verify.log"; exit $STATUS
