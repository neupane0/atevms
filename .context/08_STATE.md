# 08 Current State (UPDATE EVERY SESSION)

- Phase: 0 (Demo MVP)
- Day: 1 of 30
- Last updated: 2026-11-21
- Environment: TBD (Jetson? laptop GPU? footage available?)

## DONE
- [x] Create monorepo skeleton, `.gitignore`, `.env.example`, pre-commit (gitleaks, ruff), GitHub Actions with security scanners.
- [x] Write the Phase 0 threat model (`docs/threat-model.md`).
- [x] Add Pydantic v2 contract v1.1 validation, canonical JSON, Ed25519 sign/verify, and focused tests.
- [x] Adopt reviewed contract implementation under `server/app/contracts/`.

## IN PROGRESS
- (none)

## NEXT (single next task; AI works on this only)
1. Server skeleton: FastAPI, Postgres, MinIO, docker-compose

## BACKLOG (Phase 0, in order)
1. Server skeleton: FastAPI, Postgres, MinIO, docker-compose
2. Ingestion endpoint with mTLS, schema, signature, hash, replay checks
3. Mock DoTM registry (fake data) behind an interface
4. Auth: Argon2id, TOTP MFA, RBAC, audit log (append-only)
5. Edge: ring buffer, detector + tracker, stop-line + signal rule, evidence packager, outbox + sync
6. ANPR: plate detector, OCR (English first, then Devanagari), plate regex + normalizer
7. Dashboard: queue, editable plate, approve/reject, e-Challan PDF + QR
8. E2E demo script + metrics report

## BLOCKERS / HUMAN TODO
- Collect intersection footage and plate images (start now)
- Decide server language default (Python FastAPI assumed; see ADR-001)
- TODO(verify): plate zone/letter/province mappings in `server/app/contracts/plates.py`
- TODO(verify): plate colour enum values in `server/app/contracts/models.py`
- TODO(verify): legal basis for camera-evidence fines

## Open TODO(verify) list
- [human/legal] Legal basis for camera-evidence fines.
- [human/DoTM] Plate zone/letter/province mappings in `server/app/contracts/plates.py`.
- [human/DoTM] Plate colour enum values in `server/app/contracts/models.py`.
- [human/infrastructure] Approved Nepal data-residence location and validation method.
