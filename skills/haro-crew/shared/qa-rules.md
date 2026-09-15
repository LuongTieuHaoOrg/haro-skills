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

- The chat message and the picker are **two separate turns**. Turn 1 sends the full message text with NO tool call attached. Only after turn 1 is sent may turn 2 invoke the question/picker tool.
- FORBIDDEN: placing the message content inside the picker/question tool payload. FORBIDDEN: calling any tool in the same turn as the presentation message.
- If a turn already contains a tool call, that turn must NOT carry presentation content — the content belongs in the preceding chat-only turn.
- Anti-pattern (violation): calling the picker with the interpretation written into the question text while no chat message was sent before it — the user then sees options with nothing to judge them by (e.g. asking "Is the above correct?" with no "above").

## 3. Handling unsure / skip

- `unsure` / `skip` are always valid implicit options — never force the user to guess.
- On `unsure`/`skip`: the agent fills the best default, records it in `decisions.yaml` with `status: unconfirmed`, and marks it `[UNCONFIRMED]` wherever shown. The flow NEVER blocks on an unanswered question.
- Re-surface all `[UNCONFIRMED]` items at blueprint sign-off and at handover.

## 4. Language

- Chat, questions, options, summaries: `language.response` (default Vietnamese).
- Internal agent-to-agent prompts, docs, code: English (or `language.documentation`).
- When presenting an English-origin summary to the user, `agent_lead` translates it into `language.response`.
