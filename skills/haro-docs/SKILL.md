---
name: haro-docs
description: Manage project documentation structure using the Atomic Content Blocks model. Use when the user wants to initialize a documentation structure for a new project, organize existing documentation, aggregate complete documents (BRD, PRD, SAD, FSD...) from existing content blocks, critically review a problem/file via subagent reviewers, or manage project knowledge memory via remember/knowledge. Run /haro-docs with no args to scan the project and pick the next action. Before acting on any command, read its commands/*.md file fully — never act from memory.
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

> **Important:** `config/project.yaml` records the **doc-root** — the documentation location chosen by the user during `init`. Every command (`generate`, `remember`, `knowledge`) reads this config first. Never guess the doc-root.

> **Read order (every command):** `config/project.yaml` → `config/schema.yaml` → `config/status.yaml` → `knowledge/index.yaml` (read this first, not the payloads) → selectively load only the matching payload files. Knowledge counts as ground truth over scanned defaults. Agents resolve via `config/agents.yaml` + `agents/index.yaml` when review/config needs them. See the command's workflow file for details.

> **Language settings:** `config/project.yaml` also records the **reply language** (`language.response`) and the **documentation language** (`language.documentation`). These are the single source of truth for all communication and content decisions — see shared/writing-rules.md (§9). If they are empty or missing, ask the user before running any command.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row.
> 2. Read that workflow file **fully, before any other tool call or answer** — the no-args dashboard (§3 below) is the only workflow that runs directly from this file.
> 3. If you notice you are about to act, answer, or create anything without the workflow open, **STOP and read it first**. Acting from memory, habit, or a previous session instead of the workflow is a workflow violation: **the workflow always wins over memory**, even when you are confident. This applies equally to small/weak models — when in doubt, re-read.

## Presentation rule — chat first, picker second (all commands)

1. Render every content (assessment, outlines A/B, remember preview, review synthesis, dashboard) **fully in chat text first**.
2. Pickers hold **choice options only** — short labels (≤1 line each, pointing "see details above"). Never compress content into options to save context.
3. Order is mandatory: chat message(s) first, **then** invoke the picker tool — never merged.
4. Every option uses natural communication language (`language.response`): a plain name plus its consequence in one line. Internal tokens (`UPDATING/RELEASED`, `unsure/defer/skip`, `save/skip`, `keep/remove`, `yes/no`) appear only in parentheses, never as bare labels.
5. Every picker declares its mode: `single` by default; `multiple` only for reviewer selection and file-candidate queues (queued files run sequentially in picked order; `stop` ends the queue anytime).

## Command index

| Command | When to use | Read first (fully, before acting) | Example |
|---------|-------------|-----------------------------------|---------|
| `/haro-docs` (no args) | Scan project, show dashboard, pick next action | — (runs from §3 below) | `/haro-docs` |
| `/haro-docs init <description>` | Initialize the documentation structure for a new project | `commands/init.md` | `/haro-docs init E-commerce Next.js + PostgreSQL` |
| `/haro-docs generate` | Build next doc (guided Q&A) | `commands/generate.md` + `shared/writing-rules.md` when writing | `/haro-docs generate` |
| `/haro-docs generate <file>` | Focus on a specific file | `commands/generate.md` + `shared/writing-rules.md` when writing | `/haro-docs generate 02-business/01-value-prop.md` |
| `/haro-docs review <topic\|file>` | Critically review a problem/file via subagent reviewer(s) | `commands/review.md` | `/haro-docs review Should we use microservices?` |
| `/haro-docs remember <free text>` | Record knowledge (analyze → confirm → save) | `commands/knowledge.md` | `/haro-docs remember STID is my company` |
| `/haro-docs knowledge` | Open hub picker (list / remember / reindex / clean) | `commands/knowledge.md` | `/haro-docs knowledge` |
| `/haro-docs knowledge --reindex` | Rebuild the knowledge index from payload frontmatter + compact | `commands/knowledge.md` | `/haro-docs knowledge --reindex` |
| `/haro-docs knowledge --clean` | List stale/irrelevant knowledge, confirm per row, then remove | `commands/knowledge.md` | `/haro-docs knowledge --clean` |
| `/haro-docs config [agents\|conventions\|language]` | Manage config via hub picker | `commands/config.md` | `/haro-docs config` |

## Writing rules (summary — full text in `shared/writing-rules.md`)

- Single Source of Truth: write once, assemble — never duplicate.
- Conversation uses `language.response`, doc content uses `language.documentation` (`en` | `vi` | `vi-en`); if missing, ask first.
- Write current state as the first version — no change-log phrasing, no version history in bodies (git owns versions).
- `RELEASED` means final and must-follow; `UPDATING` means reference-only.

## 3. Command `/haro-docs` (no args) — Project Scan + Status Dashboard + Action Picker

When the user runs `/haro-docs` with no arguments, or with arguments that do not match any configured command, do NOT execute a workflow. Instead run a **deep read-only scan** and show the dashboard + action picker:

1. **Deep scan (read-only)** —
   - If `.haro-docs/config/project.yaml` and `.haro-docs/config/schema.yaml` exist: read `docroot`, `language.*`, `version`; list the actual folder tree under doc-root (for each of `00-common` → `99-assets` show exists/missing, file count, and UPDATING/RELEASED breakdown from `.haro-docs/config/status.yaml`; paths missing from the map count as UPDATING).
   - If not initialized: show `Not initialized` and display the standard tree from shared/docs-structure.md (§8) as preview.
   - Check indexes: `knowledge/index.yaml` → `Knowledge: N files` + first 5 entries; `reviews/index.yaml` → `Reviews: N (latest verdict)`; `elicitation/index.yaml` → `Elicitation: N open`; `config/agents.yaml` (≥1 enabled) → `Agents: <ids> (default: <id>)`. Missing file → `Knowledge: (empty)` / `Reviews: (none)` / `Elicitation: (none)` / `Agents: (not set up — offered on first use)`.
   - Scan the repo lightly: README (business domain, key features), top-level source tree + tech stack signals (package.json / requirements / go.mod / pom.xml / Cargo.toml...), code scale estimate, docs files lying outside doc-root (if any).
   - Synthesize a **Project Note**: 5–8 lines on current state — initialized?, doc-root, docs coverage (% RELEASED), biggest gaps (top-3 empty folders/files), tech stack, knowledge depth.
   - Synthesize an **Agent take** (apart from the neutral picker in step 4): 2–3 lines of the agent's own view — biggest risk, most worrying gap, proposed move + one-line reason. Step-4 recommendations derive from it.
2. **Show command summary:** render the Command index table above (with examples).

3. **Show Aggregation Matrix (compact)** — BRD/PRD/SAD/FSD source folders from shared/docs-structure.md (§7).
4. **Action picker (popup)** — after the dashboard, always ask the user what to do next (use the agent's question/picker tool when available, otherwise a numbered list). Pre-suggest **2–3 smart recommendations** based on the scan, e.g.:
   - E.g.: not initialized → `init`; `01-overview`/`02-business` empty → `generate <that file>`; many `RELEASED` + no recent review → `review <topic>`; knowledge empty → `remember <seed facts>`.
   The user may pick a suggestion or name any other command. Once picked, follow the MANDATORY ROUTING above: read that command's workflow file fully before acting. Do NOT auto-run side effects without that command's normal confirmations. Mode: multiple allowed for file suggestions (they form a work queue in picked order); all other picks are single. Suggestion labels keep their one-line reasons; detail lives in chat per the Presentation rule.
5. **Do not create any file or write to any file.** If the first token is unknown (e.g. `/haro-docs foo`), prefix the dashboard with `Unknown command 'foo'. Valid: init, generate, review, remember, knowledge, knowledge --reindex, knowledge --clean, config.` and suggest the closest match. Also handle `help`, `--help`, `-h` as aliases for this dashboard. Matching is case-insensitive, trim whitespace.
