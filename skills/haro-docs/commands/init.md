# Init (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs init`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).

## 5. Command `/haro-docs init [<project description>]`

Read the project state to decide what happens next. Runs any time, any number of times: fresh projects get the full structure; initialized projects get a refreshed read (re-scan + delta report, never touching user content).

### 5.1 Deep read (always runs first, read-only except refresh sync)

1. **Deep scan** — README (business domain, key features), source tree + tech stack signals (package.json / requirements / go.mod / pom.xml / Cargo.toml...), code scale estimate, existing docs inside and outside doc-root, `.haro-docs/` state (`config/project.yaml`, `config/schema.yaml`, knowledge file count, agents config).
2. **Docs reality** — when initialized: list the actual folder tree under doc-root (for each of `00-common` → `99-assets` show exists/missing, file count, and UPDATING/RELEASED breakdown from `.haro-docs/config/status.yaml`; paths missing from the map count as UPDATING). Check indexes: knowledge/reviews/elicitation file counts + first rows, agents enabled list.
3. **Synthesize — one response, chat text then tool call last (Turn discipline, `SKILL.md` Presentation rule item 6; LONG content):** block 1 = chat text with a **Project Note** (5–8 lines: initialized?, doc-root, docs coverage % RELEASED, top-3 gaps, tech stack, knowledge depth) plus an **Agent take** (2–3 lines: biggest risk, most worrying gap, proposed move + one-line reason); block 2 (FINAL, same response) = the next-command picker. Never end block 1 without block 2.
4. **Branch:**
   - Not initialized → continue the fresh workflow (§5.2 below).
    - Initialized → **refresh mode**: add missing doc files to `config/status.yaml` as `UPDATING` (the only write; never removes or rewrites user content), report the delta as the chat text block (new files, coverage change, still-open gaps), then close the SAME response with the next-command picker (`generate`, `review`, `knowledge --ingest`; Mode: single) and continue with the picked one after reading its workflow file.

### 5.2 Required workflow

1. **Scan the project** — reuse the §5.1 deep read above (no second scan); only dig deeper where §5.1 left blanks, to synthesize context: business domain, key features, code scale, technical constraints.
1b. **Agent analysis — one response, chat text then tool call last (Turn discipline, `SKILL.md` Presentation rule item 6):** block 1 = chat text with `Situation (3–5 lines from scan) → Assessment (risks, which docs to prioritize, anything suspicious in the stack) → My proposal (which deliverables first + why)`; block 2 (FINAL, same response) = the clarifying questions picker. Drop questions the analysis already answered.
2. **Proactively ask clarifying questions** — ask the user, offering suggestions based on scan results:
   - Product/solution goals (free-text)
   - Documentation audience (multiple: engineers / managers / customers / ...)
   - Scope (free-text) and technical depth (single: high-level | balanced | deep-dive)
   - Security/compliance requirements (multiple + free-text, e.g. GDPR, ISO 27001, ...)
   - Required output document types (multiple: BRD / PRD / SAD / ...)
   - **Reply language** — the language the agent uses in conversation: `en` or `vi`
   - **Documentation language** — the language of doc content: `en`, `vi`, or `vi-en` (definitions in shared/writing-rules.md (§9))
3. **Ask for the doc-root** — the user chooses (single):
   - `docs/` (traditional documentation folder), or
   - `.haro-docs/docs/` (contained within the skill workspace)
3b. **Decide conventions (compact, 4–6 questions)** — fixed rules need no questions (they live in `shared/writing-rules.md`); show them as read-only preview. Ask only project-specific conventions below, writing answers into `config/project.yaml` (`conventions:`, `audience.technical_depth`, `deliverables`), offering scan-based defaults:
   - Diagram tool (single) → `conventions.diagram_tool`: `mermaid | plantuml | drawio` (+ image fallback)
   - API spec format (single) → `conventions.api_format`: `openapi-yaml | md-table | both`
   - Tone & depth (single) → `audience.technical_depth`: `high-level | balanced | deep-dive`
   - RELEASED approver (free-text) → `conventions.approver`: single name/role, or per-domain approvers
   - Locked terms (free-text) → `conventions.locked_terms`: product/brand terms with fixed spelling, or `(none)`
   - Priority deliverables (multiple) → `deliverables`: which of BRD/PRD/SAD/... first, or `(all)`

   Unanswered items use the stated defaults. The conventions file is written at init step 5 with status RELEASED.
3c. **Agent setup (quick)** — run the shared flow in `shared/agents-setup.md`: present presets in chat, multi-pick roles, name each, pick the default, write on confirm. Skipping writes nothing — no `config/agents.yaml` is created, and the setup returns automatically the next time a command needs agents.
4. **Confirm the outline** — present the folder tree + specific file list (including the decided conventions); wait for user approval. When the project already holds docs outside the canonical tree, include a placement table `old path → new path` in this step and wait for per-row confirmation.
5. **Initialize** — after approval:
   - Create `.haro-docs/config/project.yaml` and `.haro-docs/config/schema.yaml` (from the skill's `templates/` directory) with `version: 1`, including the chosen `language.response` and `language.documentation`
   - Agents: when step 3c completed setup, `config/agents.yaml` already exists — leave it. When skipped, create nothing: the setup in `shared/agents-setup.md` returns automatically the next time a command needs agents.
   - Create `.haro-docs/config/status.yaml` from `templates/status.yaml` with every planned file listed as `UPDATING`
   - Create `.haro-docs/knowledge/index.yaml` from `templates/knowledge.yaml` with empty `entries: []`
   - Create `.haro-docs/reviews/index.yaml` from `templates/reviews.yaml` with empty `entries: []`
   - Create `.haro-docs/elicitation/index.yaml` from `templates/elicitation.yaml` with empty `entries: []`
   - Write `00-common/01-conventions.md` as a read-only view rendered from `config/project.yaml` (`conventions:`, `audience.technical_depth`, `deliverables`) with status RELEASED; create `02-references.md`, `03-abbreviations.md`, `04-glossary.md`, `05-traceability.md` as placeholders for `generate` to fill (status UPDATING)
   - Create the folder tree per the outline, each folder gets a `README.md` describing its scope
   - Create a root overview README at the doc-root following the outline in `shared/docs-structure.md` (Doc-root README outline), filling the tree and reading path from `config/schema.yaml` + `config/project.yaml`

### 5.3 After init — next-step popup

When init completes, always close with one response: chat text block summarizing what was created, then the next-step picker (FINAL) with **2–3 concrete smart suggestions** derived from the new state, e.g.:

- `generate 01-overview/01-problem-statement.md — foundational purpose is still empty`
- `config conventions — refine project-specific conventions when step 3b used defaults`
- `knowledge --ingest <seed fact from scan> — preserve stack/team facts`

Use the agent's question/picker tool when available, otherwise a numbered list. Mode: single (one next action). Wait for the user's pick; do NOT auto-run `generate` without confirmation.

### Examples

```
/haro-docs init E-commerce project with Next.js + PostgreSQL, team of 3 devs
/haro-docs init
```

With no description: still run the §5.1 deep read first, then follow the matching fresh/refresh branch.
