# QA rules (mandatory for every user-facing question in haro-crew)

> Only `agent_lead` talks to the user. Every question below applies to `agent_lead` output.
> Specialist agents never address the user directly.

## 1. Never ask an empty question

Every question MUST ship with 2–4 proposed answers derived from context (project idea, prior decisions, domain knowledge). The user picks one or types their own answer. A question without proposals is a workflow violation.

## 2. Picker format

1. Render the full context and the proposals **in chat text first** (in `language.response`).
2. Then invoke the question/picker tool: short option labels (≤1 line each, detail lives in chat) + free-text answer enabled (`type your answer`).
3. Declare Mode: `single` by default, `multiple` only when the workflow says so.

## 3. Handling unsure / skip

- `unsure` (not sure) / `skip` (bỏ qua) are always valid implicit options — never force the user to guess.
- On `unsure`/`skip`: the agent fills the best default, records it in `decisions.yaml` with `status: unconfirmed`, and marks it `[UNCONFIRMED]` wherever shown. The flow NEVER blocks on an unanswered question.
- Re-surface all `[UNCONFIRMED]` items at blueprint sign-off and at handover.

## 4. Language

- Chat, questions, options, summaries: `language.response` (default Vietnamese).
- Internal agent-to-agent prompts, docs, code: English (or `language.documentation`).
- When presenting an English-origin summary to the user, `agent_lead` translates it into `language.response`.
