# Knowledge memory (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs remember` / `/haro-docs knowledge`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults.

## 1.1 Knowledge as Selective RAG (no vector DB)

Because vector search is not available, knowledge is organized for **index + frontmatter** retrieval:

- Each fact lives in a topic file named by domain: `business-*.md`, `technical-*.md`, `team-*.md`, `common-*.md`, `security-*.md`, etc. One domain keeps 1–3 topic files; each topic file holds all facts of its subject under headings (never one tiny file per fact).
- Every topic file carries YAML frontmatter as its machine-readable identity:
  ```md
  ---
  domain: business
  tags: [team, stid]
  summary: "One-line fact summary"
  updated: "YYYY-MM-DD"
  ---
  ```
- `.haro-docs/knowledge/index.yaml` is the single lookup source: one entry per file with `file | domain | tags | summary | updated | facts | state`. Agents read **only `index.yaml`** (small) to decide which files to load for the current task, then load only those files. Never load the whole `knowledge/` directory by default. Never hand-write `index.yaml` — it is produced from payload frontmatter by `remember` and `--reindex`.
- Use `index.yaml` before every `init` or `generate` turn that needs project context: read `index.yaml`, pick entries whose domain/tags match the task (e.g. business for BRD, technical/architecture for SAD), load only those files. Knowledge overrides scanned defaults when they conflict.

## 4. Command `/haro-docs remember / knowledge` — Project Knowledge Memory (Selective RAG)

Knowledge files are project facts the agent must remember and follow. They are stored as topic-scoped files so they can be loaded selectively without reading all memory.

### Storage

```
.haro-docs/knowledge/
├── index.yaml           # single lookup source — produced, never hand-written
├── business-*.md        # topic files with frontmatter (domain/tags/summary/updated)
├── technical-*.md
├── team-*.md
├── common-*.md
└── security-*.md
```

`index.yaml` entry shape (one per knowledge file):

```yaml
- file: "business-team.md"
  domain: "business"
  tags: [team, stid, pm]
  summary: "STID is company, PM is Hao, members Hao/Vu/Dai"
  updated: "2026-09-14"
  facts: 3
  state: active          # active | stale (marked by --clean)
```

Domains: `business`, `technical`, `team`, `common`, `security`, `quality`, `operations`, `guides` — pick the closest. The agent chooses the topic filename that best matches the content (e.g. `business-team.md` for team facts) so it can be found without loading all memory. Append new facts of the same subject into the matching topic file instead of creating a new file.

### Selective loading (RAG without vector DB)

Before any `init` or `generate` turn that needs project context:

1. Read `knowledge/index.yaml` if it exists (small, always).
2. Pick only entries whose `domain`/`tags`/`summary` match the current task (e.g. `business` for BRD/Proposal, `technical`+`architecture` for SAD/FSD, `team` for any task mentioning people) and whose `state` is `active`.
3. Load only those matched knowledge files. Do NOT load the whole `knowledge/` directory.

Knowledge is ground truth: when a knowledge file conflicts with scanned code/README, prefer knowledge.

### Hub (no subcommand)

`/haro-docs knowledge` with no subcommand opens a picker (Mode: single; picker tool when available, otherwise numbered list) — same hub pattern as `/haro-docs config`:

1. `List (list)` — list all knowledge files (read-only, see table below)
2. `Record new fact (remember)` — first ask `Enter the fact to record:`, then run the `remember` flow below with the entered text
3. `Reindex + compact (--reindex)` — rebuild the knowledge index from payload frontmatter + compact
4. `Clean stale memory (--clean)` — list stale/irrelevant knowledge, confirm per row, then remove

Calling with flags (`knowledge --reindex`, `knowledge --clean`, `knowledge <free text>`) skips the picker and runs that branch directly. After a branch finishes, ask `back to hub / stop`.

### Subcommands

| Subcommand | Behaviour |
|------------|-----------|
| `remember <free text>` | **Analyze → confirm → save.** Parse the free text, extract distinct facts, rewrite each into a canonical sentence (current-state style per shared/authoring.md (§9)), find the matching topic file for each (or name a new topic file when no subject matches). Compare new facts against `active` entries first; on conflict include a `Conflict: old A ↔ new B` block in the preview and save only on explicit per-conflict confirm (keep-both / replace / drop-new). Then show a preview table `file \| canonical content` + the new index entries. Then ask `Confirm? (yes / edit <corrections>)`. Only on `yes` (or after applying `edit` and a new `yes`) write the topic files and write the new entries into `index.yaml` (set `facts` to the file's fact count; increment `facts` when appending to an existing file). If the user says `edit`, re-render the preview with corrections and ask again. `knowledge <free text>` is an alias for this subcommand. Deduplicate first: when a fact already exists, report it instead of writing a duplicate. |
| `knowledge` (= `list`, hub option 1) | **List all knowledge** (no args). Read `index.yaml` and render the table plus file counts. Read-only. |
| `knowledge --reindex` | **Produce index + compact.** Read the frontmatter of every `knowledge/*.md`, write a fresh `index.yaml` from it, then compact: merge topic files of the same domain smaller than ~10 lines, deduplicate repeated sentences. Report `before N files → after M files`. No confirmation needed; report the result. |
| `knowledge --clean` | **Remove stale/irrelevant memory.** Scan `index.yaml` for candidates: `state: stale`, `updated` older than 90 days (or `--older-than <Nd>`), or summaries with no reference in code/docs. Show a table `file \| reason \| keep/delete proposal` and confirm **per row**. Only rows confirmed `delete` are removed; then write a fresh `index.yaml`. Never remove without per-row confirmation. |

Unknown subcommand for this group → `Unknown command 'X'. Valid: remember <text>, knowledge, knowledge --reindex, knowledge --clean.` then show this table. `help`/`--help`/`-h` also show it.

### Examples

```
/haro-docs remember STID is my company, I am PM, members are Hao (me), Vu (Backend) and Dai (Frontend)
/haro-docs knowledge
/haro-docs knowledge --reindex
/haro-docs knowledge --clean
/haro-docs knowledge --clean --older-than 30d
```
