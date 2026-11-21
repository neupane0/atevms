# 06 Coding Standards

## General
- Small, single-purpose functions; explicit types everywhere; no global mutable state; no magic numbers (config/constants).
- Config via environment (pydantic-settings); `.env.example` committed, `.env` git-ignored.
- Structured logging (JSON), no PII/secrets in logs. Use UTC timestamps (ISO-8601 with Z) everywhere.
- Errors: raise specific exceptions; never bare `except:`; never swallow verification failures.
- Dependency injection for external systems (registry, storage, clock) so they are mockable.

## Python (server + edge)
- 3.11+, `ruff` (lint+format), `mypy --strict`, `pytest` (+ `pytest-cov`, `hypothesis` for parsers), `bandit`.
- Pydantic v2 models for all external input; `extra="forbid"`.
- Async for server I/O; edge uses worker threads/processes with bounded queues (backpressure, no unbounded memory).
- Edge code must be deterministic and resilient: handle camera dropout, power loss (atomic writes, fsync, WAL), full disk.

## TypeScript (dashboard)
- `strict: true`, ESLint, no `any`, no `dangerouslySetInnerHTML`. Escape all plate text. Auth tokens never in localStorage.

## Testing
- Pyramid: many unit, some integration (docker-compose), few e2e (recorded video -> edge -> server -> dashboard).
- Required per feature: happy path + failure + abuse case (tampered hash, replayed event, malformed plate, IDOR attempt).
- ML: keep a frozen held-out test set; report precision/recall per class/script/lighting. Never tune on the test set.
- Golden files for evidence packaging and signature verification.

## Git
- Branches: `feat/*`, `fix/*`, `sec/*`. PRs required; protected `main`; signed commits; Conventional Commits.
- PR template includes security checklist. One logical change per PR (small!).

## Docs
- Every module has a short README with how to run/test. ADR for decisions. Update `08_STATE.md` each session.
