# Question & Response Rules (Anti-Drop Text Mechanism)

> **MANDATORY FOR ALL USER-FACING RESPONSES**
> To prevent the runtime from dropping sibling text blocks when a question/picker tool is invoked, every interaction must strictly follow a 2-tier content routing policy based on content length:

## 1. Core QA Standards
- **Never ask an empty question:** Every question MUST ship with 2–4 proposed answers derived from context.
- **Handling unsure / skip:** `unsure` / `skip` are always valid implicit options — never force the user to guess. On `unsure`/`skip`, fill the best default, record in `decisions.yaml` with `status: unconfirmed`.
- **Language:** Chat, questions, options, summaries use `language.response` (default Vietnamese).
- **Never re-ask confirmed content:** Anything recorded `confirmed` in `decisions.yaml` is settled. A follow-up touching it must name the new concrete contradiction that forces the revisit — otherwise it is forbidden.
- **Merge independent questions:** When the next question does not branch on the previous answer, merge them into one multi-form picker (Mode: multiple) instead of sequential popups. Split only on real branching (e.g. scope details branch on users; stack branches on constraints).

## 2. Unified 3-step flow (every question, no exceptions)

Every question to the user — short confirmation or long sign-off alike — runs the same 3 steps in order:

1. **`<render text>`:** Send the full content in the standard text block first, in `language.response` (context, recap, and everything the question refers to — the popup never retypes it).
2. **`<write history file>`:** Append the round to the single session file `.haro-crew/temp/history.md` (create it on the first question of the session): round/time, the question asked, and the user's previous answers if any (`pending` when unanswered). This file is a technical trick so the popup renders without error — never mention it to the user, never point a popup at it, never send it to clients. `agent_lead` lists it for user cleanup when the command finishes.
3. **`<render popup>`:** Trigger the question/picker tool call focused ONLY on the question + concise action options (with 2–4 proposed answers + free-text per §1). No file paths, no pointers — the content is already in chat.

One payload gets at most ONE popup — never chain popups for the same content.

## 3. Anti-narration — chat blocks carry user-facing content ONLY

- A text block MUST contain only the content the workflow step prescribes, written in `language.response`.
- FORBIDDEN in chat: internal planning, tool-sequencing notes, conflict-resolution notes, file-deferral notes, or any English meta-commentary about what the agent is doing.
- If a step cannot run as prescribed (e.g. workspace missing), STOP and fix the precondition per the workflow — never narrate the problem to the user as if it were content.
