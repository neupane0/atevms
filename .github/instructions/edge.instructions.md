---
applyTo: "edge/**"
---
Design for power loss and flaky networks: atomic writes with fsync, SQLite WAL outbox, bounded queues, retry with backoff,
idempotent uploads by event_id. Hash at capture, sign the manifest with the device key, chain events via prev_event_hash and counter.
No owner data on the edge. Phase 0 is Python on recorded video; do not introduce Rust/DeepStream/TensorRT yet.
