# resources/templates — deprecated

This folder held style `.docx` files in the old single-config design. It is
kept only for backward reference — do NOT add new files here.

New template registry (since the redesign):

- Local: `<project>/.haro-docx-writer/templates/<id>/template.docx`
- Global: `~/.haro-docx-writer/templates/<id>/template.docx`
  (`%USERPROFILE%\.haro-docx-writer\templates\<id>\` on Windows)

Manage templates with:

```text
/haro-docx-writer --list
/haro-docx-writer --create:<id> <file.docx>
/haro-docx-writer --export:<id> <file.md>
```
