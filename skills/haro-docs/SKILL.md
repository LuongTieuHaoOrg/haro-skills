---
name: haro-docs
description: Manage project documentation structure using the Atomic Content Blocks model. Use when the user wants to initialize a documentation structure for a new project, organize existing documentation, aggregate complete documents (BRD, PRD, SAD, FSD...) from existing content blocks, critically review a problem/file via subagent reviewers, or manage project knowledge memory via knowledge (ingest, index, clean). Run /haro-docs with no args to scan the project and pick the next action. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Docs — Documentation Structure Skill

## 1. Overview

`haro-docs` organizes project documentation as **Atomic Content Blocks**: every small section is a separate markdown file, written exactly once (Single Source of Truth), then flexibly assembled into complete documents (BRD, PRD, SAD, FSD...).

- **Standardization:** every project has an identical documentation structure.
- **Atomicity:** each block is an independent object — easy to track and version.
- **Flexibility:** output documents are just different "Views" over the same blocks (see `shared/docs-structure.md`).
- **Knowledge memory:** project facts live as small domain-scoped files under `.haro-docs/knowledge/` and are loaded selectively like RAG — no vector DB (see `commands/knowledge.md`).
- **Two states:** every doc file is `UPDATING` (in progress, reference-only) or `RELEASED` (final, must-follow). Status lives only in `.haro-docs/config/status.yaml` — doc files carry no status themselves.

## 2. Workspace `.haro-docs/`

The skill stores all configuration and state in `.haro-docs/` at the project root.
Single-file YAMLs live together in `config/`; each multi-file feature (`knowledge/`, `reviews/`, `elicitation/`) manages itself through its own `index.yaml`. YAML files are the single source for everything the agent looks up; Markdown payloads carry YAML frontmatter.

```
.haro-docs/
├── config/
│   ├── project.yaml     # profile: type, audience, doc-root, language, version
│   ├── schema.yaml      # approved folder tree + aggregation matrix
│   ├── agents.yaml      # reviewer registry
│   └── status.yaml      # doc status: UPDATING | RELEASED
├── agents/              # project agent copies (<id>.md + index.yaml)
├── knowledge/           # topic files (business-*, technical-*, team-*, common-*.md + index.yaml)
├── elicitation/         # interim Q&A (<sanitized-path>.md + index.yaml)
└── reviews/             # reports (RR-*.md + index.yaml)
```

> **Important:** `config/project.yaml` records the **doc-root** — the documentation location chosen by the user during `init`. Every command (`generate`, `knowledge`) reads this config first. Never guess the doc-root.

> **Read order (every command):** `config/project.yaml` → `config/schema.yaml` → `config/status.yaml` → `knowledge/index.yaml` (read this first, not the payloads) → selectively load only the matching payload files. Knowledge counts as ground truth over scanned defaults. Agents resolve via `config/agents.yaml` + `agents/index.yaml` when review/config needs them. See the command's workflow file for details.

> **Language settings:** `config/project.yaml` also records the **reply language** (`language.response`) and the **documentation language** (`language.documentation`). These are the single source of truth for all communication and content decisions — see shared/writing-rules.md (§9). If they are empty or missing, ask the user before running any command.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row.
> 2. Read that workflow file **fully, before any other tool call or answer** — this file itself runs no workflow.
> 3. If you notice you are about to act, answer, or create anything without the workflow open, **STOP and read it first**. Acting from memory, habit, or a previous session instead of the workflow is a workflow violation: **the workflow always wins over memory**, even when you are confident. This applies equally to small/weak models — when in doubt, re-read.

## Presentation rule — chat first, picker second (all commands)

1. Render every content (assessment, outlines A/B, ingest preview, review synthesis, dashboard) **fully in chat text first**.
2. Pickers hold **choice options only** — short labels (≤1 line each, pointing "see details above"). Never compress content into options to save context.
3. Order is mandatory: chat message(s) first, **then** invoke the picker tool — never merged.
4. Every option uses natural communication language (`language.response`): a plain name plus its consequence in one line. Internal tokens (`UPDATING/RELEASED`, `unsure/defer/skip`, `save/skip`, `keep/remove`, `yes/no`) appear only in parentheses, never as bare labels.
5. Every picker declares its mode: `single` by default; `multiple` only for reviewer selection and file-candidate queues (queued files run sequentially in picked order; `stop` ends the queue anytime).

## Command index

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-docs` (no args) | Scan project, show dashboard, pick next action | `commands/index.md` | `/haro-docs` |
| `/haro-docs init <description>` | Initialize the documentation structure for a new project | `commands/init.md` | `/haro-docs init E-commerce Next.js + PostgreSQL` |
| `/haro-docs generate` | Build next doc (guided Q&A) | `commands/generate.md` + `shared/writing-rules.md` when writing | `/haro-docs generate` |
| `/haro-docs generate <file>` | Focus on a specific file | `commands/generate.md` + `shared/writing-rules.md` when writing | `/haro-docs generate 02-business/01-value-prop.md` |
| `/haro-docs review <topic\|file>` | Critically review a problem/file via subagent reviewer(s) | `commands/review.md` | `/haro-docs review Should we use microservices?` |
| `/haro-docs knowledge` | Open hub picker (list / ingest / index / clean / delete) | `commands/knowledge.md` | `/haro-docs knowledge` |
| `/haro-docs knowledge --ingest [<text>]` | Take new content in (propose from discussion, or direct) | `commands/knowledge.md` | `/haro-docs knowledge --ingest STID is my company` |
| `/haro-docs knowledge --index` | Rebuild the knowledge index from payload frontmatter + compact | `commands/knowledge.md` | `/haro-docs knowledge --index` |
| `/haro-docs knowledge --clean` | List stale/irrelevant knowledge, confirm per row, then remove | `commands/knowledge.md` | `/haro-docs knowledge --clean` |
| `/haro-docs knowledge --delete [<uid>]` | Remove one ingested fact by UID (or picker) | `commands/knowledge.md` | `/haro-docs knowledge --delete kb-0007` |
| `/haro-docs config [agents\|conventions\|language]` | Manage config via hub picker | `commands/config.md` | `/haro-docs config` |

## Writing rules (summary — full text in `shared/writing-rules.md`)

- Single Source of Truth: write once, assemble — never duplicate.
- Conversation uses `language.response`, doc content uses `language.documentation` (`en` | `vi` | `vi-en`); if missing, ask first.
- Write current state as the first version — no change-log phrasing, no version history in bodies (git owns versions).
- `RELEASED` means final and must-follow; `UPDATING` means reference-only.

## 3. Command `/haro-docs` (no args) — Index + Fallback

Runs from `commands/index.md` — read it fully before acting. (`init` owns the deep project read; see its §5.1.)
