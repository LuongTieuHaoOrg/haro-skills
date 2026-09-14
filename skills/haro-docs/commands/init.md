# Init (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs init`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).

## 5. Command `/haro-docs init <project description>`

Initialize the documentation structure for a new project.

### 5.1 Check current state

1. **Scan first** — same deep scan as SKILL.md (§3): README, source tree + tech stack, existing docs (inside and outside doc-root), `.haro-docs/config/` state (`project.yaml`, `schema.yaml`, knowledge file count, agents config).
2. **When `.haro-docs/` already exists** — report `Already initialized` with the current profile (doc-root, languages, docs file count, knowledge N files) and stop. Point to the next commands (`generate`, `remember`, `review`).

### 5.2 Required workflow

1. **Scan the project** — read README, source code (tree structure, main technologies), and any existing docs to synthesize context: business domain, key features, code scale, technical constraints.
1b. **Agent analysis** — present `Situation (3–5 lines from scan) → Assessment (risks, which docs to prioritize, anything suspicious in the stack) → My proposal (which deliverables first + why)` **in chat first**, then proceed to clarifying questions. Drop questions the analysis already answered.
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

When init completes, always show a next-step picker with **2–3 concrete smart suggestions** derived from the new state, e.g.:

- `generate 01-overview/01-problem-statement.md — foundational purpose is still empty`
- `config conventions — refine project-specific conventions when step 3b used defaults`
- `remember <seed fact from scan> — preserve stack/team facts`

Use the agent's question/picker tool when available, otherwise a numbered list. Mode: single (one next action). Wait for the user's pick; do NOT auto-run `generate` without confirmation.

### Examples

```
/haro-docs init E-commerce project with Next.js + PostgreSQL, team of 3 devs
/haro-docs init
```

With no description: still scan the current project first, then start asking from step 2 of §5.2.
