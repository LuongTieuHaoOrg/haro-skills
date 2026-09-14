# Conventions

> Decided during `/haro-docs init` (§5.2 step 3b). Part A is fixed by the skill —
> do not write it by hand. Part B is project-specific — set via `/haro-docs config conventions`.
> This file is the single source of truth for conventions (MD-only, no mirror).

## A. Fixed by skill (do not write by hand)

- **File naming:** kebab-case with numeric prefix indicating reading order (e.g. `01-problem-statement.md`).
- **Single Source of Truth:** each piece of content is written once in one file only; aggregated documents under `10-deliverables/` only assemble content, never duplicate it.
- **Status lifecycle:** every doc file is `UPDATING` (in progress, reference-only) or `RELEASED` (final, must-follow), tracked in `.haro-docs/config/status.yaml`. Doc files carry no status themselves. `RELEASED` files are final ground for later files; only `RELEASED` files feed `10-deliverables/`.
- **Language:** conversation replies use `language.response`, doc content uses `language.documentation` from `.haro-docs/config/project.yaml` (`en` | `vi` | `vi-en`).
- **Images/diagrams:** stored in `99-assets/`, referenced via relative paths; no inline base64.
- **Auto files:** `02-references.md`, `03-abbreviations.md`, `04-glossary.md`, `05-traceability.md` are written only by `generate` — do not write them by hand. `02-05` are living references with status `UPDATING`.

## B. Project-specific (decided at init, set via `/haro-docs config conventions`)

| # | Item | Value |
|---|------|-------|
| 1 | Diagram tool | {{diagram_tool}} <!-- mermaid \| plantuml \| drawio + image fallback --> |
| 2 | API spec format | {{api_format}} <!-- openapi-yaml \| md-table \| both --> |
| 3 | Tone & depth | {{tone}} <!-- high-level \| balanced \| deep-dive, synced with audience.technical_depth --> |
| 4 | RELEASED approver | {{approver}} <!-- single name/role, or per-domain approvers --> |
| 5 | Locked terms | {{terms}} <!-- product/brand terms with fixed spelling, or (none) --> |
| 6 | Priority deliverables | {{deliverables}} <!-- e.g. BRD, SAD — determines which conventions get detailed first, or (all) --> |
