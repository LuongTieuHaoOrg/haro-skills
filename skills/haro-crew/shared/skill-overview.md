# Haro Crew — Skill Overview

> File nội dung chi tiết của skill `haro-crew`. `SKILL.md` chỉ giữ router + ràng buộc; mọi chi tiết workspace/crew nằm ở đây.

## 1. Overview

`haro-crew` operates a crew of specialist agents like real employees: they receive requirements, analyze, debate in meetings, build, review quality, and report. The user never types commands or drafts content proactively — the crew asks structured questions with proposed answers, and the user only picks an option or types a short answer. Built for small and medium projects (outsourcing, freelancing, personal) — docs are just enough to close the deal, track progress, and hand over, not enterprise ceremony (that is `haro-docs` territory).

- **Five workflows:** INDEX (`/haro-crew`) → PLAN (`collect → debate → blueprint`) → DOCS → BUILD (includes handover) → optional WEB viewer.
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

> **Language settings:** `config/project.yaml` records the **reply language** (`language.response`, default `vi`) and the **content language** (`language.documentation`, default `en`). Templates leave both empty — the first command that runs asks them per `shared/question-rules.md` (SKILL harness steps 1–2) and locks them. All user-facing chat uses `language.response`. Docs and code use `language.documentation`. Later commands only read, never re-ask.

> **Template skeletons:** each atomic doc starts from its skeleton in the skill's `templates/docs/` (flat dash-names map to nested targets, e.g. `01-proposal-problem.md` → `docs/01-proposal/problem.md`, `02-requirements-features.md` → `docs/02-requirements/features.md`, `03-design-architecture.md` → `docs/03-design/architecture.md`).

## 3. Crew roster (summary — full personas in `agents/*.md`)

- `agent_lead` — PM/MC. The only agent that talks to the user. Coordinates all phases.
- `agent_ba` — Business analysis, requirements, scope, acceptance criteria.
- `agent_arch` — System architecture, data model, stack selection.
- `agent_uiux` — User journeys, screen flows, interface specs.
- `agent_devops` — Environments, CI/CD, run configuration.
- `agent_dev` — Implements code per task, follows approved docs.
- `agent_qa` — Test strategy, code/doc review, release gate.

Default crew for small projects: `lead + ba + arch + dev` (personal) or `lead + ba + arch + dev + qa` (small outsource). Other agents stay off until needed — enable via team setup in `commands/index.md`.
