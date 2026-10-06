---
name: haro-docx-writer
description: Render enterprise-standard .docx from markdown/text/pdf using named templates (cover page, revision history, auto TOC, styled header/footer, page numbers). Use this skill whenever the user mentions xuat docx, xuất docx, file Word, trinh ky, trình ký, nop specs, nộp specs/BRD/PRD/SAD/FSD, in an, in ấn, company template, mau docx, mẫu docx, or needs a Word file — even if they don't say the word docx. Run /haro-docx-writer with no args to pick an action. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Docx Writer — Enterprise DOCX Export Skill (template registry)

## 1. Overview

`haro-docx-writer` turns user-provided sources (**markdown / text / pdf**) into a
company-standard `.docx` for technical specs, rendered through a **named
template** (`<id>`). It is a standalone skill like `haro-docs` / `haro-crew`,
invoked via `/haro-docx-writer ...`.

Enterprise layout (the "why": a sign-off document must identify itself on
every page and carry its own audit trail):

- **Cover page:** document title, company, solution, version, date, author.
- **Control pages:** revision history table plus responsibility table
  (author / reviewer / approver).
- **TOC page:** Word auto-TOC field — the user presses "Update Field" on
  first open.
- **Header (every content page):** left = logo image; right = 2 lines
  (line 1 = document name in bold, line 2 = company name).
- **Footer (every content page):** left = page number field (`Trang X / Y`);
  right = solution name.
- **Body:** Heading 1–3, justified text, bulleted lists, tables, code blocks
  in a monospace shaded style. Single ink only: Times New Roman, black
  (`000000`) — see `shared/docx-style.md`.

## 2. Workspace `.haro-docx-writer/` + global `~/.haro-docx-writer/`

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

skills/haro-docx-writer/
├── commands/            # normative workflows (read fully before acting)
│   ├── index.md         # /haro-docx-writer dashboard
│   ├── list.md          # /haro-docx-writer --list
│   ├── import.md        # /haro-docx-writer --import:<id>
│   ├── update.md        # /haro-docx-writer --update:<id>
│   ├── delete.md        # /haro-docx-writer --delete:<id>
│   ├── view.md          # /haro-docx-writer --view:<id>
│   ├── validate.md      # /haro-docx-writer --validate:<id>
│   └── export.md        # /haro-docx-writer --export:<id>
├── shared/docx-style.md # the visual standard (normative)
├── scripts/build_docx.py       # the ONLY exporter — never hand-craft .docx
├── scripts/template_store.py   # registry helpers (list/resolve/delete)
├── scripts/extract_template.py # .docx -> template.yaml (used by --import)
├── scripts/validate_template.py# yaml-vs-docx check (used by --validate)
├── scripts/update_template.py  # patch yaml + push styles into .docx (used by --update)
└── templates/config.yaml       # param defaults merged at --import time
```

> **Read order (every command):** the template's `template.yaml` (resolved
> local-first) → `shared/docx-style.md` → the command's workflow file.
> Template values are ground truth over guessed names.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives
> in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row (colon syntax:
>    `--import:<id>` — the id is glued to the flag with `:`).
> 2. Read that workflow file **fully, before any other tool call or answer**.
> 3. If you notice you are about to act, answer, or create anything without
>    the workflow open, **STOP and read it first**. The workflow always wins
>    over memory.

## Command index

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-docx-writer` (no args) | Show dashboard, pick next action | `commands/index.md` | `/haro-docx-writer` |
| `/haro-docx-writer --list` | List all templates (id, name, description, location, created, updated) | `commands/list.md` | `/haro-docx-writer --list` |
| `/haro-docx-writer --import:<id> <file.docx>` | Register a .docx file as a new template (asks local/global, checks duplicates, extracts yaml) | `commands/import.md` | `/haro-docx-writer --import:congty-a DieuLe.docx` |
| `/haro-docx-writer --update:<id> <nội dung>` | Update a template's params/content per user request | `commands/update.md` | `/haro-docx-writer --update:congty-a đổi company thành CTY X` |
| `/haro-docx-writer --delete:<id>` | Delete a template (asks confirm) | `commands/delete.md` | `/haro-docx-writer --delete:congty-a` |
| `/haro-docx-writer --view:<id>` | Show a template's yaml + .docx paths and full config | `commands/view.md` | `/haro-docx-writer --view:congty-a` |
| `/haro-docx-writer --validate:<id>` | Check yaml-vs-docx match (style-level) | `commands/validate.md` | `/haro-docx-writer --validate:congty-a` |
| `/haro-docx-writer --export:<id> <input>` | Render md/txt/pdf to enterprise .docx with template `<id>` | `commands/export.md` + `shared/docx-style.md` | `/haro-docx-writer --export:congty-a docs/sad.md` |

## 3. Hard rules

- NEVER build `.docx` by hand or with another ad-hoc script. Export ALWAYS
  calls `scripts/build_docx.py`; visual patches ALWAYS call
  `scripts/update_template.py`. If a script cannot do something, extend the
  script — don't work around it.
- NEVER invent company/solution/document names or template ids. Ids match
  `[a-z0-9][a-z0-9-_]{0,40}` (lowercase, 2–41 chars). Resolution order is
  **local first, global second** — never guess which scope; `--list` shows it.
- Colon syntax is normative: `--import:<id>`, `--update:<id>`,
  `--delete:<id>`, `--view:<id>`, `--validate:<id>`, `--export:<id>`.
  The id is glued to the flag with `:` (no space).
- `--update` with vague content (`làm đẹp hơn`, `sửa giúp anh`, empty):
  ask back with concrete options — never interpret freely.
- `--validate` is style-level only (styles + header/footer presence +
  logo-file existence). Run-level oddities are ignored to avoid false
  positives — see `shared/docx-style.md` §9.
- Input formats: `.md` and `.txt` are native. `.pdf` is best-effort text
  extraction (needs `pypdf` installed); scanned/image PDFs are refused with a
  clear message. A `.docx` is NEVER an export input — it is a template
  source for `--import`.
- Language rules:
  - Skill instructions and code comments are in **English**.
  - Everything the user sees — chat replies, generated document content,
    template values, console messages — is in **Vietnamese with full diacritics**.
  - The skill formats source content, never translates it: code, endpoints,
    and parameters stay in their original English.
