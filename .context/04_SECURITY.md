# 04 Security Requirements (MANDATORY on every change)
Goal is defense in depth, not "unhackable". Assets at risk: fines, evidence, citizen data, officer accounts.

## Threat model (maintain in /docs/threat-model.md; STRIDE per component)
| Asset | Threat | Controls |
|---|---|---|
| Evidence media | tamper/delete/forge | SHA-256 + Ed25519 signed manifest, hash chain, WORM storage, audit log |
| Edge device | theft, SSH takeover, fake device | LUKS, key-only SSH over VPN, per-device cert, secure boot (later) |
| Edge<->server | MITM, replay | mTLS, counter + timestamp + nonce, reject stale/duplicate |
| Owner data | leak, insider snooping | RBAC, field encryption, minimization, lookup access logs |
| Officer accounts | credential theft | Argon2id, TOTP MFA, short sessions |
| API/dashboard | injection, broken access control | schema validation, server-side authz, rate limits, CSP |
| Fines | fake/altered challans | four-eyes on edits, append-only audit |

## Implementation rules
Auth: mTLS for devices (private CA, revocation, rotation). Officers via OIDC or a vetted library; Argon2id;
mandatory TOTP MFA; 15-min JWT; rotating refresh token in HttpOnly+Secure+SameSite=Strict cookie. TLS 1.2+, HSTS.
Authz: roles `device, officer, senior_officer, auditor, admin`. DENY BY DEFAULT. Check every object server-side
(prevent IDOR). Scope officers by jurisdiction.
Input: Pydantic strict models, `extra="forbid"`, length/enum limits. Parameterized SQL only.
OCR/plate text is attacker-controlled (printed plates/signs can carry payloads): regex-validate, escape in HTML/PDF/SMS.
Files: verify magic bytes, size limits, server-generated names, re-verify SHA-256 and signature on ingestion
using constant-time compare (`hmac.compare_digest`). MinIO private buckets, SSE, versioning/object lock, presigned URLs.
Abuse: rate limits, login throttling, request size limits, CORS allow-list (never `*`), CSP, X-Content-Type-Options,
frame-ancestors, Referrer-Policy.
Data: minimize (edge never gets owner data), encrypt at rest (AES-GCM, KMS-managed keys), retention policy,
encrypted tested backups in Nepal, lookup logging (who/what/why).
Audit: append-only `audit_log` (app DB role has INSERT only), hash-chained rows, logs who approved/rejected,
original vs edited OCR, timestamps, IP. Four-eyes for plate edits, cancellations, fine changes.
Edge: LUKS, firewall deny-all inbound, non-root services, authenticated NTP, tamper/clock-jump logging, signed OTA only.
Infra: non-root containers, read-only FS, dropped caps, DB/MinIO not internet-exposed, per-service DB roles.
Supply chain: lockfiles, pinned image digests, `gitleaks`, `semgrep`, `bandit`, `pip-audit`, `npm audit`, `trivy` in CI.
Media parsing (ffmpeg/OpenCV/image libs) is a memory-safety risk: keep updated, sandbox decoding where possible.

## Never
- Commit secrets/keys/real personal data; log PII or full tokens; disable TLS verification "temporarily";
  use `eval`/`exec`/`pickle` on untrusted data; catch-and-ignore verification errors; roll your own crypto.

## Gates
Every PR: scanners + tests. Before shadow pilot: OWASP ASVS L2 + Top 10 self-review. Before real fines:
external penetration test + legal review. Fuzz ingestion endpoint and media parsing.

## Incident runbook (write before pilot, /docs/runbooks)
Stolen device -> revoke cert. Leaked credentials -> rotate. Suspected tampering -> freeze + audit.
Breach -> notification process. Test revocation and backup restore at least once.
