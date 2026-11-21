---
applyTo: "server/**,edge/**,infra/**"
---
Apply `.context/04_SECURITY.md` to all code here. Validate all input with strict schemas, use parameterized queries only,
verify signatures/hashes with constant-time comparison and fail closed, never log secrets or PII, never disable TLS verification,
never use eval/exec/pickle on untrusted data, and add an abuse-case test for every new endpoint or parser.
