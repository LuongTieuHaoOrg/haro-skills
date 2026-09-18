# Build (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew build`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, following `shared/question-rules.md`. Reports use `language.response`. Never start a task without its acceptance criteria recorded in `tasks.yaml`.

## Command `/haro-crew build` — Tasks → Queue (Code → Review → Report) → Handover

State-driven: read state first, then propose. Creates tasks when empty, runs the queue, regens the progress view after every task, and writes the handover view when the queue is done (handover lives here — there is no separate handover command).

### Task lifecycle

`pending` → `doing` (agent_dev implements) → `review` (agent_qa verdicts) → `done` (`pass`) or back to `doing` (`fail` + notes). Statuses live only in `.haro-crew/tasks.yaml` (SSOT for progress).

### Workflow

> Assumes SKILL harness steps 1–2 done (workspace + language). If `project.yaml` is still missing → STOP, return to SKILL harness.

1. **Pre-check (entry requirement):** read `tasks.yaml` + `docs/02-requirements/features.md` + `docs/03-design/*` pointers.
   - Empty queue but features exist → seed `tasks.yaml` from the feature breakdown (each task: id, title, description + acceptance criteria, owner `agent_dev`, `status: pending`), then continue below.
   - Empty queue and no features → offer: `Generate docs first (recommended)` / `Add tasks manually (guided)`. Guided mode asks one multi-form (title + description + AC per task) and writes `tasks.yaml` directly.
2. **Pick next task (per `shared/question-rules.md`):** `<render text>` with the queue (id | title | status) → `<write history file>` → single picker (Mode: single): next `pending` task (recommended) / specific task / `stop`. **AC gate:** a task without recorded acceptance criteria is skipped — route it back for requirements instead of implementing.
3. **Implement:** set task `doing`, update `staffing.yaml` (`agent_dev: busy`). Dispatch `agent_dev` with the task brief (description + acceptance criteria + relevant docs pointers). Collect `IMPLEMENTED / TESTS / NOTES`.
4. **Review:** set task `review`, update staffing (`agent_qa: busy`, `agent_dev: ready`). Dispatch `agent_qa` with task + diff + test evidence. Collect `VERDICT / COVERAGE / GAPS / FOLLOW-UPS`; write `review_note` into `tasks.yaml`.
   - `pass` / `pass-with-notes` → `done`.
   - `fail` → back to `doing` with the notes appended; re-run implement once, then report to the user instead of looping forever (max 2 implement attempts per report cycle — one cycle is one task from pick to report).
5. **Report per task (per `shared/question-rules.md`):** `<render text>` in `language.response` (what was built, test evidence, QA verdict, files changed; prescribed content only, anti-narration) → `<write history file>` → `<render popup>` picker `Next task (recommended)` / `Fix notes now` / `Pause build` / `Stop`.
6. **After every task:** regen `.haro-crew/docs/_views/05-progress.md` from `tasks.yaml` (feature | status | demo link | note, filtered — no secrets, no internal detail). This is the only progress file — there is no `docs/progress.md` and no hand-written `tasks.md`.
7. Set `phase: build` at start. When all tasks are `done` → write the handover (no separate command):
   - Collect `config/project.yaml`, `decisions.yaml`, `tasks.yaml`, `.haro-crew/docs/`, meeting conclusions, and the built source tree.
   - Write `.haro-crew/docs/_views/06-handover.md` (the ONLY handover file — there is no `docs/handover.md`): what was built (features ↔ tasks `done`), how to run (prerequisites, env vars, seed, commands — from devops input), architecture + data model recap (pointers to `03-design/*`, never retyped), open items (remaining `[UNCONFIRMED]` + tasks not `done` + QA `pass-with-notes`).
   - Present per `shared/question-rules.md` (pack already persisted in `06-handover.md`): `<render text>` summary in `language.response` → `<write history file>` → `<render popup>` picker `Accept handover` / `Request fix` (free-text) / `Continue build`.
   - On accept: set `phase: done`, set all crew `ready` in `staffing.yaml`, then list the `temp/` files created during build in chat so the user can delete them if wanted.

### Examples

```
/haro-crew build
```
