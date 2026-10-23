# Security
- `AUTH_MODE=mock` and `X-Demo-Role` are local-only and unsafe for deployment.
- Production verifies Firebase ID tokens and reads role from trusted custom claims: citizen=read, officer=review, admin=manage.
- Request models validate fields; uploads accept CSV/JSON only and enforce size/row limits. SQL queries are parameterized.
- Raw payloads are SHA-256 hashed. Audit events append to JSONL; production should use immutable Cloud Logging/retention-locked storage.
- Lightweight in-process rate limiting is not a distributed gateway replacement.
- PII/prompt-injection checks are heuristics, not a full DLP solution.
- No credentials in source. Use Secret Manager; never commit `.env` or service account keys.
- Only synthetic records are bundled. Risk signals require human verification.
