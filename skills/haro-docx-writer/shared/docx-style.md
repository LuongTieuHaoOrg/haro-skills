# DOCX Rendering — Template-First (Haro Docx Writer, normative)

> `scripts/build_docx.py` implements this file. The agent must NOT restyle
> by hand — change this file plus the script instead.

## 1. Doctrine: the template governs

The template's `.docx` defines pages, styles, and header/footer. The export
only: strips the template's sample body, renders fresh body content into it,
fills `{{name}}` / `[[name]]` placeholders, and applies the yaml `page`
block (size/orientation/margins/distances) to existing sections.

The export explicitly does NOT:

- build cover / revision-history / responsibility / TOC pages;
- generate header/footer (the template's own are kept and used as-is);
- force fonts, sizes, colors, alignment, or fills onto any style or run;
- translate content (code, endpoints, parameters stay in their original language).

Style definitions in `template.yaml` (`styles.*`) describe the template for
viewing, `--validate`, and `--sync-docx` — they are never forced at render.
The single exception: a missing `Code Block` style is created (from yaml
`code_*` as fallback definition) so fenced code has a style to use.

## 2. Body mapping (md/txt → docx)

Structural mapping only — all formatting comes from the template's styles:

| Source | Output |
|--------|--------|
| `#` … `######` | Heading 1–6, template's own formatting |
| plain paragraph | Normal, template's own formatting |
| `- ` / `* ` / `1.` | List Bullet / List Number, template's own formatting |
| `\| a \| b \|` | Table Grid if the template defines it (plain, no fills, no forced bold) |
| fenced ` ``` ` | Code Block (template's, or fallback created at export) |
| `![alt](path)` | Centered figure + caption below (`Caption` style if defined, else Normal). Caption text from yaml `figure_caption` (default `"Figure {n}: {alt}"`). Image files must live under `assets/`, never base64 embeds; an unresolvable path becomes a plain `[alt]` line instead |
| `---` | Blank paragraph (whitespace), NEVER a page break or a rule line |
| `> quote` | Quote block: template's `Quote`/`Block Text`/`Intense Quote` style if defined, else Normal + left indent |

Inline markup (paragraphs, bullets, headings, table cells, captions) parses
to runs: `**bold**`, `*italic*`, `` `code` `` (yaml `code_font`), `~~strike~~`,
`[text](url)` (clickable hyperlink: template `Hyperlink` char style if defined,
else blue + underline), `\` escapes, nesting supported, unclosed markers stay
literal. Fenced code blocks are never inline-parsed. Placeholder values are
inserted as plain text (never re-parsed).

PDF input is plain extracted text: a blank line starts a new paragraph, and
ALL-CAPS or numbered (`1.`, `1.1`) lines are heuristically promoted to headings.

## 3. Units in YAML

Bare numbers keep legacy meaning (font/spacing sizes = pt,
margins/indents = cm, `body_line_spacing` is a unitless factor). Strings
with a unit convert automatically: `"12pt"`, `"2.54cm"`, `"25mm"`, `"1in"`
(`1in = 2.54cm = 25.4mm = 72pt`). Unknown units or bad formats are refused
with a clear error — never guessed.

## 4. Template registry mapping (extract / validate / update)

| YAML key | DOCX source (style-level only) |
|----------|-------------------------------|
| `styles.body_font` / `styles.body_size` | `Normal` style font name / size |
| `styles.body_line_spacing` / `body_space_before` / `body_space_after` | `Normal` paragraph format |
| `styles.h1_size` … `styles.h6_size` | `Heading 1` … `Heading 6` style font sizes |
| `styles.heading_space_before` / `heading_space_after` | `Heading 1` paragraph format (recorded; applied via `--sync-docx`) |
| `styles.bullet_indent_cm` / `bullet_space_after` | `List Bullet` (fallback `List Number`) indent / spacing |
| `styles.code_font` / `styles.code_size` | `Code Block` style font name / size — compared only when the style exists in the docx (`_extracted.has_code_style`) |
| `page.size` / `orientation` | First section page dimensions (A4/Letter within 0.15cm, else recorded in `_extracted`) |
| `page.margin_*_cm`, `page.header/footer_distance_cm` | First section margins / distances (cm, rounded 2dp) |
| `figure_caption` | Not extracted — YAML-configured caption pattern (`{n}`, `{alt}`) |
| `_extracted.has_header` / `header_text` | Any section header: any text or image |
| `_extracted.header_has_image` | Any drawing/picture element in a header |
| `_extracted.has_footer` / `footer_text` | Any section footer text |
| `_extracted.logo_saved` | `assets/logo.<ext>` extracted from the first header image (empty when none) — informational; no yaml key consumes it |
| `content.txt` | Not a param — raw dump (paragraphs with sizes, tables, header/footer text, image list) for the agent's purpose reading in `commands/import.md` §5 |

Style-level means: style definitions are compared, individual text runs are
ignored (a single odd run never counts as LỆCH). A docx attribute that was
never set explicitly (inherited theme default) never conflicts with the
yaml — `--validate` reports `(dùng YAML)`. Only two explicit, differing
values count as LỆCH. Document identity fields (`company_name`,
`solution_name`, `document_name`, ...) live in the yaml params and feed
placeholder substitution at export. The agent proposes their values by
reading `content.txt` and understanding the template's purpose (free-form
inference with cited evidence); if the template is empty/generic (< 3
meaningful text blocks, no tables, no header/footer text), the agent must
propose 2–3 likely purposes and ask the user (purpose + needed info +
optional sample file) — never invent a purpose.

## 5. Placeholders (`{{name}}` / `[[name]]`)

Token syntax (both accepted): `{{ten_du_an}}`, `[[ngay_ky]]` — name matches
`[A-Za-z0-9_.-]+`, optional inner spaces. Detection scans body + tables +
headers/footers at `--import` (raw list in `_extracted.placeholders_found`);
the agent presents each for user confirmation and only confirmed entries land
in yaml `placeholders:` (`<tên>.value` + `<tên>.description`).

Fill priority at export: `--param name=value` (one-shot, not saved) >
`placeholders.<name>.value` (non-empty) > top-level yaml scalar of the same
name (e.g. `{{company_name}}` → `company_name`). Tokens without value stay
intact and abort the export with the missing-name list (exit 2) — the agent
asks the user to map/input, then reruns with `--param` or saves via `--update`.

Scope notes: headers/footers are always the template's own (kept, with filled
values) — nothing is ever generated. Tokens living only in the sample body
disappear at export (body is replaced by rendered content). `Code Block`
paragraphs are never scanned nor substituted (literal `{{ }}` in code samples).
