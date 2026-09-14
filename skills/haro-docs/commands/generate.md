# Generate (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs generate`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).
> Content writing in this file must follow `shared/authoring.md`.

## 6. Command `/haro-docs generate` / `generate <file>` — Build Docs in Order (Role-Adaptive)

Build documentation flexibly based on current state + your role. Two modes:

- `/haro-docs generate` — propose 2–3 next files to build, based on reality, not rigid order. Skips all `00-common` files — `01-conventions.md` is decided during `init` (§5.2 step 3b) and `02-references, 03-abbreviations, 04-glossary, 05-traceability` are written only by `generate` itself; start writing at `01-overview`.
- `/haro-docs generate <file>` — focus on a specific file (e.g. `02-business/01-value-prop.md` or `10-deliverables/01-BRD.md`) to create it. When the named file is already `RELEASED`, report `File is RELEASED (final)` with a one-line summary and suggest the next open file instead — `generate` never writes to a `RELEASED` file.

### Ordered index

Canonical order is `00-common → 01-overview → 02-business → 03-features → 04-architecture → 05-security → 06-implementation → 07-quality → 08-operations → 09-guides → 10-deliverables → 99-assets` as defined in `schema.yaml` and shared/structure.md (§8). Within each folder, files are ordered by numeric prefix. This order is the **reference**, not a rigid gate: use it to understand what is prerequisite for what, but do not block flexibly. If all files are `RELEASED`, reply `All done — every file is RELEASED.`.

### Elicitation storage

Interim Q&A is stored in `.haro-docs/elicitation/<sanitized-path>.md` (e.g. `02-business-01-value-prop.md`) with frontmatter (`target`, `role`, `updated`) to avoid context overload. It is read on demand during `generate` and never loaded by default — locate it through `.haro-docs/elicitation/index.yaml` (one entry per file: `target | file | role | updated`). Creating the elicitation file writes its entry; removing the file removes its entry. Never hand-write the index. After the target file is completed, ask the user whether to keep or remove the elicitation file.

### Status

The single source of status is `.haro-docs/config/status.yaml`. Doc files carry no status themselves; paths missing from the map count as `UPDATING`.

- `UPDATING` — in progress, reference-only: consult for context, never treat as truth, never feed into deliverables.
- `RELEASED` — final, must-follow: later files comply strictly; only `RELEASED` files feed `10-deliverables/`; `generate` never writes to a `RELEASED` file.
- `00-common/02-references.md`, `03-abbreviations.md`, `04-glossary.md`, `05-traceability.md` are living references with status `UPDATING`, so `generate` appends to them at any time.

### Workflow

1. **Selective RAG** — read `knowledge/index.yaml` (if exists), pick entries whose domain/tags match the target file (`business` for BRD/Proposal, `technical`+`architecture` for SAD/FSD, `team` for people) with `state: active`, load only those knowledge files. Read `.haro-docs/config/status.yaml`: `RELEASED` files in scope are hard constraints (conflict → stop and ask), `UPDATING` files are background only.
2. **Ask who you are & propose next file based on reality:**
   - Ask first: `Who are you in this project? What is your role? (customer / sales / BA / dev / PM) — what do you know best about?` Save the answer to `knowledge/team-role.md` when not yet recorded (later turns only confirm `Still <role>?`), and also into `elicitation/<target>.md`.
    - Scan the current docs reality from `status.yaml`: which files are still `UPDATING`, which are `RELEASED`, which `change-requests/CR-*.md` exist. Use the canonical order as reference to understand prerequisites (e.g. `01-overview` and `02-business` are prerequisites for `04-architecture`), but **do not enforce rigidly** — understand flexibly what is actually needed. Skip the whole `00-common` folder (`01-conventions.md` is decided at init, `02-05` are written by `generate` itself); start writing at `01-overview`, not `00-common`.
   - If `<file>` was given and is `RELEASED`: report final and suggest the next open file (see two modes above).
   - If `<file>` was given and is `UPDATING`: treat it as the user's preference, but when it depends on an unfinished prerequisite (e.g. targeting `04-architecture` while `01-overview/03-goals.md` is still `UPDATING` with no content), explain why the prerequisite matters and ask `Do you want to continue with this file or switch to the prerequisite?`.
   - If no `<file>`: propose **2–3 candidates** for the next file, each with a one-line reason (e.g. `1. 01-overview/01-problem-statement.md — foundational purpose is still empty; 2. 02-business/01-value-prop.md — business value needed before architecture`). Let the user pick. If the user picks none, they can specify another file.
   - Once a target is chosen/confirmed, read nearby files in the same folder + glossary for context.
3. **Role-adaptive elicitation (flexible, not rigid):**
   - Produce **~5 tailored questions** based on `role + file domain + current reality` (e.g. for `02-business/*` with customer → market/pain/SLA/metrics; for `04-architecture/*` with customer → flows/business rules only, with dev → endpoints/schemas/NFR/diagrams). **Never ask a customer about code**, but otherwise adapt to what is actually missing.
   - Append Q&A to the elicitation file.
   - Analyze: check which required sections of the target file (per schema) are still missing. If incomplete, ask another 3–5 follow-up questions, append to the elicitation file, repeat until sufficient.
4. **Propose outline** — list sections for the target file, annotating source (which block/folder and which knowledge files). Wait for outline approval.
5. **Write** — create the target file in its canonical folder (kebab-case + numeric prefix, shared/authoring.md (§9)) in current-state first-version style (shared/authoring.md (§9)). Follow `00-common/01-conventions.md` Part B (diagram tool, API format, tone & depth, locked terms); when conventions lack guidance for this file, use the sensible default and note it in one line without writing to conventions. Write the new status into `.haro-docs/config/status.yaml` (`UPDATING`). When new facts surfaced, also record them in `knowledge/` when needed. Record `related_paths` when any.
6. **Auto 00-common** — immediately after writing, scan the new content for glossary terms, abbreviations, and references not yet in `00-common/`. Append them to the corresponding living file without requiring another command:
   - New term → append to `00-common/04-glossary.md` with one-line definition inferred from context; if `vi-en` mode, add English gloss.
   - New abbreviation → append to `00-common/03-abbreviations.md`.
   - New external reference (link, doc, standard) → append to `00-common/02-references.md`.
   No confirmation needed; just note `Auto 00-common: +2 terms, +1 abbreviation.` in the reply. Deduplicate before appending.
7. **Elicitation cleanup** — ask `Keep elicitation file for reference or remove? (keep / remove)`. On `remove`, remove the file and its `elicitation/index.yaml` entry. Act accordingly.
8. **Confirm & mark status** — ask `Mark this file as? (UPDATING / RELEASED)`. On `RELEASED`, write the new status into `.haro-docs/config/status.yaml`. `RELEASED` files become ground for later `generate` runs.
9. **Next-step popup** — after marking status, always ask what to do next (picker tool when available, otherwise numbered list). Propose 2–3 concrete candidates based on the fresh reality scan (prerequisites + gaps), each with a one-line reason, plus `review <just-finished file>` and `stop`. Example: `1. generate 02-business/01-value-prop.md — business value needed before architecture; 2. review 01-overview/01-problem-statement.md — just RELEASED, worth a critic pass; 3. stop`. Wait for the pick; do NOT auto-run.

### Examples

```
/haro-docs generate
/haro-docs generate 02-business/01-value-prop.md
/haro-docs generate 10-deliverables/01-BRD.md
```
