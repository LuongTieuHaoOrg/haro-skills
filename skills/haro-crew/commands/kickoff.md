# Kickoff (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew kickoff` and for `/haro-crew` with no args (status section only). Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, always following `shared/question-rules.md`. Respect `language.response` (chat) and `language.documentation` (docs/code); if either is missing, ask the user first.

## 0. Command `/haro-crew kickoff <idea>` — Start From One Sentence

### Syntax

```
/haro-crew kickoff restaurant management app
/haro-crew kickoff
```

### Workflow

1. **Capture the idea:**
   - With argument: take `<idea>` as the raw idea.
   - Without argument: ask ONE question with 2–3 example ideas as proposals (e.g. restaurant management app, online course platform, warehouse tracker) + free-text. Wait for the answer.
2. **Initialize workspace FIRST** (only on first kickoff — never overwrite existing user state; must complete before any LONG content is presented):
   - `.haro-crew/config/project.yaml` from `templates/project.yaml` (`name`, `idea`, `goal`, `phase: kickoff`, languages).
   - `.haro-crew/config/staffing.yaml` (from team setup; all `ready`).
   - `.haro-crew/decisions.yaml` from template (empty `decisions: []`).
   - `.haro-crew/knowledge/index.yaml` from template (empty `facts: []`).
   - `.haro-crew/tasks.yaml` from template (empty `tasks: []`).
   - `.haro-crew/meetings/`, `.haro-crew/docs/`, `.haro-crew/output/`, `.haro-crew/knowledge/`, `.haro-crew/agents/` directories.
3. **Interpret back (LONG content — 3-step flow per `shared/question-rules.md`):**
   - **`<render text>`:** `agent_lead` writes exactly this content in `language.response` — and nothing else (anti-narration rule: no planning notes, no meta-commentary):
     - `My understanding:` 3–5 lines restating the idea (what the product is, who it serves, the core value).
     - `Assumed goal:` 1 proposed primary goal.
   - **`<write file>`:** save the same interpretation to `.haro-crew/output/kickoff-interpretation.md`.
   - **`<render popup>`:** picker (Mode: single) with short labels only — `Correct, proceed` / `Edit understanding` / `Change goal` — plus free-text. The question carries the file pointer (e.g. the interpretation just saved, your decision:). Never point "above"; never compress the interpretation into the payload.
4. **Confirm languages:** ask reply language (`vi` | `en`, default `vi`) and content language (`en` | `vi` | `vi-en`, default `en`) — single pickers with defaults pre-suggested. Record into `config/project.yaml`.
5. **Team setup:** when `.haro-crew/config/staffing.yaml` is missing, run `shared/team-setup.md`.
6. **Next-step popup** (Mode: single): `Start discover (recommended)` / `Open web viewer` / `Stop`. On `discover`, read `commands/discover.md` fully first — never act from memory.

## Status — Command `/haro-crew` (no args)

When run with no args (or when kickoff finds an existing workspace):

1. Read `config/project.yaml` → `config/staffing.yaml` → `decisions.yaml` → `tasks.yaml` (read-only).
2. SHORT single picker call per `shared/question-rules.md` (Mode: single, no separate text block): question payload carries the status (product name + idea 1 line, current phase, decisions confirmed vs `[UNCONFIRMED]`, tasks by status, crew statuses) + the valid next actions for the current phase (e.g. in `discover` → `Continue discover` / `Open web viewer` / `Stop`). Read the picked command's workflow file fully before acting.
