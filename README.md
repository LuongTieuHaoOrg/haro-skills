# haro-skills

A collection of agent skills built by Haro. Each skill lives in its own folder under `skills/`.

---

## Haro Docs

Manage project documentation (PLM docs for software) using the Atomic Content Blocks model: init structure, generate docs, critical review via subagents, knowledge memory.

Path: `skills/haro-docs/`

```bash
npx skills add https://github.com/LuongTieuHaoOrg/haro-skills.git --skill haro-docs
```

---

## Haro Crew

Turn a one-sentence product idea into a running app with a crew of specialist agents (index → plan → docs → build, atomic docs + client views) plus a view-only localhost web viewer.

Path: `skills/haro-crew/`

```bash
npx skills add https://github.com/LuongTieuHaoOrg/haro-skills.git --skill haro-crew
```

---

## Haro Docx Writer

Render enterprise-standard .docx for technical specs from markdown/text/pdf via named templates (`--list/--create/--update/--delete/--view/--validate/--export:<id>`); local + global registry.

Path: `skills/haro-docx-writer/`

```bash
npx skills add https://github.com/LuongTieuHaoOrg/haro-skills.git --skill haro-docx-writer
```

---

## Adding a new skill

1. Create `skills/<skill-name>/` with a `SKILL.md` (frontmatter `name`, `description`).
2. Keep skill assets (e.g. `templates/`) inside the skill folder.
3. Add one section above.
