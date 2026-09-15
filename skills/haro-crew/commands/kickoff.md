# Kickoff (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew kickoff` and for `/haro-crew` with no args (status section only). Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, always following `shared/qa-rules.md`. Respect `language.response` (chat) and `language.documentation` (docs/code); if either is missing, ask the user first.

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
2. **Interpret back — one response, chat text then tool call last (Turn discipline, `shared/qa-rules.md` §2b; LONG content):**
   - **Block 1 — chat text:** `agent_lead` writes one message in `language.response` containing exactly:
     - `My understanding:` 3–5 lines restating the idea (what the product is, who it serves, the core value).
     - `Assumed goal:` 1 proposed primary goal.
   - **Block 2 — tool call (FINAL, same response):** picker (Mode: single) with short labels only — `Correct, proceed` / `Edit understanding` / `Change goal` — plus free-text, and a one-line pointer such as `Details above. Your call:`. Never compress the interpretation into the picker payload, and never end block 1 without block 2.
3. **Confirm languages:** ask reply language (`vi` | `en`, default `vi`) and content language (`en` | `vi` | `vi-en`, default `en`) — single pickers with defaults pre-suggested. Record into `config/project.yaml`.
4. **Team setup:** when `.haro-crew/config/staffing.yaml` is missing, run `shared/team-setup.md`.
5. **Initialize workspace** (only on first kickoff — never overwrite existing user state):
   - `.haro-crew/config/project.yaml` from `templates/project.yaml` (`name`, `idea`, `goal`, `phase: kickoff`, languages).
   - `.haro-crew/config/staffing.yaml` (from team setup; all `ready`).
   - `.haro-crew/decisions.yaml` from template (empty `decisions: []`).
   - `.haro-crew/tasks.yaml` from template (empty `tasks: []`).
   - `.haro-crew/meetings/`, `.haro-crew/docs/`, `.haro-crew/agents/` directories.
6. **Next-step popup** (Mode: single): `Start discover (recommended)` / `Open web viewer` / `Stop`. On `discover`, read `commands/discover.md` fully first — never act from memory.

## Status — Command `/haro-crew` (no args)

When run with no args (or when kickoff finds an existing workspace):

1. Read `config/project.yaml` → `config/staffing.yaml` → `decisions.yaml` → `tasks.yaml` (read-only).
2. Render in chat: product name + idea (1 line), current phase, decisions count (confirmed vs `[UNCONFIRMED]`), tasks count by status, crew statuses.
3. Picker (Mode: single) with the valid next actions for the current phase (e.g. in `discover` → `Continue discover` / `Open web viewer` / `Stop`). Read the picked command's workflow file fully before acting.
