# ATEVMS

ATEVMS is a Nepal-focused edge-AI traffic enforcement and e-Challan demo.
Phase 0 covers one intersection and red-light violations only.

## Repository layout

- `edge/`: Python edge pipeline for recorded video.
- `server/`: Central FastAPI API and persistence.
- `dashboard/`: Next.js officer review dashboard.
- `infra/`: Local infrastructure configuration.
- `docs/`: Project and operational documentation.

The implementation directories are introduced as each roadmap task begins.
Do not add out-of-scope enforcement features.

## Local setup

```bash
cp .env.example .env
python -m pip install pre-commit
pre-commit install
pre-commit run --all-files
```

Never use real plate, owner, or credential data in repository files.
