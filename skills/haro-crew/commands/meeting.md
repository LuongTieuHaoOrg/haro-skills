# Meeting (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew meeting`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user (in `language.response`), following `shared/question-rules.md`. Specialists communicate in English. Specialists never read raw history — the chair injects targeted context per turn.

## 2. Command `/haro-crew meeting [<topic>]` — Internal Crew Debate

### Storage

- Each meeting lives at `.haro-crew/meetings/<meeting_id>/` with `meeting.yaml` (metadata, `status: in-progress|completed`, structured round summaries) and `rounds/round-<N>-<agent_id>.md` (verbatim raw answers).
- Raw files are the archive. Inter-round context is the prior round summary + recaps only — never full raw history.

### Syntax

```
/haro-crew meeting
/haro-crew meeting database choice for orders module
```

### Workflow

1. **No-args case:** scan `.haro-crew/meetings/*/meeting.yaml` for `status: in-progress`. If found — one response, chat text then tool call last (Turn discipline, `shared/qa-rules.md` §2b): block 1 = chat text listing the in-progress meetings (id | topic | current round); block 2 (FINAL) = picker with `Resume <id>` options plus `New meeting`. If none (or user picks new), ask topic (1 question + free-text) then goal (1 question + free-text), each as its own chat-then-tool pair. SHORT lists may live in the picker payload directly (SHORT level).
   **With-arg case:** confirm interpretation: `Discuss '<topic>'? [Confirm / Edit]` then `Goal '<goal>'? [Confirm / Enter goal]`.
2. **Participants:** list active crew from `config/staffing.yaml` for multi-pick (default: ba + arch + uiux + devops + qa). If staffing is missing, run `shared/team-setup.md` first. Confirm the chair (default `agent_lead`).
3. **Init artifact:** create `.haro-crew/meetings/MT-YYYYMMDD-HHmmss-<slug>/` from `templates/meeting.yaml` (`status: in-progress`) + `rounds/` subdir. For resume: load the file, verify rounds, continue at the next round number.
4. **Health check:** chair pings each participant in English (`You are invited to a crew meeting about '<topic>'. Acknowledge readiness.`). Slow/incoherent response → warn the user in chat with options: `Replace agent` / `Switch model` / `Proceed anyway`.
5. **Debate loop (round-robin):**
   - Chair opens the round with the brief + meeting rules (structured points/arguments/examples; no raw code dumps; stay on profession).
   - Each participant writes its analysis; chair saves it verbatim to `rounds/round-<N>-<agent>.md` and records a 1–2 line English `recap` + `raw_file` pointer in `meeting.yaml`.
   - Chair writes the structured `summary_of_round` in English (`consensus | conflicts_or_disputes | key_takeaways | open_questions_for_next_round`).
   - Chair translates the summary into `language.response` as the chat text block, then closes the SAME response with the picker tool call (FINAL): `Next round` / `Redirect` (free-text instruction) / `Conclude meeting`, with a one-line pointer such as `Summary above. Your call:`. On conclude: write `conclusion`, set `status: completed`.
6. Next-step popup per qa-rules. Set `phase: blueprint` in `config/project.yaml` when the meeting serves blueprint.
