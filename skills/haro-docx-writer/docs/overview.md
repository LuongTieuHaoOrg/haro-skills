# Overview (Haro Docx Writer reference)

`haro-docx-writer` turns user-provided sources (**markdown / text / pdf**) into a
`.docx` rendered through a **named template** (`<id>`), invoked via
`/haro-docx-writer ...`.

The template governs everything visual: its pages, styles, and header/footer
are used as-is. The export only renders fresh body content into it, fills
`{{name}}` / `[[name]]` placeholders from the template's YAML config, and
applies the YAML `page` block (size/orientation/margins) — see
`../shared/docx-style.md`.
