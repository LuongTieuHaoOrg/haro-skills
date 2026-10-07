# Update (Haro Docx reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** Normative workflow for
> `/haro-docx-writer --update` (no id) and `/haro-docx-writer --update:<id>`.
> Do not act from memory: read every step first.
> **Ground rules:** this command SUPPORTS the two sync commands — it never
> syncs by itself. NEVER hand-edit `template.docx` binary with tricks —
> yaml edits go through `scripts/update_template.py`. NEVER interpret a
> vague request freely.

## Command `/haro-docx-writer --update[:<id>]`

Guides the user to update a template, then stops so the user calls the
matching sync manually: `--sync-docx:<id>` after yaml edits,
`--sync-yaml:<id>` after docx edits.

### 0. Parse args (no guessing)

- `/haro-docx-writer --update` (no id) → go to Question 1.
- `/haro-docx-writer --update:<id>` (id glued with `:`) → resolve the id
  (unknown id → STOP with `LỖI: không tìm thấy mẫu '<id>'.` + hint
  `/haro-docx-writer --list`; show the winning scope, local first), then
  SKIP Question 1 and go straight to Question 2.
- A trailing `<nội dung>` after the command (if any) is NOT applied directly —
  keep it as a prefill suggestion for the YAML branch.

### 1. Question 1 — pick a template (only when no id)

Run from the project root:

```bash
python skills/haro-docx-writer/scripts/template_store.py --project-root . list
```

Render a single picker call (picker tool when available, otherwise numbered
list) with one entry per template: `<id> — <tên mẫu> (<local|global>)`.
Empty registry → STOP with `Chưa có mẫu nào.` + hint
`/haro-docx-writer --import:<id> <file.docx>`. Once picked → Question 2.

### 2. Question 2 — yaml or docx (mandatory picker)

Ask which file to update (single picker, exactly one choice):

- `yaml` — `.../<id>/template.yaml` (config thuộc tính)
- `docx` — `.../<id>/template.docx` (file mẫu render)

ALWAYS show both resolved file paths so the user can find them, whichever
branch is picked.

**YAML branch:**

1. Ask what to change (free-text, multiple items allowed). If the command
   carried `<nội dung>`, present it as the prefilled suggestion — still
   confirm before applying.
2. If the request is empty or vague (`làm đẹp hơn`, `sửa giúp anh`,
   single word with no target, ...), ask back with the concrete picker
   (multiple choice allowed): company/solution/document info, font/sizes,
   logo header, name/description, page geometry, other
   (`trường nào → giá trị nào`). Proceed only with explicit field → value pairs.
3. Apply the edit FOR the user (fast path): via
   `scripts/update_template.py --set` (repeatable, dot-paths) — see the key
   list below. NEVER ask the user to hand-edit when the agent can do it.
4. Show the before → after diff per key from script output.
5. STOP here. Point to the manual next step:
   run `/haro-docx-writer --sync-docx:<id>` to push into the docx.
   NEVER auto-sync.

**DOCX branch:**

1. Show the `template.docx` path and tell the user to open it in Word and
   edit (fonts, sizes, spacing, margins, header/footer...), then report back
   when done.
2. STOP here. Point to the manual next step:
   run `/haro-docx-writer --sync-yaml:<id>` (warn: docx wins, yaml
   styles/page overwritten with NO backup — suggest `--validate:<id>` first
   if unsure). NEVER auto-sync.

### Mappable `--set` keys (YAML branch)

- Text/meta: `name`, `description`, `company_name`, `solution_name`,
  `document_name`, `document_title`, `version`, `date`, `status`,
  `figure_caption` (`{n}`/`{alt}` pattern).
- Styles: `styles.body_font`, `styles.body_size`, `styles.h1_size` …
  `styles.h6_size`, `styles.body_line_spacing`, `styles.body_space_before`,
  `styles.body_space_after`, `styles.heading_space_before`,
  `styles.heading_space_after`, `styles.bullet_indent_cm`,
  `styles.bullet_space_after`, `styles.code_font`, `styles.code_size`.
- Page: `page.size` (`A4`/`Letter`), `page.orientation`
  (`portrait`/`landscape`), `page.margin_top/bottom/left/right_cm`,
  `page.header/footer_distance_cm`.
- Placeholders: `placeholders.<tên>.value` / `.description` (free text).
- Lists (`authors`, `reviewers`, `approvers`): comma-separated.
- Units: numeric values accept bare numbers (legacy meaning) or strings with
  units — `"15pt"`, `"2cm"`, `"25mm"`, `"1in"` (auto-converted). Examples:
  `--set styles.h1_size="15pt"`, `--set page.margin_left_cm="25mm"`.
  Bad units are refused with a clear error.
- Anything outside this list → explain it is fixed by the template itself
  (styles, header/footer, page structure come from the `.docx`); offer the
  closest supported alternative instead of improvising.

```bash
python skills/haro-docx-writer/scripts/update_template.py \
  --id <id> --project-root . \
  --set company_name="CTY X" --set styles.h1_size=15
```

### Examples

```text
/haro-docx-writer --update
/haro-docx-writer --update:congty-a
/haro-docx-writer --update:congty-a đổi company_name thành CÔNG TY X
```
