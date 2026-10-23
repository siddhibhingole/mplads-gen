# Evaluation
Run `pytest`, `ruff check app tests scripts`, `mypy app`, frontend `npm run lint`, `npm run test`, `npm run build`, and `python scripts/smoke_test.py`.
Acceptance: ingest → risk scan → alert → cited explanation → fetch work; strict explanation schema; citation allow-list; no committed secrets.
Rules: sanction pending >45 days; incomplete >365 days; no payment >90 days; no progress update >90 days; payment > sanction; low payment ratio; cost threshold; consistency issues.
Measure citation coverage, invalid-row rejection reasons, reviewer agreement, false-positive rate, API p50/p95, and rule precision/recall against synthetic labels. Synthetic results do not imply real-world performance. No automated adverse action.
