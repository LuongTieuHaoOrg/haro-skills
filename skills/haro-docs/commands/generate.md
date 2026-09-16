# Generate (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs generate`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).
> Content writing in this file must follow `shared/writing-rules.md`.

## 6. Command `/haro-docs generate` / `generate <target>` — Build Docs (Folder, File, or Guided Discovery)

Build documentation flexibly based on current state. Three modes:
- `/haro-docs generate` — propose **Folders** (e.g., `01-overview`, `02-business`, `04-architecture`) or specific files that need attention. Choosing a folder allows building/updating the whole section cluster at once.
- `/haro-docs generate <folder>` — focus on a specific folder (e.g., `02-business`) to elicit and update all files within that domain cluster.
- `/haro-docs generate <file>` — focus on a specific file (e.g., `02-business/01-value-prop.md`) to research and write in depth. (Never writes to a `RELEASED` file).

### Elicitation storage

Interim Q&A is stored in `.haro-docs/elicitation/<sanitized-path>.md` with frontmatter (`target`, `updated`, `gaps`). Locate it through `.haro-docs/elicitation/index.yaml`. Never hand-write the index.

### Status

The single source of status is `.haro-docs/config/status.yaml`. `UPDATING` = in progress, reference-only. `RELEASED` = final, must-follow; only `RELEASED` files feed `10-deliverables/`. `generate` never writes to a `RELEASED` file.

### Workflow
1. **Selective RAG & Assessment (Anti-Drop 3-Step Flow per `shared/question-rules.md`):**
   - `<render text>`: Present situation & recommended angle.
   - `<write file>`: Write detailed analysis to `.haro-docs/output/generate-assessment.md`.
   - `<render popup>`: Propose folder or file candidates (popup pointing to the assessment file, plus short options).
2. **Consolidate needs (D2 — before any writing):** merge near-duplicate role desires into ONE need (`N-xx.y`); split role differences out as authorization/business rules. Assign REQ-IDs per `shared/writing-rules.md` (§11–12): every need, use case, story, and AC carries `N-xx / UC-xx / US-xxx / AC-xxx.y`.
3. **Guided elicitation with skip/defer:** ~5 plain-word questions per target; each answer recorded as `answered | unsure | deferred | skipped` in the elicitation file. Every story must satisfy the story-quality bar (`Là/muốn/để` + Given/When/Then ACs + INVEST-lite) — failing stories stay gaps, never land in docs. **Mandatory pushback:** on conflict with knowledge/RELEASED/scan evidence, stop with `You said X → but evidence Y shows Z → keep X or change? (keep / change / skip)`.
4. **Propose outline with alternatives** (LONG content per `shared/question-rules.md`): `Recommended A` → `Alternative B + tradeoff` → open gaps; picker `Choose A / Choose B / Revise`.
5. **Write** the target file(s) with REQ-IDs inline, current-state first-version style. Folder mode: write/update all files in the cluster sequentially. Update `status.yaml` (`UPDATING`). Auto-append new terms/abbreviations/references to `00-common/`.
6. **Confirm & mark status (D1 — completeness gate):** `RELEASED` only when zero blocking gaps remain; otherwise keep `UPDATING` with open gaps in the elicitation file. Then update `00-common/05-traceability.md` with the ID chains (`N → UC → US → AC → TC`).
7. **Next-step popup:** 2–3 concrete candidates + `review <file>` + `stop`. Wait for the pick; do NOT auto-run.

### Examples

```
/haro-docs generate
/haro-docs generate 02-business
/haro-docs generate 02-business/01-value-proposition.md
/haro-docs generate 10-deliverables/01-BRD.md
```
