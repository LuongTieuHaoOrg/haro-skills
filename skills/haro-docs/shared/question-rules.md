# Question & Response Rules (Anti-Drop Text Mechanism)

> **MANDATORY FOR ALL USER-FACING RESPONSES**
> To prevent the runtime from dropping sibling text blocks when a question/picker tool is invoked, every interaction must strictly follow a 2-tier content routing policy based on content length:

## 1. Core Standards & Language
- **Single Source of Truth:** Write once, assemble — never duplicate.
- **Language:** Chat uses `language.response`, doc content uses `language.documentation`.
- **Handling unsure / defer / skip:** Always allow users to skip, defer, or mark unsure without blocking.

## 2. Content Routing (Short vs Long)
- **SHORT Content (≤ ~200 characters, hub navigation, confirmations, save/skip):**
  - Embed the message directly inside the question/picker tool payload (`question` parameter).
  - No separate text block. Single response containing only the tool call.

- **LONG Content (Detailed explanations, outlines, reviews, assessments):**
  - Execute the 3-step robust presentation flow:
    1. **`<render text>`**: Send the full content in the standard text block first (kept for clients supporting text + tool rendering).
    2. **`<write file>`**: Write the complete detailed content into a workspace file under `.haro-docs/output/<step-name>.md` (or relevant workspace path).
    3. **`<render popup>`**: Trigger the question/picker tool call with a clear title pointing directly to the file (e.g., *"Đã ghi lại nội dung chi tiết vào file `...` tại <path>. Tiếp theo sẽ làm gì?"*) accompanied by concise action options.

## 3. Anti-narration — chat blocks carry user-facing content ONLY

- A text block MUST contain only the content the workflow step prescribes, written in `language.response`.
- FORBIDDEN in chat: internal planning, tool-sequencing notes, conflict-resolution notes, file-deferral notes, or any English meta-commentary about what the agent is doing.
- If a step cannot run as prescribed, STOP and fix the precondition per the workflow — never narrate the problem to the user as if it were content.
