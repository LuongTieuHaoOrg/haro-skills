# Overview (Haro Docx Writer reference)

`haro-docx-writer` turns user-provided sources (**markdown / text / pdf**) into a
company-standard `.docx` for technical specs, rendered through a **named
template** (`<id>`), invoked via `/haro-docx-writer ...`.

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
  (`000000`) — see `../shared/docx-style.md`.
