# Workspace (Haro Docx Writer reference)

## Registry: `.haro-docx-writer/` + global `~/.haro-docx-writer/`

Every template is a folder holding exactly two files:

```text
<project>/.haro-docx-writer/templates/<id>/
├── template.docx   # the style source (copied verbatim from the user's .docx)
└── template.yaml   # meta (id/name/description/created_at/updated_at)
                    # + params (company/solution/document/header/styles...)

~/.haro-docx-writer/templates/<id>/        # same layout, global scope
├── template.docx
└── template.yaml

.haro-docx-writer/output/                 # generated .docx files (git-ignored recommended)
```

## Skill layout: `skills/haro-docx-writer/`

```text
├── commands/            # normative workflows (read fully before acting)
│   ├── index.md         # /haro-docx-writer dashboard
│   ├── quick.md         # /haro-docx-writer <file> (quick export, pick template)
│   ├── list.md          # /haro-docx-writer --list
│   ├── import.md        # /haro-docx-writer --import:<id>
│   ├── update.md        # /haro-docx-writer --update:<id>
│   ├── sync-docx.md     # /haro-docx-writer --sync-docx:<id> (yaml -> docx)
│   ├── sync-yaml.md     # /haro-docx-writer --sync-yaml:<id> (docx -> yaml)
│   ├── delete.md        # /haro-docx-writer --delete:<id>
│   ├── view.md          # /haro-docx-writer --view:<id>
│   ├── validate.md      # /haro-docx-writer --validate:<id>
│   └── export.md        # /haro-docx-writer --export:<id>
├── shared/docx-style.md # the visual standard (normative)
├── scripts/build_docx.py       # the ONLY exporter — never hand-craft .docx
├── scripts/template_store.py   # registry helpers (list/resolve/delete)
├── scripts/extract_template.py # .docx -> template.yaml (used by --import)
├── scripts/validate_template.py# yaml-vs-docx check (used by --validate)
├── scripts/update_template.py  # patch yaml + push styles into .docx (used by --update/--sync-docx)
├── scripts/sync_yaml.py        # re-extract docx styles into yaml (used by --sync-yaml)
└── templates/
    ├── config.yaml           # param defaults merged at --import time
    ├── default-template.docx # basic default template (import it to start fast)
    └── sample-input.md       # sample spec input for trial exports
```
