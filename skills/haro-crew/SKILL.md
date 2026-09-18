---
name: haro-crew
description: Turn a one-sentence product idea into a running application with a crew of specialist agents. Use when the user wants to go from idea to client-ready docs to working code via four commands (index, plan, docs, build) plus a view-only web viewer — the crew asks structured questions with proposed answers, and the user only picks an option or types a short answer. Run /haro-crew with no args to index the project, pick the reply language first, then continue. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Crew — Idea-to-Product Agent Crew Skill

## Harness (runs before and during every command, in order — no exceptions)

1. Response loop: every turn after a user input runs `shared/question-rules.md` §1 (`<respond>` → `<decide>` → `<ask>` via `temp/q-*.md` file first, picker second). Only `agent_lead` talks to the user. Exception: short confirmations (`OK`, `Stop`, `Next`, verbatim option pick) may skip `<respond>`.
2. Workspace: if `.haro-crew/config/project.yaml` is missing → run first-time init exactly as `commands/index.md` (create workspace from templates, ask reply + content language per question-rules, record + lock, ask product idea), then continue to step 4. Never create workspace any other way.
3. Language: if `language.response` or `language.documentation` is empty/missing → ask BEFORE anything else (single picker with defaults `vi`/`en` per `shared/question-rules.md`), record into `project.yaml` and lock, then continue. If present → only read, never re-ask.
4. Dispatch: match the user's command to exactly one row in Command index, read that workflow file fully, then run it. Never act from memory.

## Rules (must follow — details in `shared/question-rules.md`)

5. Read order every command (after harness): `config/project.yaml` → `config/staffing.yaml` → `decisions.yaml` → `tasks.yaml`, then load only needed meetings/docs. `decisions.yaml` wins over guesses; `[UNCONFIRMED]` = default not confirmed, never present as final.
6. Language: chat uses `language.response`; docs/code use `language.documentation`. Locked at first run, later commands only read.
7. Presentation: every question runs the Response Loop — `<respond>` in chat, then write `temp/q-<NN>-<slug>.md` FIRST, then `<render popup>` (question + options only). 2–4 proposed answers + free-text; Mode `single` by default; never re-ask `confirmed` unless a new concrete contradiction is named.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is the harness + router. No workflow runs here.
>
> 1. Run harness steps 1–3 first (response loop governs every turn; workspace, then language) — before any other tool call or answer.
> 2. Match the user's command to exactly one table row.
> 3. Read that workflow file **fully** — this file itself runs no workflow.
> 4. If you notice you are about to act, answer, or create anything without the workflow open, **STOP and read it first**. Acting from memory, habit, or a previous session instead of the workflow is a workflow violation: **the workflow always wins over memory**. This applies equally to small/weak models — when in doubt, re-read.

## Command index

| Command                           | When to use                                                                                                             | Read first (fully, before acting) | Example                                     |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------|-----------------------------------|---------------------------------------------|
| `/haro-crew` (no args)            | Index the project, pick the reply language first, then propose the next action from current state                       | `commands/index.md`               | `/haro-crew`                                |
| `/haro-crew plan [<idea\|topic>]` | State-driven planning: collect requirements → debate them → sign off the blueprint                                      | `commands/plan.md`                | `/haro-crew plan restaurant management app` |
| `/haro-crew docs`                 | State-driven docs: write the atomic docs set, regen the `_views/` client exports                                        | `commands/docs.md`                | `/haro-crew docs`                           |
| `/haro-crew build`                | State-driven build: create tasks if empty, run the queue (code → review → report), regen progress, hand over at the end | `commands/build.md`               | `/haro-crew build`                          |
| `/haro-crew web`                  | Open the view-only progress web viewer (localhost)                                                                      | `commands/web.md`                 | `/haro-crew web`                            |
| `/haro-crew web --stop`           | Stop the local web server                                                                                               | `commands/web.md`                 | `/haro-crew web --stop`                     |

> Details (workspace layout, language, crew roster): see `shared/skill-overview.md`.
