# QA rules (mandatory for every user-facing question in haro-crew)

> Only `agent_lead` talks to the user. Every question below applies to `agent_lead` output.
> Specialist agents never address the user directly.

## 1. Never ask an empty question

Every question MUST ship with 2–4 proposed answers derived from context (project idea, prior decisions, domain knowledge). The user picks one or types their own answer. A question without proposals is a workflow violation.

## 2. Picker format

1. Render the full context and the proposals **in chat text first** (in `language.response`).
2. Then invoke the question/picker tool: short option labels (≤1 line each, detail lives in chat) + free-text answer enabled (`type your answer`).
3. Declare Mode: `single` by default, `multiple` only when the workflow says so.

## 2b. Turn discipline — "chat first, picker second" (hard rule, no exceptions)

- **One response, ordered blocks, tool call LAST.** A step that asks the user is a single response containing N blocks in strict order: `[chat text block(s) first ...] → [question/picker tool call as the FINAL block]`. The harness renders text first, popup second — the user gets both content and popup. Never split asking into two separate responses (the second one may never run).
- **The tool call is MANDATORY.** Every asking step MUST end with one picker/question tool call (or a numbered list when the runtime has no tool). Presenting content and stopping without calling the tool is a violation — equal to stuffing everything into the payload.
- **Two-level payload policy:**
  - **SHORT (content allowed in payload):** the whole payload (question + all options) fits in ~200 characters, each label ≤1 line, self-explanatory with nothing to add — e.g. confirmations, hub navigation, save/skip, next-step with nothing to report. No separate chat text required.
  - **LONG (chat text required):** needs explanation, evidence, or multi-line structure (interpretations, assessments, outlines, reports, summaries, sign-off packs). Full content goes in chat text block(s) FIRST; the picker payload carries only a one-line pointer (e.g. `Details above. Your call:`) + short labels + free-text. Never compress LONG content into the payload.
- Anti-patterns (violations): (1) picker with long content stuffed into its payload; (2) chat text sent with no tool call after it — the user reads but can never answer.

## 3. Handling unsure / skip

- `unsure` / `skip` are always valid implicit options — never force the user to guess.
- On `unsure`/`skip`: the agent fills the best default, records it in `decisions.yaml` with `status: unconfirmed`, and marks it `[UNCONFIRMED]` wherever shown. The flow NEVER blocks on an unanswered question.
- Re-surface all `[UNCONFIRMED]` items at blueprint sign-off and at handover.

## 4. Language

- Chat, questions, options, summaries: `language.response` (default Vietnamese).
- Internal agent-to-agent prompts, docs, code: English (or `language.documentation`).
- When presenting an English-origin summary to the user, `agent_lead` translates it into `language.response`.
