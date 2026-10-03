---
name: data-quality
description: Validate the synthetic orders and policy when fixture fields, sample amounts or scenarios change.
---
# Synthetic data quality

Read data/orders.json, data/policy.json and specs/001-support-demo/spec.md.
Run `python scripts/validate_data.py`, then `python run.py evaluate`.
Check that IDs are synthetic, amounts/days have valid types, no PII fields are added and all expected scenario outcomes still make sense.
If a contract changes, update validator, scenario expectations and acceptance tests together.
Deliver the changed fixture paths, failed/passed checks and remaining uncertainty.
Never import live customer records to enrich the demonstration.
