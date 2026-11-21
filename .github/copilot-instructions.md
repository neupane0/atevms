# Copilot instructions: ATEVMS (Nepal Automated Traffic Enforcement & e-Challan)

You are pair-programming on an edge-AI traffic enforcement system. Full context lives in `.context/`.
ALWAYS consult, in order: `.context/00_MASTER_PROMPT.md`, `.context/08_STATE.md`, `.context/07_GUARDRAILS.md`.
Consult `.context/03_CONTRACTS.md` for payloads and `.context/04_SECURITY.md` for security rules.

Essentials:
- Phase 0 scope: red-light violation only, one intersection, recorded video. Anything else goes to the Parking Lot, not code.
- Stack defaults: Python 3.11 + FastAPI + Pydantic v2 + PostgreSQL + MinIO; Next.js + strict TypeScript; edge in Python.
- Security is mandatory: strict input validation (extra="forbid"), parameterized SQL, deny-by-default authz, mTLS for devices,
  Ed25519-signed evidence manifests, SHA-256 verification with constant-time compare, append-only audit log, no secrets or real PII in code.
- Plate/OCR text is untrusted input; validate and escape everywhere.
- Heavy inference runs on the edge; never stream raw video to the server. Data stays in Nepal.
- Do not add dependencies, services, or architecture without asking. No refactors outside the task.
- Small changes (<~300 lines), with tests for happy, failure, and abuse paths. Ask before guessing; say "I don't know" when unsure.
- Never invent facts about Nepali law, DoTM systems, or plate formats; mark `TODO(verify)`.
- Stuck after ~3 attempts: stop, summarize, give options, ask.
- Update `.context/08_STATE.md` at the end of each task.
