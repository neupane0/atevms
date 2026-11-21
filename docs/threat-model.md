Found 11 errors.Found 11 errors.# ATEVMS Threat Model (Phase 0)  v0.1

Method: STRIDE per component. Living document: update every phase and after every security-relevant change.
Status key: [P0] implemented/planned in Phase 0, [P2] hardware phase, [P4] before real fines.

## 1. Scope and assumptions
In scope: edge node software, edge-to-server channel, ingestion API, review dashboard, DB + MinIO, officer accounts, evidence.
Assumptions: devices sit in public places and CAN be physically stolen or opened; the network is hostile; officers can be
careless, coerced or corrupt; plates are attacker-controlled text; attackers may include insiders.
Out of scope for Phase 0: nation-state attackers, supply-chain compromise of Jetson firmware, real DoTM interface, physical
attacks on the signal controller (tracked as risks).

## 2. Assets (what we protect, in priority order)
1. Evidence integrity (media + manifest) and its chain of custody
2. Correctness of fines (no forged, deleted or silently altered challans)
3. Officer credentials and audit trail
4. Citizen/owner data returned by registry lookups
5. Device keys and the private CA
6. System availability (cameras keep working through power/network loss)

## 3. Trust boundaries
Camera/scene -> Edge node -> (mTLS) -> Ingestion API -> DB/MinIO -> Review API -> Dashboard (officer browser).
Registry (mock in P0) sits behind an interface on the server side only.

## 4. STRIDE analysis

### 4.1 Edge node
| Threat | Example | Control | Status |
|---|---|---|---|
| Spoofing | Cloned device uploads fake violations | Per-device Ed25519 signing key + mTLS client cert; revocation | [P0] sign, [P2] key in secure storage |
| Tampering | Attacker edits media/manifest on disk | SHA-256 at capture, signed manifest, hash chain (prev_event_hash, counter), LUKS | [P0] chain+sign, [P2] LUKS |
| Repudiation | Operator denies altering clock/config | Authenticated NTP, clock-jump and reboot logging, signed config | [P2] |
| Info disclosure | Stolen device exposes evidence | Full-disk encryption; no owner data ever stored on edge | [P2] |
| DoS | Disk fills, power cut, camera dropout | Bounded queues, atomic writes + WAL, retention cap, graceful low-power | [P0] queues/WAL, [P2] power |
| Elevation | SSH takeover, malicious update | Key-only SSH over VPN, firewall deny-all inbound, signed OTA only, non-root services | [P2] |

### 4.2 Edge-to-server channel
| Threat | Example | Control | Status |
|---|---|---|---|
| Spoofing | Fake server / fake device | mTLS with private CA, pinned CA | [P0] |
| Tampering | Modify payload in transit | TLS + signed manifest verified server-side | [P0] |
| Replay | Resend old violation to create duplicates | event_id idempotency, monotonic counter, timestamp window, chain check | [P0] |
| DoS | Flood ingestion | Rate limits, size limits, per-device quotas | [P0] |

### 4.3 Ingestion API and server
| Threat | Example | Control | Status |
|---|---|---|---|
| Tampering/Injection | Malicious JSON, SQL via plate text | Strict Pydantic (extra=forbid), duplicate-key rejection, parameterized SQL, plate regex allow-list | [P0] (contracts done) |
| Tampering | Malformed media exploits decoder | Magic-byte checks, size limits, sandboxed decoding, patched libs | [P0]/[P4] |
| Info disclosure | Error messages leak internals | Generic errors, structured server-side logging without PII | [P0] |
| Elevation | Broken authorization / IDOR | Deny by default, per-object checks, jurisdiction scoping | [P0] |
| Repudiation | "I never approved that fine" | Append-only hash-chained audit log, officer badge ID per action | [P0] |

### 4.4 Review dashboard and officer accounts
| Threat | Example | Control | Status |
|---|---|---|---|
| Spoofing | Stolen/phished officer password | Argon2id, mandatory TOTP MFA, short sessions, lockout | [P0] |
| Tampering | Officer edits plate to cancel a fine or frame someone | Four-eyes on plate edits/cancellations; original OCR kept in audit | [P0] |
| Info disclosure | Insider looks up owners without cause | Lookup logging (who/what/why), role scoping, alerts on unusual volume | [P0]/[P3] |
| XSS | Malicious plate text rendered in UI/PDF/SMS | Validate + escape everywhere, CSP, no dangerouslySetInnerHTML | [P0] |
| CSRF/session theft | Forged requests | HttpOnly+Secure+SameSite=Strict cookies, CSRF tokens, CORS allow-list | [P0] |

### 4.5 Database and object storage
| Threat | Example | Control | Status |
|---|---|---|---|
| Tampering | Evidence overwritten or deleted | MinIO versioning/object lock (WORM), app role INSERT-only on audit | [P0]/[P3] |
| Info disclosure | DB dump leak | Encryption at rest, field-level encryption for PII, encrypted backups in Nepal | [P3]/[P4] |
| Elevation | App uses superuser role | Per-service least-privilege roles; DB/MinIO not internet-reachable | [P0] |

## 5. Plate-specific attacks (project-specific)
- Adversarial/printed text on plates or stickers (injection payloads, instructions aimed at downstream tools): treated as untrusted data,
  allow-list charset, token-length limits, never executed or interpolated. Tests included.
- Plate swapping/cloning: out of automated scope; mitigated by registry cross-check (vehicle make/colour mismatch flag) in later phases.
- Deliberate occlusion/mud: results in low OCR confidence -> officer review, not auto-fine.

## 6. Residual risks and open questions
- Legal admissibility and basis for camera-evidence fines in Nepal: TODO(verify) with a Nepali lawyer.
- Signature proves the device signed it, not that the scene was truthful; a compromised device can sign false events (mitigate: tamper detection, spot audits, secure key storage).
- Signal state input can be spoofed at the controller interface [P2].
- Canonical JSON depends on Python float formatting (Python-only signers in P0).
- Clock integrity on edge devices.

## 7. Required security gates
Every PR: gitleaks, Semgrep, Bandit, pip-audit, Ruff, tests. Before shadow pilot: OWASP ASVS L2 self-review. Before issuing real fines: external penetration test and legal review.
