---
name: haro-docx-writer
description: Export content to Word (.docx) from markdown, text, or PDF sources using named reusable templates with a local and global registry. Templates carry document identity, styles, page layout, header/footer, and fillable placeholders; commands cover the full lifecycle: import/list/view/validate/update/delete templates, two-way yaml-docx sync, and render output by template id or quick-pick.
---

# Haro Docx Writer

Export markdown/text/pdf to `.docx` through a named template (`<id>`),
invoked via `/haro-docx-writer ...`. Each template pairs a YAML config
(identity, styles, page, placeholders) with its `.docx` source; local
registry wins over global. Placeholders fill at render; yaml-docx sync
runs both directions manually.

Details live in `docs/` — read on demand: `docs/overview.md` (concepts),
`docs/workspace.md` (registry + file layout), `docs/commands-reference.md`
(full command table), `docs/rules.md` (normative rules).

> ## MANDATORY ROUTING
>
> 1. Match the command to exactly one row below (bare file = quick row;
>    flags glue the id with `:`, e.g. `--import:<id>`).
> 2. Read that workflow file fully before any other tool call or answer.
> 3. Acting without the workflow open → STOP and read it first.

| Command | Read first |
|---------|------------|
| `/haro-docx-writer` (no args) | `commands/index.md` |
| `/haro-docx-writer <file>` | `commands/quick.md` |
| `/haro-docx-writer --list` | `commands/list.md` |
| `/haro-docx-writer --import:<id> <file.docx>` | `commands/import.md` |
| `/haro-docx-writer --update[:<id>]` | `commands/update.md` |
| `/haro-docx-writer --sync-docx:<id>` | `commands/sync-docx.md` |
| `/haro-docx-writer --sync-yaml:<id>` | `commands/sync-yaml.md` |
| `/haro-docx-writer --delete:<id>` | `commands/delete.md` |
| `/haro-docx-writer --view:<id>` | `commands/view.md` |
| `/haro-docx-writer --validate:<id>` | `commands/validate.md` |
| `/haro-docx-writer --export:<id> <input>` | `commands/export.md` |
