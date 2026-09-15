# Blueprint (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew blueprint`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, following `shared/qa-rules.md`. All synthesis shown to the user is in `language.response`.

## 3. Command `/haro-crew blueprint` — Architecture + Stack + Scope Sign-off

### Workflow

1. **Pre-check:** read `decisions.yaml`. If the 5 discover axes are not all recorded, warn in chat and offer: `Back to discover` / `Proceed with gaps as [UNCONFIRMED]`.
2. **Run the debate:** ensure one completed meeting covering at minimum: scope boundaries, architecture + data model, stack choice. If no such meeting exists, run `commands/meeting.md` (topics: `product scope`, `architecture and stack`) and return here after conclusion.
3. **Synthesize sign-off pack — two turns, chat first (Turn discipline, `shared/qa-rules.md` §2b):**
   - **(a) Chat-only turn (no tool call):** render the full pack:
     - `Scope:` in/out lists + open scope questions.
     - `Architecture:` components, data entities, key API boundaries (5–10 lines).
     - `Stack:` choice + one-line trade-off (default Next.js + PostgreSQL unless constraints decided otherwise).
     - `[UNCONFIRMED] items:` every default the user never confirmed, each with its `Confirm` / `Change` path.
   - **(b) Picker turn (only after (a) is sent):** Mode single per item or batch — `Approve all` / `Change item` (free-text) / `Re-meet on item`. Short labels only; never repeat the pack inside the picker payload.
4. **Record:** write approvals into `decisions.yaml` (`axis: stack|architecture|scope`, `status: confirmed`), set `phase: docs` when moving on to docs.
5. **Next-step popup:** `Generate docs (recommended)` / `Re-meet a topic` / `Open web viewer` / `Stop`. On docs, read `commands/docs.md` fully first.
