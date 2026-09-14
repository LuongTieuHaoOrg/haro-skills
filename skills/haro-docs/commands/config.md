# Config hub (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs config`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).

## 11. Command `/haro-docs config` — Config Hub (agents | conventions | language)

Central hub for skill configuration. Three branches; doc-root lives only in `.haro-docs/config/project.yaml` (chosen at `init`).

### 11.1 Hub (no args)

```
/haro-docs config               → hub picker (read-only until a branch is chosen)
/haro-docs config agents        → straight into §11.2
/haro-docs config conventions   → straight into §11.3
/haro-docs config language      → straight into §11.4
```

Workflow:

1. Read state: `agents.yaml` (exists? N enabled, default?), Part B of `00-common/01-conventions.md` (6-row table or `missing`), `language.response/documentation` from `.haro-docs/config/project.yaml`.
2. Show picker (Mode: single; picker tool when available, otherwise numbered list), each row with a one-line status:
   - `1. agents — reviewer subagents (N enabled, default: <id>)`
   - `2. conventions — project-specific conventions (diagram, API format, tone, approver...)`
   - `3. language — reply + documentation language`
3. Enter the chosen branch. After a branch finishes, ask `back to hub / stop`. Unknown arg → `Unknown command 'config X'. Valid: agents, conventions, language.` then show the hub.

### 11.2 Branch: agents — Manage Reviewer Subagents

Manage the `.haro-docs/config/agents.yaml` configuration:

1. When the file is missing or holds zero enabled entries, run the shared setup flow in `shared/agent-setup.md` first (it lists presets from `templates/agents.yaml`).
2. Otherwise list as `id | invoke | type/command | role | enabled | default?` (file/model per id via `.haro-docs/agents/index.yaml`).
3. Offer operations (Mode: single; picker when available, otherwise numbered list): `add from template | add custom (blank) | attach existing | tune model | enable / disable | set default_reviewer | export to IDE | reset from template (confirm first)`.
   - add from template: pick a preset from the registry (`templates/agents.yaml`) → name it (lowercase-hyphen, unique) → invoke (preset default) → copy the template file into `.haro-docs/agents/` when missing → write index + registry entries on confirm.
   - add custom (blank): name it → create `.haro-docs/agents/<name>.md` from `agents/_blank.md` for the user to fill → write entries on confirm.
   - attach existing: pick a source — Task runtime type (catalog: sub_reviewer, sub_qc, sub_sec, sub_ba, sub_e2e, sub_uiux, sub_data, sub_arch, explore), or `@command` (typed, or picked from `.claude/agents/*.md` / `.agents/**` when found), or an existing project file → name it → confirm.
   - tune model: edits only the `model:` line in the project copy frontmatter; confirm before writing.
   - export to IDE: copies `.haro-docs/agents/<id>.md` to `.claude/agents/` (Claude Code) or `.agents/`; confirm the target first; never writes outside on its own.
4. After any write, re-render the list and remind that `/haro-docs review` will offer these agents for selection.

### 11.3 Branch: conventions — Set Project-Specific Conventions

Set Part B of `00-common/01-conventions.md` (Part A is fixed by the skill):

1. Show current Part B as table `item | value`; show Part A as 6 bullet titles only (full text on request).
2. Offer per-item values (Mode: single; picker when available, otherwise numbered list): diagram tool | API spec format | tone & depth | RELEASED approver | locked terms | priority deliverables. Each item offers scan-based defaults.
3. `reset` writes Part A fresh from `templates/conventions.md` and **keeps Part B**. Confirm before any write.
4. After writing, suggest `review` for any RELEASED files the new conventions touch — only suggest the `review` command; `config` never writes to doc files.

### 11.4 Branch: language — Reply + Documentation Language

1. Show current `language.response` + `language.documentation` from `.haro-docs/config/project.yaml` (with `vi` vs `vi-en` definitions from shared/authoring.md (§9)).
2. Offer values `en | vi | vi-en` as applicable; confirm before writing back to `.haro-docs/config/project.yaml`.
