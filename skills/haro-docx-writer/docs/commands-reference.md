# Command reference (Haro Docx Writer reference)

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-docx-writer` (no args) | Show dashboard, pick next action | `../commands/index.md` | `/haro-docx-writer` |
| `/haro-docx-writer <file>` | Quick export: pick an existing template, render immediately | `../commands/quick.md` | `/haro-docx-writer docs/sad.md` |
| `/haro-docx-writer --list` | List all templates (id, name, description, location, created, updated) | `../commands/list.md` | `/haro-docx-writer --list` |
| `/haro-docx-writer --import:<id> <file.docx>` | Register a .docx file as a new template (asks local/global, checks duplicates, extracts yaml) | `../commands/import.md` | `/haro-docx-writer --import:congty-a DieuLe.docx` |
| `/haro-docx-writer --update[:<id>]` | Guide a template update: pick template (if no id), pick yaml or docx, edit/route to manual sync | `../commands/update.md` | `/haro-docx-writer --update:congty-a` |
| `/haro-docx-writer --sync-docx:<id>` | Push yaml config into template.docx (after hand-editing yaml) | `../commands/sync-docx.md` | `/haro-docx-writer --sync-docx:congty-a` |
| `/haro-docx-writer --sync-yaml:<id>` | Pull template.docx styles into yaml, docx wins, no backup (after hand-editing docx) | `../commands/sync-yaml.md` | `/haro-docx-writer --sync-yaml:congty-a` |
| `/haro-docx-writer --delete:<id>` | Delete a template (asks confirm) | `../commands/delete.md` | `/haro-docx-writer --delete:congty-a` |
| `/haro-docx-writer --view:<id>` | Show a template's yaml + .docx paths and full config | `../commands/view.md` | `/haro-docx-writer --view:congty-a` |
| `/haro-docx-writer --validate:<id>` | Check yaml-vs-docx match (style-level) | `../commands/validate.md` | `/haro-docx-writer --validate:congty-a` |
| `/haro-docx-writer --export:<id> <input>` | Render md/txt/pdf to enterprise .docx with template `<id>` | `../commands/export.md` + `../shared/docx-style.md` | `/haro-docx-writer --export:congty-a docs/sad.md` |
