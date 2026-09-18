# Plan (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew plan`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user (in `language.response`), always following `shared/question-rules.md`. Specialists communicate in English. Every question ships with 2–4 proposed answers + free-text. `unsure`/`skip` are always valid — fill the best domain default, record as `unconfirmed` (`[UNCONFIRMED]`), never block. Never re-ask anything already `confirmed` unless a new concrete contradiction forces it — then name the contradiction in the question.

## Command `/haro-crew plan [<idea|topic>]` — Collect → Debate → Blueprint

State-driven: read state first, then enter at the earliest unfinished step. Three steps run in order; each step hands its records to the next.

### Syntax

```
/haro-crew plan
/haro-crew plan restaurant management app
/haro-crew plan database choice for orders module
```

### Entry (read state, then route)

> Assumes SKILL harness steps 1–2 done (workspace + language). If `project.yaml` is still missing → STOP, return to SKILL harness. This command is always allowed (creates the idea if none exists).

1. Read `config/project.yaml` → `decisions.yaml` → scan `.haro-crew/meetings/*/meeting.yaml` (read-only).
2. **With-arg case:** if the arg reads as a product idea (no plan exists yet) → treat as the idea, record into `config/project.yaml`, enter Step 1. If it reads as a debate topic (plan exists) → confirm interpretation per Response Loop (`shared/question-rules.md` §1–§3): `<respond>` with the interpretation, then write `temp/q-<NN>-<slug>.md` FIRST, then picker `Discuss '<topic>'? Confirm / Edit`, then enter Step 2 with that topic.
3. **No-args case:** enter at the earliest unfinished step — no plan records → Step 1; Step 1 done-checklist incomplete → Step 1 (only the missing axes); Step 1 done, no completed meeting → Step 2; meeting done, no blueprint sign-off → Step 3; sign-off recorded → report done and propose `Generate docs`.
4. Set `phase: plan` in `config/project.yaml` at start.

### Step 1 — Discover / Collect (enough to write the business view)

Goal: converge on the user's business requirements. The loop is `ask → answer → think → ask/suggest → answer → … → done → Step 2`. There is NO cap on rounds — ask until the coverage map is full or the user declares done.

1. **Coverage map (starts with 5 axes, grows):** Goal (why, what success looks like) / Users (who, which roles) / Scale (size, load, daily transactions) / Scope (feature areas in AND explicitly out) / Constraints (timeline, hosting, integrations, budget). The agent studies each answer and MAY add further areas the user has not thought of yet (e.g. payments, shifts, stock, reports, permissions) — each added area must cite the answer it was inferred from (`From your answer X, Y looks missing, I suggest Z`).
2. **Ask:** one topic per round. Merge into a multi-form (Mode: multiple) picker whenever the questions are independent (no branching on each other); split into single-question rounds only when the next question branches on the previous answer. Scope features always use Mode: multiple + free-text additions.
3. **Think (mandatory, internal, never narrated in chat):** after every answer — (a) record immediately into `decisions.yaml` (`axis | question | answer | status: confirmed|unconfirmed | decided_at`); (b) update the coverage map; (c) choose exactly one next move: dig deeper into the current axis / open a newly inferred area / summarize and ask for done.
4. **Progress line:** every round opens with one line of status in `language.response` (e.g. `Clear so far: 6/8 areas — still missing: payments, permissions.`). The user always knows where the loop stands.
5. **Done (tiered exit):** every round ends with a picker `Nothing more / Move to debate` / continue-current-axis per `shared/question-rules.md` — offered as soon as the hard gate below is satisfied, so the user can exit at any time. Coverage-complete fast-path: all 5 base axes answered (confirmed, or unconfirmed with defaults) AND the agent has no further inferred area to propose. Early exit is always honored for everything EXCEPT the hard gate: gaps are recorded as `[UNCONFIRMED]` for Step 2. Hard gate: Goal and Scope in/out must have answers (even unconfirmed) before Step 2 — if the user declares done with a gate item missing, run ONE targeted round asking only the missing gate items, then proceed.
6. **Write-through:** Step 1 maintains `.haro-crew/docs/01-proposal/problem.md`, `scope.md` (SSOT for scope — nothing else copies scope text, everything else points here), `timeline.md`, and `.haro-crew/docs/02-requirements/users.md` as it goes (start each file from its skeleton in the skill's `templates/docs/`). Every round follows the Response Loop (`shared/question-rules.md` §1–§3): `<respond>` (ack where the last answer was recorded + progress line per item 4) → write `temp/q-<NN>-<slug>.md` FIRST → `<render popup>`.

### Step 2 — Discuss / Debate (enough to close features + draft the technical view)

Goal: challenge, counter-argue, and close every Step 1 record. Runs ALWAYS in full — including personal projects — because this is where "user remembered 5, system needs 10" gets fixed.

1. **Setup:** participants from `config/staffing.yaml` (default: ba + arch + uiux + devops + qa; personal default may run lean: ba + arch). If staffing is missing, run `shared/team-setup.md` first. Chair is `agent_lead`. If the entry arg is a topic, debate that topic; otherwise the chair derives topics from Step 1 gaps and `[UNCONFIRMED]` items.
2. **Artifacts:** each meeting lives at `.haro-crew/meetings/MT-YYYYMMDD-HHmmss-<slug>/` from `templates/meeting.yaml` (`status: in-progress`) + `rounds/` subdir. Resuming an `in-progress` meeting: per Response Loop (`shared/question-rules.md` §1–§3) — `<respond>` with the list (id | topic | current round), then write `temp/q-<NN>-<slug>.md` FIRST, then picker `Resume <id>` / `New meeting`. Chair saves each participant's analysis verbatim to `rounds/round-<N>-<agent_id>.md`, records a 1–2 line English `recap` + `raw_file` pointer plus the structured `summary_of_round` (`consensus | conflicts_or_disputes | key_takeaways | open_questions_for_next_round`) in `meeting.yaml`. Inter-round context is prior summaries + recaps only — never full raw history.
3. **Debate loop (round-robin, capped):** max 2 rounds per topic. Each round ends per Response Loop (`shared/question-rules.md` §1–§3): `<respond>` with the translated summary in `language.response`, then write `temp/q-<NN>-<slug>.md` FIRST, then `<render popup>` picker `Next round` / `Redirect` (free-text) / `Conclude`. On conclude: write `conclusion`, set `status: completed`.
4. **Step 1 revision rule:** Step 2 MAY send records back to Step 1 (mark decision `unconfirmed` + reason) — max ONE revert per decision; the second touch of the same decision requires an explicit user pick. No B1↔B2 ping-pong without the user.
5. **Done:** scope boundaries + architecture direction + stack direction all closed (or explicitly `[UNCONFIRMED]` with owner), or the user picks `Close and move to blueprint`. Write-through: `.haro-crew/docs/02-requirements/features.md` (features + short AC — SSOT for acceptance) and `open-items.md` (auto-regenerated `[UNCONFIRMED]` list), each started from its skeleton in the skill's `templates/docs/`.

### Step 3 — Blueprint (business + technical sufficient for docs)

Goal: validate the design frame and sign it off once — the output must carry enough business + technical content to write the docs (idea, goals, key points) without asking again.

1. **Pre-check:** read `decisions.yaml` + completed meetings. Missing Step 1 gate items → back to Step 1 (only the missing items). Missing debate coverage → back to Step 2 (only the missing topics).
2. **Sign-off pack (per Response Loop, `shared/question-rules.md` §1–§3, exactly ONCE):**
   - **`<respond>`** (prescribed content only, anti-narration):
     - `Idea / Goals:` 2–4 lines.
     - `Scope:` in/out lists (point to `scope.md`, do not retype at length) + open scope questions.
     - `Architecture:` components, data entities, key API/page boundaries (5–10 lines).
     - `Stack:` choice + one-line trade-off (default Next.js + PostgreSQL unless constraints decided otherwise).
     - `[UNCONFIRMED] items:` every default never confirmed, each with its `Confirm` / `Change` path.
   - **Write Q file FIRST:** write the full pack Q&A to `temp/q-<NN>-blueprint-signoff.md` (schema per §3), then:
   - **`<render popup>`:** single batch picker — `Approve all` / `Fix step 1` (free-text) / `Fix step 2` (free-text) / `Re-meet one topic`. One popup for the whole pack, never per-item popups.
3. **Record:** write approvals into `decisions.yaml` (`axis: scope|architecture|stack`, `status: confirmed`), write `.haro-crew/docs/03-design/architecture.md` + `data-model.md` (start each file from its skeleton in the skill's `templates/docs/`), set `phase: docs`. Then list the `temp/q-*.md` files created during plan in chat so the user can delete them if wanted.
4. **Next-step popup:** `Generate docs (recommended)` / `Re-meet a topic` / `Open web viewer` / `Stop`. On docs, read `commands/docs.md` fully first.

### Examples

```
/haro-crew plan
/haro-crew plan restaurant management app
/haro-crew plan database choice for orders module
```
