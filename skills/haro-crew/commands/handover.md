# Handover (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew handover`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, following `shared/qa-rules.md`. The handover pack uses `language.documentation` for docs and `language.response` for the chat summary.

## 6. Command `/haro-crew handover` — Docs + Code + Run Guide

### Workflow

1. **Collect:** read `config/project.yaml`, `decisions.yaml`, `tasks.yaml`, `.haro-crew/docs/`, meeting conclusions, and the built source tree.
2. **Write the handover pack** to `.haro-crew/docs/handover.md`:
   - What was built (feature list ↔ tasks `done`).
   - How to run (prerequisites, env vars, seed, commands — from devops input).
   - Architecture + data model recap (pointers to `architecture.md`, `data-model.md`).
   - Open items: all remaining `[UNCONFIRMED]` decisions + tasks not `done` + QA `pass-with-notes`.
3. **Present in chat** (summary, not full text) + picker: `Accept handover` / `Request fix (free-text)` / `Continue build`.
4. On accept: set `phase: done` in `config/project.yaml`, set all crew `ready` in `staffing.yaml`.
