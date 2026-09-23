---
name: haro-docx
description: Render enterprise-standard .docx for technical specs (cover page, revision history, auto TOC, styled header/footer, page numbers). Use this skill whenever the user mentions xuat docx, xuất docx, file Word, trinh ky, trình ký, nop specs, nộp specs/BRD/PRD/SAD/FSD, in an, in ấn, company template, or needs a Word file from markdown/text/pdf — even if they don't say the word docx. Run /haro-docx with no args to pick an action. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Docx — Enterprise DOCX Export Skill

## 1. Overview

`haro-docx` turns user-provided sources (**markdown / text / pdf**) into a
company-standard `.docx` for technical specs. It is a standalone skill like
`haro-docs` / `haro-crew`, invoked via `/haro-docx ...`.

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

## 2. Workspace `.haro-docx/`

User configuration lives in `.haro-docx/` at the project root (created by
`config`, never guessed). Skill defaults live in `templates/` + `resources/`.

```
.haro-docx/
├── config.yaml          # company, solution, document defaults, logo path
└── output/              # generated .docx files (git-ignored recommended)

skills/haro-docx/
├── commands/            # normative workflows (read fully before acting)
├── shared/docx-style.md # the visual standard (normative)
├── scripts/build_docx.py# the ONLY generator — never hand-craft .docx
├── templates/config.yaml# default config shipped with the skill
├── templates/sample-input.md  # default sample spec input
└── resources/templates/ # user-supplied .docx style templates (picker source)
```

> **Read order (every command):** `.haro-docx/config.yaml` (if present, else
> `templates/config.yaml` defaults) → `shared/docx-style.md` → the command's
> workflow file. Config values are ground truth over guessed names.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives
> in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row.
> 2. Read that workflow file **fully, before any other tool call or answer**.
> 3. If you notice you are about to act, answer, or create anything without
>    the workflow open, **STOP and read it first**. The workflow always wins
>    over memory.

## Command index

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-docx` (no args) | Show dashboard, pick next action | `commands/index.md` | `/haro-docx` |
| `/haro-docx export <input> [-o out.docx] [--template name]` | Render md/txt/pdf to enterprise .docx | `commands/export.md` + `shared/docx-style.md` | `/haro-docx export docs/spec.md -o dist/spec.docx` |
| `/haro-docx export --template` | List `resources/templates/` + user templates, pick style template | `commands/export.md` | `/haro-docx export --template` |
| `/haro-docx config` | Show how to configure `.haro-docx/config.yaml` + `resources/` | `commands/config.md` | `/haro-docx config` |

## 3. Hard rules

- NEVER build `.docx` by hand or with another ad-hoc script. ALWAYS call
  `scripts/build_docx.py`. If the script cannot do something, extend the
  script — don't work around it.
- NEVER invent company/solution/document names. Read them from config; if
  missing, ask the user (see `commands/config.md`).
- Input formats: `.md` and `.txt` are native. `.pdf` is best-effort text
  extraction (needs `pypdf` installed); scanned/image PDFs are refused with a
  clear message. Existing `.docx` inputs are NOT merged — they belong in
  `resources/templates/` as style templates via `--template`.
- Language rules:
  - Skill instructions and code comments are in **English**.
  - Everything the user sees — chat replies, generated document content,
    config values, console messages — is in **Vietnamese with full diacritics**.
  - The skill formats source content, never translates it: code, endpoints,
    and parameters stay in their original English.
