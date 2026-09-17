# Index (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew` with no args. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, always following `shared/question-rules.md`. This command is read-only except for first-time workspace init and language lock.

## Command `/haro-crew` (no args) — Index project, language first, propose next action

### Workflow

1. **Locate workspace:** check for `.haro-crew/config/project.yaml` at the project root.
2. **Language first (only when missing):** if `language.response` (or `language.documentation`) is empty or missing, ask it BEFORE anything else — single picker call(s) with defaults pre-suggested: reply language (`vi` | `en`, default `vi`), content language (`en` | `vi` | `vi-en`, default `en`). Record into `config/project.yaml` and lock — later commands read this value and never ask again.
3. **First-time init (only when `.haro-crew/` is missing):** create the workspace without overwriting anything (there is nothing to overwrite):
   - `.haro-crew/config/project.yaml` from `templates/project.yaml` (`name`, `idea` empty, `phase: index`, locked languages, `project_type` empty: `outsource | freelance | personal`).
   - `.haro-crew/config/staffing.yaml` via `shared/team-setup.md` (all `ready`; default crew: `lead + ba + dev`, add `arch + qa` for outsource).
   - `.haro-crew/decisions.yaml` from template (empty `decisions: []`).
   - `.haro-crew/knowledge/index.yaml` from template (empty `facts: []`).
   - `.haro-crew/tasks.yaml` from template (empty `tasks: []`).
   - Directories: `.haro-crew/meetings/`, `.haro-crew/docs/01-proposal/`, `.haro-crew/docs/02-requirements/`, `.haro-crew/docs/03-design/`, `.haro-crew/docs/_views/`, `.haro-crew/temp/`, `.haro-crew/knowledge/`, `.haro-crew/agents/`.
   - Then ask for the product idea: ONE question with 2–3 example ideas as proposals (e.g. restaurant management app, online course platform, warehouse tracker) + free-text. Record it into `config/project.yaml` and propose `Run plan (recommended)` — on pick, read `commands/plan.md` fully first.
4. **Existing workspace (read-only status):** read `config/project.yaml` → `config/staffing.yaml` → `decisions.yaml` → `tasks.yaml` (read-only). Then a SHORT single picker call per `shared/question-rules.md` (Mode: single, no separate text block): the question payload carries the status (product name + idea 1 line, project type, current phase, decisions confirmed vs `[UNCONFIRMED]`, tasks by status, crew statuses) + the valid next actions derived from state:
   - No idea yet → `Run plan with idea` / `Open web viewer` / `Stop`.
   - Idea, no plan sign-off → `Continue plan (recommended)` / `Open web viewer` / `Stop`.
   - Plan signed off, no docs → `Generate docs (recommended)` / `Back to plan` / `Open web viewer` / `Stop`.
   - Docs ready, tasks pending → `Start build (recommended)` / `Edit docs` / `Open web viewer` / `Stop`.
   - Tasks `done` → `View handover` / `Continue build` / `Stop`.
   - Read the picked command's workflow file fully before acting — never act from memory.

### Examples

```
/haro-crew
```
