# Docs (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew docs`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, following `shared/question-rules.md`. Doc content uses `language.documentation`. Docs are regen views over state — fix the state (`decisions.yaml`, meetings), then regen; never hand-edit a `_views/` file.

## Command `/haro-crew docs` — Atomic docs + client exports

Generates the internal atomic docs the build phase implements against, then regens the `_views/` client exports. Small, sufficient, no ceremony.

> **Lean stop-rule:** docs exist to feed production — stop when dev can code and QA can test from them. No use cases, no formal SAD/FSD, no enterprise paperwork. Depth goes into features/ACs, not documents.

### Files (under `.haro-crew/docs/` — one fact in exactly one place)

Internal atomic docs (SSOT):

1. `01-proposal/problem.md` — problem, goal, success criteria (from plan step 1).
2. `01-proposal/scope.md` — in/out lists — SSOT for scope. Everything else points here, never retypes it.
3. `01-proposal/timeline.md` — milestones + schedule (from constraints).
4. `02-requirements/users.md` — roles + needs (from plan step 1).
5. `02-requirements/features.md` — features with short acceptance criteria (from plan step 2) — SSOT for acceptance.
6. `02-requirements/open-items.md` — auto-regenerated `[UNCONFIRMED]` + open questions (never hand-written).
7. `03-design/architecture.md` — components, main flows, API/page boundaries, stack + why (from plan step 3).
8. `03-design/data-model.md` — entities, key fields, relationships (from plan step 3).

Client exports (regen-only, under `.haro-crew/docs/_views/` — never hand-edited):

1. `01-proposal.md` — deal view: problem, solution, scope summary, milestones, terms (no price). Regen from `01-proposal/*`.
2. `02-pricing.md` — optional, only when the project needs a quote (outsource/freelance; personal skips): items | price | payment milestones | warranty.
3. `03-business.md` — non-tech view: problem + scope + users + lean features + timeline. Regen, no tech detail.
4. `04-technical.md` — dev/tech view: architecture + data model + features with AC + scope. Regen.
5. `05-progress.md` — tracking view: regen from `tasks.yaml` (feature | status | demo link | note, filtered — no secrets, no internal task detail).
6. `06-handover.md` — written at the end of build (see `commands/build.md`), surfaced here for delivery.

### Workflow

> Assumes SKILL harness steps 1–2 done (workspace + language). If `project.yaml` is still missing → STOP, return to SKILL harness.

1. **Pre-check (entry requirement):** read `decisions.yaml` + completed meetings + `config/project.yaml` (`project_type`). Missing plan sign-off → not allowed to draft silently → offer: `Back to plan (recommended)` / `Draft docs with [UNCONFIRMED] gaps`.
2. **Draft the 8 atomic files** from decisions + meeting conclusions (no new user questions unless a gap blocks everything — then ask with proposals per question-rules). Start each file from its skeleton in the skill's `templates/docs/` (same base name); keep each file ≤ ~150 lines; if a file outgrows that, split it (e.g. `features/<name>.md`), never bloat. Other files reference by pointer (`See scope.md`), never by copying long passages.
3. **Pricing gate:** if `project_type` is `personal` (or the user says no quote is needed) → skip `02-pricing.md`. Otherwise ask ONE picker: `Create pricing view? Yes / No`. On yes, draft it from scope + timeline.
4. **Present once (per `shared/question-rules.md`):** `<render text>` with the 8 atomic files + one-line brief each → `<write history file>` → single picker `Accept all` / `Edit` (free-text, names the file) / `Regen a view`. One popup for all files, never per-file popups.
5. **Write** accepted files; regen all `_views/` from the atomic sources; seed `.haro-crew/tasks.yaml` from the feature breakdown (each task: id, title, description + acceptance criteria, owner `agent_dev`, `status: pending`). Then list any `temp/` files in chat so the user can delete them if wanted.
6. Set `phase: docs` at start, `phase: build` when moving on.
7. **Next-step popup:** `Start build (recommended)` / `Edit a doc` / `Open web viewer` / `Stop`. On build, read `commands/build.md` fully first.

### Examples

```
/haro-crew docs
```
