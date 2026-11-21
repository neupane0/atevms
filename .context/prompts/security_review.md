# Security review (paste into Copilot Chat with the changed files attached)
#file:.context/04_SECURITY.md

Review the attached changes against 04_SECURITY.md. For each item answer PASS / FAIL / N/A with a line of evidence:
- Inputs strictly validated (schema, limits, enums, extra=forbid)? OCR/plate text treated as untrusted and escaped on output?
- Parameterized queries only? No string-built SQL?
- AuthN/AuthZ enforced server-side, deny by default, IDOR checked, jurisdiction scoped?
- Hashes/signatures verified with constant-time compare; verification failures fail closed?
- Replay protection (event_id, counter, timestamp) intact?
- Secrets/PII absent from code, logs, tests, fixtures?
- Audit log entries written for consequential actions? Four-eyes respected?
- New dependencies justified, pinned, scanned?
- Error handling leaks no internals; no swallowed exceptions?
List concrete fixes ordered by severity. Do not rewrite unrelated code.
