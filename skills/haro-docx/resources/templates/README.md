# resources/templates — deprecated

This folder held style `.docx` files in the old single-config design. It is
kept only for backward reference — do NOT add new files here.

New template registry (since the redesign):

- Local: `<project>/.haro-docx/templates/<id>/template.docx`
- Global: `~/.haro-docx/templates/<id>/template.docx`
  (`%USERPROFILE%\.haro-docx\templates\<id>\` on Windows)

Manage templates with:

```text
/haro-docx --list
/haro-docx --create:<id> <file.docx>
/haro-docx --export:<id> <file.md>
```
