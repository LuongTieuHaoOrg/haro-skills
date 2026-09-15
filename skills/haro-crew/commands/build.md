# Build (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew build`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, following `shared/qa-rules.md`. Reports use `language.response`. Never start a task without its acceptance criteria recorded in `tasks.yaml`.

## 5. Command `/haro-crew build` — Task Queue: Code → Review → Report

### Task lifecycle

`pending` → `doing` (agent_dev implements) → `review` (agent_qa verdicts) → `done` (`pass`) or back to `doing` (`fail` + notes). Statuses live only in `.haro-crew/tasks.yaml`.

### Workflow

1. **Pre-check:** read `tasks.yaml` + `docs/` pointers. Empty queue → offer: `Generate docs first` / `Add tasks manually (guided)`.
2. **Pick next task — one response, chat text then tool call last (Turn discipline, `shared/qa-rules.md` §2b):** block 1 = chat text with the queue (id | title | status); block 2 (FINAL, same response) = picker (Mode: single): next `pending` task (recommended) / specific task / `stop`.
3. **Implement:** set task `doing`, update `staffing.yaml` (`agent_dev: busy`). Dispatch `agent_dev` with the task brief (description + acceptance criteria + relevant docs pointers). Collect `IMPLEMENTED / TESTS / NOTES`.
4. **Review:** set task `review`, update staffing (`agent_qa: busy`, `agent_dev: ready`). Dispatch `agent_qa` with task + diff + test evidence. Collect `VERDICT / COVERAGE / GAPS / FOLLOW-UPS`; write `review_note` into `tasks.yaml`.
   - `pass` / `pass-with-notes` → `done`.
   - `fail` → back to `doing` with the notes appended; re-run implement once, then report to the user instead of looping forever (max 2 implement attempts per report cycle).
5. **Report per task — one response, chat text then tool call last (Turn discipline, `shared/qa-rules.md` §2b):** block 1 = chat text in `language.response` (what was built, test evidence, QA verdict, files changed); block 2 (FINAL, same response) = picker: `Next task (recommended)` / `Fix notes now` / `Pause build` / `Stop`.
6. Set `phase: build` at start. When all tasks are `done` → suggest `handover`.

### Examples

```
/haro-crew build
```
