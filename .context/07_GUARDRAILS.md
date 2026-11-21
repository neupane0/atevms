# 07 Guardrails: keeping the AI (and you) out of rabbit holes

## Scope fence
Only work on items listed under "NEXT" or "IN PROGRESS" in `08_STATE.md`. Everything else is parked.

## Stop-and-ask triggers (AI must stop and ask the human)
- Task not mappable to the current phase in `05_ROADMAP.md`.
- Change needs a new dependency, new service, new language, or new architecture component.
- Change touches the JSON contract, auth, crypto, or audit logic beyond the task's stated scope.
- Same problem unresolved after ~3 attempts.
- Requirement involves Nepali law, real DoTM data, real citizen data, or physical hardware.
- You are about to write more than ~300 lines in one step. Split it.

## Forbidden detours
Premature optimization (TensorRT/DeepStream/Rust) before Phase 2; custom model architectures; training from scratch;
building a labeling tool (use the dashboard correction loop or an existing tool); microservices split; Kubernetes;
GraphQL; custom auth; UI polish before the workflow works; perfect Devanagari accuracy in Phase 0.

## Priority order when in doubt
1. Security/evidence integrity  2. Correct end-to-end flow  3. Tests  4. Simplicity  5. Performance  6. Polish

## Parking Lot (ideas/bugs outside current scope; do not implement)
| Date | Item | Source | Target phase |
|---|---|---|---|
| (empty) | | | |
