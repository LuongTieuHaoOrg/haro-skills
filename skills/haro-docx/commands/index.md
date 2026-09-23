# Index (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the `/haro-docx`
> landing and fallback: it runs for `/haro-docx` with no arguments, for
> `help` / `--help` / `-h`, and for any unknown first token. Do not act from
> memory: the reference always wins over memory.
> **Ground rules:** reply to the user in Vietnamese with full diacritics.
> This workflow is strictly read-only: never create or write any file.

## Index — Introduce + List Commands + Suggest

`haro-docx` renders markdown/text/pdf sources into enterprise-standard `.docx`
(cover page, revision history, TOC, header/footer, page numbers). Full
concept: `SKILL.md` §1.

1. **Introduce (chat, 3–4 lines, Vietnamese with diacritics)** — what the
   skill does + the single rule that matters: every command's workflow lives
   in its own file; generated files go to `.haro-docx/output/`.
2. **List commands:** render the Command index table from `SKILL.md`. Do not
   duplicate it here.
3. **Light status (one check only):** when `.haro-docx/config.yaml` exists →
   `Đã cấu hình (.haro-docx/config.yaml)`; otherwise →
   `Chưa cấu hình — chạy /haro-docx config trước`.
4. **Action picker:** single picker call (picker tool when available, otherwise
   numbered list) with `export`, `export --template`, `config`, `stop` and a
   one-line Vietnamese "when to use" for each. When not configured, pre-suggest
   `config`. Once picked, follow MANDATORY ROUTING in `SKILL.md`.
5. **Fallback (unknown token):** prefix with
   `Lệnh 'foo' không hợp lệ. Các lệnh hợp lệ: export, export --template, config.`
   Suggest the closest match. Case-insensitive, trim whitespace.
