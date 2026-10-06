# Index (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the `/haro-docx-writer`
> landing and fallback: it runs for `/haro-docx-writer` with no arguments and
> for `help` / `--help` / `-h`. A bare FILE argument routes to
> `commands/quick.md` (not this file); an unknown `--flag` falls back here.
> Do not act from memory: the reference always wins over memory.
> **Ground rules:**
> This workflow is strictly read-only: never create or write any file.

## Index — Introduce + List Commands + Suggest

`haro-docx-writer` renders markdown/text/pdf sources into enterprise-standard `.docx`
through named templates (cover page, revision history, TOC, header/footer,
page numbers). Templates live in `.haro-docx-writer/templates/<id>/` (local) and
`~/.haro-docx-writer/templates/<id>/` (global). Full concept: `SKILL.md` §1–2.

1. **Introduce (chat, 3–4 lines)** — what the
   skill does + the single rule that matters: every template has an id; every
   command's workflow lives in its own file; generated files go to
   `.haro-docx-writer/output/`.
2. **List commands:** render the Command index table from `SKILL.md`. Do not
   duplicate it here.
3. **Light status (one check only):** run
   `python skills/haro-docx-writer/scripts/template_store.py --project-root . list`
   and summarize in one line: `Có N mẫu local, M mẫu global` (or
   `Chưa có mẫu nào — hãy --import mẫu đầu tiên`). No other file checks.
4. **Action picker:** single picker call (picker tool when available, otherwise
   numbered list) with `--list`, `--import:<id>`, `--update:<id>`,
   `--sync-docx:<id>`, `--sync-yaml:<id>`,
   `--delete:<id>`, `--view:<id>`, `--validate:<id>`, `--export:<id>`,
   `quick <file>` (quick-export, runs `commands/quick.md`), `stop` and a
   one-line "when to use" for each. When no templates
   exist, pre-suggest `--import:<id>`. Once picked, follow MANDATORY ROUTING
   in `SKILL.md`.
5. **Fallback (unknown `--flag` only):** prefix with
   `Lệnh 'foo' không hợp lệ. Các lệnh hợp lệ: --list, --import:<id>, --update:<id>, --sync-docx:<id>, --sync-yaml:<id>, --delete:<id>, --view:<id>, --validate:<id>, --export:<id>.`
   Suggest the closest match. Case-insensitive, trim whitespace. A bare file
   path is NOT invalid — it routes to `commands/quick.md`.
