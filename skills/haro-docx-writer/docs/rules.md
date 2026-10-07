# Rules (Haro Docx Writer reference)

> **Read order (every command):** the template's `template.yaml` (resolved
> local-first) → `../shared/docx-style.md` → the command's workflow file.
> Template values are ground truth over guessed names.

- NEVER build `.docx` by hand or with another ad-hoc script. Export ALWAYS
  calls `../scripts/build_docx.py`; visual patches ALWAYS call
  `../scripts/update_template.py`. If a script cannot do something, extend the
  script — don't work around it.
- NEVER invent company/solution/document names or template ids. Ids match
  `[a-z0-9][a-z0-9-_]{0,40}` (lowercase, 2–41 chars). Resolution order is
  **local first, global second** — never guess which scope; `--list` shows it.
- Colon syntax is normative: `--import:<id>`, `--update:<id>`,
  `--sync-docx:<id>`, `--sync-yaml:<id>`,
  `--delete:<id>`, `--view:<id>`, `--validate:<id>`, `--export:<id>`.
  The id is glued to the flag with `:` (no space).
- `--update` YAML branch with vague content (`làm đẹp hơn`, `sửa giúp anh`,
  empty): ask back with concrete options — never interpret freely.
  `--update` never syncs by itself; sync is always a manual user call.
- `--validate` is style-level only (styles + header/footer presence +
  logo-file existence). Run-level oddities are ignored to avoid false
  positives — see `../shared/docx-style.md` §9.
- Input formats: `.md` and `.txt` are native. `.pdf` is best-effort text
  extraction (needs `pypdf` installed); scanned/image PDFs are refused with a
  clear message. A `.docx` is NEVER an export input — it is a template
  source for `--import`.
- The skill formats source content, never translates it: code, endpoints,
  and parameters stay in their original language.
