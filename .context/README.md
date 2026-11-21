# .context: Project Brain for ATEVMS

This folder is the single source of truth for humans and AI assistants (GitHub Copilot, etc.).
If code and these docs disagree, STOP and resolve it. Do not silently pick one.

## Reading order (AI: read in this order at the start of every session)
1. `00_MASTER_PROMPT.md`  - your role, rules, workflow
2. `08_STATE.md`          - where we are RIGHT NOW and the single next task
3. `07_GUARDRAILS.md`     - scope fence and anti-rabbit-hole rules
4. Then only what the task needs: `01`-`06`, `09`

## Files
| File | Purpose | Changes how often |
|---|---|---|
| 00_MASTER_PROMPT.md | Operating instructions for the AI | Rarely |
| 01_PROJECT.md | Mission, Nepal constraints | Rarely |
| 02_ARCHITECTURE.md | Components, stack, pipeline | Per phase |
| 03_CONTRACTS.md | JSON payload, API contracts | Versioned, careful |
| 04_SECURITY.md | Security requirements (mandatory) | Per phase |
| 05_ROADMAP.md | Phases and exit criteria | Monthly |
| 06_STANDARDS.md | Coding standards, testing, git | Rarely |
| 07_GUARDRAILS.md | Scope fence, stop rules, parking lot | Weekly |
| 08_STATE.md | Living status and next task | EVERY session |
| 09_DECISIONS.md | Decision log (ADRs) | When deciding |
| prompts/ | Reusable task prompts | As needed |

## How GitHub Copilot uses this
Copilot does NOT automatically read arbitrary folders. It auto-loads
`.github/copilot-instructions.md` (repo-wide) and `.github/instructions/*.instructions.md`
(path-specific), and `AGENTS.md` for the coding agent. Those files are short and POINT to `.context/`.
In Copilot Chat, attach context explicitly, e.g.:
`#file:.context/00_MASTER_PROMPT.md #file:.context/08_STATE.md`
(Copilot features change; verify current behavior in GitHub's docs.)

## Maintenance rules
- End of every session: update `08_STATE.md` (use `prompts/session_handoff.md`).
- Every non-trivial choice: add an ADR to `09_DECISIONS.md`.
- Anything out of scope the AI discovers goes to the Parking Lot in `07_GUARDRAILS.md`, NOT into code.
