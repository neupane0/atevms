# 09 Decision Log (ADRs)
Format: ID | Date | Decision | Why | Alternatives | Status

- ADR-001 | 2026-11-21 | Server in Python FastAPI (not Rust) | Faster to build for Phase 0, strong ML/ecosystem fit | Rust Axum (revisit Phase 4 if performance requires) | Accepted (default; human may override)
- ADR-002 | 2026-11-21 | Phase 0 = red-light violation only | Easiest to defend; keeps 30-day scope honest | Multi-violation | Accepted
- ADR-003 | 2026-11-21 | Ed25519-signed manifests + hash-chained events | Hash alone does not stop forgery | SHA-256 only | Accepted
- ADR-004 | 2026-11-21 | Shadow-mode pilot before issuing real fines | Legal risk, trust, data | Direct enforcement | Accepted
- ADR-005 | 2026-11-21 | Mock DoTM registry behind an interface | Real access needs approvals | Wait for real API | Accepted
- ADR-006 | 2026-11-21 | Pydantic v2 and cryptography for contract validation/signatures | Provides strict external-input validation and audited Ed25519/SHA-256 primitives | Hand-built models/crypto or alternative libraries | Accepted
- Contracts adopted from the reviewed package, replacing `server/contract.py` and `tests/test_contract.py` | Reviewed package provides the contract implementation under `server/app/contracts/`; the earlier duplicate is not retained | Keep duplicate implementations or merge compatibility APIs | Accepted
