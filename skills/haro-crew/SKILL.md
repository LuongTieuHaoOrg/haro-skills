---
name: haro-crew
description: Turn a one-sentence product idea into a running application with a crew of specialist agents. Use when the user wants to go from idea to docs to code end-to-end (kickoff, discover, blueprint, docs, build, handover) without typing commands or content proactively — the crew asks, the user only picks or types short answers. Run /haro-crew with no args to see status and pick the next action. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Crew — Idea-to-Product Agent Crew Skill

## 1. Overview

`haro-crew` operates a crew of specialist agents like real employees: they receive requirements, analyze, debate in meetings, build, review quality, and report. The user never types commands or drafts content proactively — the crew asks structured questions with proposed answers, and the user only picks an option or types a short answer.

- **Five phases:** KICKOFF → DISCOVER → BLUEPRINT → DOCS → BUILD → LAUNCH/Handover.
- **Single voice:** only `agent_lead` talks to the user, always via question/picker with proposed options plus free-text answer. All specialist agents communicate internally in English.
- **State:** all runtime state lives in `.haro-crew/` at the project root (YAML-first). Markdown payloads carry the content; YAML files are the single source the agents look up.
- **Web viewer:** a view-only static web dashboard under `.haro-crew/web/`, served on localhost so the user can watch progress, agents, tasks, meetings, and docs.

## 2. Workspace `.haro-crew/`

```
.haro-crew/
├── config/
│   ├── project.yaml     # profile: name, idea, phase, language
│   ├── staffing.yaml    # crew roster: agent id | status (ready/busy/offline) | current task
├── decisions.yaml       # confirmed decisions + [UNCONFIRMED] defaults
├── tasks.yaml           # build task queue: pending → doing → review → done
├── agents/              # project agent copies (<id>.md)
├── meetings/            # <meeting_id>/meeting.yaml + rounds/round-<N>-<agent>.md
├── docs/                # internal docs: overview, features, architecture, data-model, tasks
└── web/                 # static viewer (index.html, app.js, styles.css, vendor/, .port)
```

> **Read order (every command):** `config/project.yaml` → `config/staffing.yaml` → `decisions.yaml` → `tasks.yaml` → selectively load meetings/docs payloads. `decisions.yaml` counts as ground truth over guesses. Entries marked `[UNCONFIRMED]` are defaults the user has not confirmed — use them to keep moving, never present them as final.

> **Language settings:** `config/project.yaml` records the **reply language** (`language.response`, default `vi`) and the **content language** (`language.documentation`, default `en`). All user-facing chat uses `language.response`. Docs and code use `language.documentation`. If empty or missing, ask the user before running any command.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row.
> 2. Read that workflow file **fully, before any other tool call or answer** — this file itself runs no workflow.
> 3. If you notice you are about to act, answer, or create anything without the workflow open, **STOP and read it first**. Acting from memory, habit, or a previous session instead of the workflow is a workflow violation: **the workflow always wins over memory**. This applies equally to small/weak models — when in doubt, re-read.

## Presentation rule — chat first, picker second (all commands)

1. Render every content (interpretation, questions context, meeting summaries, task reports) **fully in chat text first**.
2. Pickers hold **choice options only** — short labels (≤1 line each, pointing "see details above"). Never compress content into options to save context.
3. Order is mandatory: chat message(s) first, **then** invoke the picker/question tool — never merged.
4. Every picker declares its mode: `single` by default; `multiple` only where the workflow says so.
5. Every question offers 2–4 proposed answers plus free-text (`type your answer`). Never ask an empty question. See `shared/qa-rules.md`.

## Command index

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-crew` (no args) | Show crew status, current phase, pick next action | `commands/kickoff.md` (status section) | `/haro-crew` |
| `/haro-crew kickoff <idea>` | Start from a one-sentence product idea | `commands/kickoff.md` | `/haro-crew kickoff restaurant management app` |
| `/haro-crew discover` | Deep-dive the 5 axes (goal, users, scale, scope, constraints) | `commands/discover.md` | `/haro-crew discover` |
| `/haro-crew meeting [<topic>]` | Open/resume an internal crew debate on a topic | `commands/meeting.md` | `/haro-crew meeting database choice` |
| `/haro-crew blueprint` | Synthesize meeting output into architecture + stack + scope sign-off | `commands/blueprint.md` | `/haro-crew blueprint` |
| `/haro-crew docs` | Generate the minimal internal docs set | `commands/docs.md` | `/haro-crew docs` |
| `/haro-crew build` | Run the task queue: code each task, QA review, report per task | `commands/build.md` | `/haro-crew build` |
| `/haro-crew handover` | Hand over docs + code + run guide + open items | `commands/handover.md` | `/haro-crew handover` |
| `/haro-crew web` | Open the view-only progress web viewer (localhost) | `commands/web.md` | `/haro-crew web` |
| `/haro-crew web --stop` | Stop the local web server | `commands/web.md` | `/haro-crew web --stop` |

## Crew roster (summary — full personas in `agents/*.md`)

- `agent_lead` — PM/MC. The only agent that talks to the user. Coordinates all phases.
- `agent_ba` — Business analysis, requirements, scope, acceptance criteria.
- `agent_arch` — System architecture, data model, stack selection.
- `agent_uiux` — User journeys, screen flows, interface specs.
- `agent_devops` — Environments, CI/CD, run configuration.
- `agent_dev` — Implements code per task, follows approved docs.
- `agent_qa` — Test strategy, code/doc review, release gate.
