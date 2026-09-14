# Dashboard (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs` with no arguments (or an unknown command). Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** reply in `language.response` from `.haro-docs/config/project.yaml` (ask the user first when missing). This workflow is strictly read-only: never create or write any file.

## 3. Command `/haro-docs` (no args) — Project Scan + Status Dashboard + Action Picker

When the user runs `/haro-docs` with no arguments, or with arguments that do not match any configured command, do NOT execute a workflow. Instead run a **deep read-only scan** and show the dashboard + action picker:

1. **Deep scan (read-only)** —
   - If `.haro-docs/config/project.yaml` and `.haro-docs/config/schema.yaml` exist: read `docroot`, `language.*`, `version`; list the actual folder tree under doc-root (for each of `00-common` → `99-assets` show exists/missing, file count, and UPDATING/RELEASED breakdown from `.haro-docs/config/status.yaml`; paths missing from the map count as UPDATING).
   - If not initialized: show `Not initialized` and display the standard tree from shared/docs-structure.md (§8) as preview.
   - Check indexes: `knowledge/index.yaml` → `Knowledge: N files` + first 5 entries; `reviews/index.yaml` → `Reviews: N (latest verdict)`; `elicitation/index.yaml` → `Elicitation: N open`; `config/agents.yaml` (≥1 enabled) → `Agents: <ids> (default: <id>)`. Missing file → `Knowledge: (empty)` / `Reviews: (none)` / `Elicitation: (none)` / `Agents: (not set up — offered on first use)`.
   - Scan the repo lightly: README (business domain, key features), top-level source tree + tech stack signals (package.json / requirements / go.mod / pom.xml / Cargo.toml...), code scale estimate, docs files lying outside doc-root (if any).
   - Synthesize a **Project Note**: 5–8 lines on current state — initialized?, doc-root, docs coverage (% RELEASED), biggest gaps (top-3 empty folders/files), tech stack, knowledge depth.
   - Synthesize an **Agent take** (apart from the neutral picker in step 4): 2–3 lines of the agent's own view — biggest risk, most worrying gap, proposed move + one-line reason. Step-4 recommendations derive from it.
2. **Show command summary:** render the Command index table from `SKILL.md` (with examples).

3. **Show Aggregation Matrix (compact)** — BRD/PRD/SAD/FSD source folders from shared/docs-structure.md (§7).
4. **Action picker (popup)** — after the dashboard, always ask the user what to do next (use the agent's question/picker tool when available, otherwise a numbered list). Pre-suggest **2–3 smart recommendations** based on the scan, e.g.:
   - E.g.: not initialized → `init`; `01-overview`/`02-business` empty → `generate <that file>`; many `RELEASED` + no recent review → `review <topic>`; knowledge empty → `remember <seed facts>`.
   The user may pick a suggestion or name any other command. Once picked, follow the MANDATORY ROUTING in `SKILL.md`: read that command's workflow file fully before acting. Do NOT auto-run side effects without that command's normal confirmations. Mode: multiple allowed for file suggestions (they form a work queue in picked order); all other picks are single. Suggestion labels keep their one-line reasons; detail lives in chat per the Presentation rule.
5. **Do not create any file or write to any file.** If the first token is unknown (e.g. `/haro-docs foo`), prefix the dashboard with `Unknown command 'foo'. Valid: init, generate, review, remember, knowledge, knowledge --reindex, knowledge --clean, config.` and suggest the closest match. Also handle `help`, `--help`, `-h` as aliases for this dashboard. Matching is case-insensitive, trim whitespace.
