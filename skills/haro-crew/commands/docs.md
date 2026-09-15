# Docs (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew docs`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, following `shared/qa-rules.md`. Doc content uses `language.documentation`.

## 4. Command `/haro-crew docs` — Minimal Internal Docs Set

Generates the internal docs the build phase implements against. Small, sufficient, no ceremony.

### Files (under `.haro-crew/docs/`)

1. `overview.md` — product, goal, users, success criteria (from decisions + kickoff).
2. `features.md` — feature areas with user stories + acceptance criteria (BA output, meeting-backed).
3. `architecture.md` — components, data entities, API boundaries, stack (arch output, meeting-backed).
4. `data-model.md` — entities, key fields, relationships.
5. `tasks.md` — human-readable task list mirroring `tasks.yaml`.

(`handover.md` is added later by `/haro-crew handover` — see `commands/handover.md`.)

### Workflow

1. **Pre-check:** read `decisions.yaml` + completed meetings. Missing blueprint sign-off → offer: `Run blueprint first (recommended)` / `Draft docs with [UNCONFIRMED] gaps`.
2. **Draft each file** from decisions + meeting conclusions (no new user questions unless a gap blocks everything — then ask with proposals per qa-rules).
3. **Present per file — two turns, chat first (Turn discipline, `shared/qa-rules.md` §2b):** (a) chat-only message with the short brief (not full text; no tool call); (b) picker: `Accept` / `Edit` (free-text) / `Skip file`.
4. **Write** accepted files to `.haro-crew/docs/`; seed `.haro-crew/tasks.yaml` from the task breakdown (each task: id, title, description + acceptance criteria, owner `agent_dev`, `status: pending`).
5. Set `phase: docs` at start, `phase: build` when moving on.
6. **Next-step popup:** `Start build (recommended)` / `Edit a doc` / `Open web viewer` / `Stop`. On build, read `commands/build.md` fully first.
