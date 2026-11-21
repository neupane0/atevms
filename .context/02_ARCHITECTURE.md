# 02 Architecture

## Default stack (changeable only via ADR in 09_DECISIONS.md)
| Layer | Choice (default) |
|---|---|
| Server | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2 + Alembic |
| DB | PostgreSQL (PostGIS/TimescaleDB later, not Phase 0) |
| Object storage | MinIO (private buckets, versioning/object lock) |
| Dashboard | Next.js + TypeScript (strict) + Tailwind |
| Edge (Phase 0) | Python 3.11, OpenCV, Ultralytics YOLO, ByteTrack, PaddleOCR; TensorRT export for Jetson later |
| Edge queue | SQLite (WAL) outbox |
| Transport | HTTPS with mTLS (REST). MQTT only if an ADR approves it |
| Packaging | Docker Compose for server stack; systemd services on Jetson |
| CI | GitHub Actions |
NOTE: Rust/DeepStream are Phase 2+ optimizations, NOT Phase 0.

## Repo layout
```
/edge        edge pipeline (ingest, detect, track, rules, anpr, evidence, outbox, sync)
/server      API, ingestion, registry mock, e-challan, audit
/dashboard   officer UI
/infra       docker-compose, CA scripts, nginx, CI configs
/docs        threat model, runbooks
/.context    this folder
/tests       cross-component / e2e
```

## Edge pipeline (in order)
1. Ingest RTSP/file at 30+ FPS into a 10s ring buffer (RAM).
2. Detect + track vehicles: motorcycle, car, bus, truck, three_wheeler (ByteTrack/BoT-SORT).
3. Rules engine. PHASE 0: RED_LIGHT_JUMP only = signal_state RED AND tracked vehicle crosses virtual stop_line polygon.
   Signal state in Phase 0 comes from a manual config/timeline file or simple colour detection on video; the real
   optocoupler interface is Phase 2. Later: speed (homography + radar), helmet, wrong-way.
4. Two-stage ANPR: (a) plate detector on vehicle crop; (b) rectify/deskew + OCR (PaddleOCR baseline, fine-tuned
   on Devanagari + English). Output raw text, normalized text, script type, confidence.
5. Evidence: 3 JPEGs (scene, vehicle, plate) + 5s H.265 mp4 (2.5s before/after). SHA-256 each, build manifest,
   sign with device key (Ed25519), include prev_event_hash + monotonic counter, write to outbox.
6. Sync: background worker, retry with backoff, mTLS, idempotent by event_id, buffer 72h offline.

## Server components
- Ingestion: verify mTLS identity, schema, signature, hash chain, media SHA-256, replay/duplicate window, store media in MinIO.
- Dedup: same vehicle/plate within cooldown window => one ticket.
- Mock DoTM registry: realistic fake records (NO real personal data). Behind an interface so a real adapter can replace it.
- Review API + dashboard: verification queue, editable plate field, approve/reject, officer badge ID, audit log.
- e-Challan: PDF with unique QR; simulated SMS/Nagarik/eSewa webhooks.
- Device health: online/offline, battery voltage (Phase 0 may mock).

## Boundaries (do not blur)
- Edge never receives owner data. Server never runs heavy video inference.
- Registry access goes only through the registry interface and is always access-logged.
- All modules talk via documented contracts in `03_CONTRACTS.md`.
