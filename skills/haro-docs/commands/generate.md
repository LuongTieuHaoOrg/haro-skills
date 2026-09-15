# Generate (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs generate`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).
> Content writing in this file must follow `shared/writing-rules.md`.

## 6. Command `/haro-docs generate` / `generate <target>` — Build Docs (Folder, File, or Guided Discovery)

Build documentation flexibly based on current state. Three modes:
- `/haro-docs generate` — propose **Folders** (e.g., `01-overview`, `02-business`, `04-architecture`) or specific files that need attention. Choosing a folder allows building/updating the whole section cluster at once.
- `/haro-docs generate <folder>` — focus on a specific folder (e.g., `02-business`) to elicit and update all files within that domain cluster.
- `/haro-docs generate <file>` — focus on a specific file (e.g., `02-business/01-value-prop.md`) to research and write in depth. (Never writes to a `RELEASED` file).

### Workflow
1. **Selective RAG & Assessment (Anti-Drop 3-Step Flow per `shared/question-rules.md`):**
   - `<render text>`: Present situation & recommended angle.
   - `<write file>`: Write detailed analysis to `.haro-docs/output/generate-assessment.md`.
   - `<render popup>`: Propose folder or file candidates (`<render popup>` pointing to the assessment file, plus short options).
2. **Execution:**
   - If a **Folder** is chosen: elicit the core domain questions, outline all relevant missing/updating files in that folder, and write/update them sequentially.
   - If a **File** is chosen: follow guided elicitation, outline A/B, write, auto-update `00-common` glossary/abbreviations, and prompt for `RELEASED` status.
/haro-docs generate
/haro-docs generate 02-business/01-value-prop.md
/haro-docs generate 10-deliverables/01-BRD.md
```
