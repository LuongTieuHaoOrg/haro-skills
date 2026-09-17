---
name: haro-crew
description: Turn a one-sentence product idea into a running application with a crew of specialist agents. Use when the user wants to go from idea to client-ready docs to working code via four commands (index, plan, docs, build) plus a view-only web viewer — the crew asks structured questions with proposed answers, and the user only picks an option or types a short answer. Run /haro-crew with no args to index the project, pick the reply language first, then continue. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Crew — Idea-to-Product Agent Crew Skill

## 1. Overview

`haro-crew` operates a crew of specialist agents like real employees: they receive requirements, analyze, debate in meetings, build, review quality, and report. The user never types commands or drafts content proactively — the crew asks structured questions with proposed answers, and the user only picks an option or types a short answer. Built for small and medium projects (outsourcing, freelancing, personal) — docs are just enough to close the deal, track progress, and hand over, not enterprise ceremony (that is `haro-docs` territory).

- **Four commands:** INDEX (`/haro-crew`) → PLAN (`collect → debate → blueprint`) → DOCS → BUILD (includes handover) → optional WEB viewer.
- **Single voice:** only `agent_lead` talks to the user, always via question/picker with proposed options plus free-text answer (following `shared/question-rules.md`). All specialist agents communicate internally in English.
- **State:** all runtime state lives in `.haro-crew/` at the project root (YAML-first). Markdown payloads carry the content; YAML files are the single source the agents look up.
- **Docs:** atomic files under `.haro-crew/docs/` (one fact in exactly one place — never duplicate). Client-facing exports are regen-only views under `.haro-crew/docs/_views/` (never hand-edited).
- **Web viewer:** a view-only static web dashboard under `.haro-crew/web/`, served on localhost so the user can watch progress, agents, tasks, meetings, and docs.

## 2. Workspace `.haro-crew/`

```
.haro-crew/
├── config/
│   ├── project.yaml     # profile: name, idea, phase, language, project_type (outsource/freelance/personal)
│   ├── staffing.yaml    # crew roster: agent id | status (ready/busy/offline) | current task
├── decisions.yaml       # confirmed decisions + [UNCONFIRMED] defaults
├── knowledge/           # project knowledge memory (index.yaml + domain facts)
├── tasks.yaml           # build task queue: pending → doing → review → done (SSOT for progress)
├── agents/              # project agent copies (<id>.md)
├── meetings/            # <meeting_id>/meeting.yaml + rounds/round-<N>-<agent>.md
├── temp/                # LONG-content work files (kept; agent_lead lists them for user cleanup when each command finishes — never sent to clients)
├── docs/                # atomic internal docs (one fact, one place)
│   ├── 01-proposal/
│   │   ├── problem.md   # problem + goal (plan step 1)
│   │   ├── scope.md     # in/out — SSOT for scope
│   │   └── timeline.md  # milestones + schedule
│   ├── 02-requirements/
│   │   ├── users.md     # roles + needs
│   │   ├── features.md  # features + short acceptance criteria — SSOT for acceptance
│   │   └── open-items.md # auto-regenerated [UNCONFIRMED] + open questions
│   ├── 03-design/
│   │   ├── architecture.md # components + main flows + stack + why
│   │   └── data-model.md   # entities + key fields
│   └── _views/          # regen-only client exports (never hand-edited)
│       ├── 01-proposal.md     # deal: problem, solution, scope summary, milestones, terms (no price)
│       ├── 02-pricing.md      # deal, optional: items | price | payment milestones | warranty
│       ├── 03-business.md     # non-tech: problem + scope + users + lean features + timeline
│       ├── 04-technical.md    # dev/tech: architecture + data model + features with AC + scope
│       ├── 05-progress.md     # tracking: feature | status | demo link | note (filtered, no secrets)
│       └── 06-handover.md     # handover: what was built, how to run, what is delivered, open items, warranty
└── web/                 # static viewer (index.html, app.js, styles.css, vendor/, .port)
```

> **Read order (every command):** `config/project.yaml` → `config/staffing.yaml` → `decisions.yaml` → `tasks.yaml` → selectively load only the meetings/docs payloads the step needs (never the whole tree). `decisions.yaml` counts as ground truth over guesses. Entries marked `[UNCONFIRMED]` are defaults the user has not confirmed — use them to keep moving, never present them as final.

> **Language settings:** `config/project.yaml` records the **reply language** (`language.response`, default `vi`) and the **content language** (`language.documentation`, default `en`). All user-facing chat uses `language.response`. Docs and code use `language.documentation`. The reply language is picked FIRST in `/haro-crew` (index) and locked there — later commands never ask again, they only read it.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row.
> 2. Read that workflow file **fully, before any other tool call or answer** — this file itself runs no workflow.
> 3. If you notice you are about to act, answer, or create anything without the workflow open, **STOP and read it first**. Acting from memory, habit, or a previous session instead of the workflow is a workflow violation: **the workflow always wins over memory**. This applies equally to small/weak models — when in doubt, re-read.

## Presentation rule — content routing per `shared/question-rules.md` (all commands)

1. **SHORT content** (confirmations, navigation, save/skip — whole payload ≤ ~200 chars): single picker call with the content embedded in the question payload. No separate text block.
2. **LONG content** (interpretation, questions context, meeting summaries, task reports — whole payload > ~800 chars or an irreversible sign-off): 3-step flow — `<render text>` (prescribed content only, anti-narration) → `<write file>` under `.haro-crew/temp/` (or the owning workspace path) → `<render popup>` whose question points to the **file path**. Never point "above"; never compress LONG content into options. Between ~200 and ~800 chars, prefer SHORT unless the workflow says otherwise.
3. Every picker declares its mode: `single` by default; `multiple` only where the workflow says so.
4. Every question offers 2–4 proposed answers plus free-text (`type your answer`). Never ask an empty question.
5. Never re-ask anything already `confirmed` in `decisions.yaml` unless a new concrete contradiction forces it — and then the question must name the contradiction.

## Command index

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-crew` (no args) | Index the project, pick the reply language first, then propose the next action from current state | `commands/index.md` | `/haro-crew` |
| `/haro-crew plan [<idea\|topic>]` | State-driven planning: collect requirements → debate them → sign off the blueprint | `commands/plan.md` | `/haro-crew plan restaurant management app` |
| `/haro-crew docs` | State-driven docs: write the atomic docs set, regen the `_views/` client exports | `commands/docs.md` | `/haro-crew docs` |
| `/haro-crew build` | State-driven build: create tasks if empty, run the queue (code → review → report), regen progress, hand over at the end | `commands/build.md` | `/haro-crew build` |
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

Default crew for small projects: `lead + ba + arch + dev` (personal) or `lead + ba + arch + dev + qa` (small outsource). Other agents stay off until needed — enable via team setup in `commands/index.md`.
