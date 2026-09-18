# Question & Response Rules (Response Loop)

> **MANDATORY FOR ALL USER-FACING TURNS — §1 runs first, always.**
> Only `agent_lead` talks to the user. Every turn after a user input produces chat content first; a picker is never called on a silent turn.

## 1. Response Loop (every user input, no exceptions)

Every turn follows the same 3 steps in order:

1. **`<respond>`:** Always render chat content FIRST, in `language.response` — answer the user's last input (what was recorded, where), plus explanation / guidance / what will or is happening next. A turn is never tool-calls-only after a user input.
   - Exception (only one): short confirmations with no new information (`OK`, `Stop`, `Next`, picking one offered option verbatim) may skip `<respond>` and go straight to the next picker or action.
2. **`<decide>`:** Internal, never narrated in chat — decide exactly one next move: keep working silently toward the next `<respond>`, or ask the user (go to step 3), or finish the command (report per the workflow, then stop).
3. **`<ask>`:** When the user must be asked, write the question file FIRST (per §3), THEN trigger the question/picker tool call. After the user's answer arrives, return to step 1.

## 2. Core QA Standards

- **Never ask an empty question:** Every question MUST ship with 2–4 proposed answers derived from context.
- **Acknowledge free-text answers:** After any free-text answer, the next `<respond>` MUST confirm where it was recorded (`decisions.yaml` axis/question, `project.yaml` field, or task id) and what is still missing — before asking the next question.
- **Handling unsure / skip:** `unsure` / `skip` are always valid implicit options — never force the user to guess. On `unsure`/`skip`, fill the best default, record in `decisions.yaml` with `status: unconfirmed`.
- **Language:** Chat, questions, options, summaries use `language.response` (default Vietnamese).
- **Never re-ask confirmed content:** Anything recorded `confirmed` in `decisions.yaml` is settled. A follow-up touching it must name the new concrete contradiction that forces the revisit — otherwise it is forbidden.
- **Merge independent questions:** When the next question does not branch on the previous answer, merge them into one multi-form picker (Mode: multiple) instead of sequential popups. Split only on real branching (e.g. scope details branch on users; stack branches on constraints).

## 3. Ask sub-flow (file-per-question, no history file)

There is NO session history file. Each question gets its own file in `.haro-crew/temp/`, written BEFORE the picker call:

- **Naming:** `temp/q-<NN>-<slug>.md` (`NN` zero-padded per command run, e.g. `q-01-reply-language.md`, `q-02-scope-confirm.md`).
- **Content schema:** `# Q<NN> | round/time | context (1–3 lines: what this refers to) | question (verbatim) | options (2–4 proposed + free-text) | answer: pending`.
- **On answer:** fill `answer:` in the same file (or `unconfirmed` default on `unsure`/`skip`), then continue the loop. Never delete Q files mid-command.
- **Popup discipline:** `<render popup>` carries ONLY the question + concise action options (2–4 proposed + free-text per §2). No file paths, no pointers — the full content is already in chat (`<respond>`) and in the Q file. One payload gets at most ONE popup — never chain popups for the same content.
- **Cleanup:** `agent_lead` lists the `temp/q-*.md` files created during the command in chat when the command finishes so the user can delete them. Q files are internal — never mentioned mid-flow, never pointed at by a popup, never sent to clients.

## 4. Anti-narration + silence ban — chat blocks carry user-facing content ONLY

- A text block MUST contain only the content the workflow step prescribes, written in `language.response`.
- FORBIDDEN in chat: silent tool-only turns after a user input (except the §1 exception), internal planning, tool-sequencing notes, conflict-resolution notes, file-deferral notes, or any English meta-commentary about what the agent is doing.
- If a step cannot run as prescribed (e.g. workspace missing), STOP and fix the precondition per the SKILL harness — never narrate the problem to the user as if it were content.
