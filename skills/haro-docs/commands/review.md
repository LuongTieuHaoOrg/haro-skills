# Review (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs review`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** read `docroot` from `.haro-docs/config/project.yaml` before operating — never guess it. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first. Knowledge in `.haro-docs/knowledge/` is ground truth over scanned defaults (see `commands/knowledge.md`).
> Review is **read-only** on docs: the reviewed file is never written; only a new report file is written under `.haro-docs/reviews/` after asking.

## 10. Command `/haro-docs review <topic|file>` — Critical Review via Subagent Reviewers

Objectively research, analyze and evaluate a problem, idea, or doc file using critical thinking and logic. The skill dispatches reviewer subagent(s) ("đệ tử"), then synthesizes their reports into one verdict plus follow-up proposals. **Read-only on docs**: the reviewed file is never written; only a new report is optionally written under `.haro-docs/reviews/` after asking.

### Syntax

```
/haro-docs review Should we use microservices for this project?
/haro-docs review 04-architecture/02-components.md
/haro-docs review --no-agents The current pricing model has a flaw
```

### Workflow

1. **Parse target + load context (selective RAG)** — read `knowledge/index.yaml` (if exists), load only entries with `state: active` whose domain/tags match the topic. Read `.haro-docs/reviews/index.yaml` (if exists) to skip topics already reviewed and to cite past reports. Read `.haro-docs/config/status.yaml`: a `RELEASED` target counts as evidence-grade ground; an `UPDATING` target counts as context-only (findings on it are framed as draft feedback, never as verdicts over final ground). When the target is a doc path: read that file + nearby files in the same folder + glossary. When it is free text: lightly scan repo + doc-root for related evidence. State what was loaded (`sources: ...`) so reviewers can cite it.
2. **Resolve reviewers from `.haro-docs/config/agents.yaml`:**
   - When the file is missing: use a single inline `critic` with the default prompt from `features/agents.yaml` (single-critic mode).
   - When the file exists: show enabled agents (`id | role`) and let the user multi-select (picker tool when available, otherwise numbered list). Pre-select `default_reviewer`. Default mode is **single critic**; multi-agent runs only when the user selects 2+ agents or the topic explicitly needs research + critique.
   - `--no-agents` flag forces single inline critic, ignoring the config.
   - When the runtime has no subagent mechanism (no Task tool): **inline fallback** — run each selected reviewer sequentially in the current context, clearly labeled `Reviewer <id> (inline fallback)`, then synthesize. Never fail just because subagents are unavailable.
3. **Dispatch reviewers** — each reviewer receives: the topic/file content, the loaded context summary, and its own `role + prompt` from `agents.yaml`. Require a structured return:
   - `findings:` bullet list (claim → evidence `file:line` or `knowledge/<file>`)
   - `counter-arguments:` strongest opposing views
   - `verdict:` agree | conditionally-agree | disagree + reasons
   - `confidence:` high/medium/low per finding
   - `open questions:` what evidence is still missing
   Run selected agents in parallel when the runtime supports it.
4. **Synthesize (skill, not a subagent)** — cross-check reports into:
   - `Consensus:` points all reviewers agree on
   - `Conflicts:` points they disagree on (with who-says-what)
   - `Missing evidence:` what would settle the conflicts
   - `Overall verdict:` agree | conditionally-agree | disagree + 3–5 line rationale
   - `Risks & alternatives:` short list
   Reply in `language.response`. Be objective: report disagreements honestly instead of hiding them.
5. **Save report (ask first)** — ask `Save review report to .haro-docs/reviews/? (save / skip)`. On `save`, write `.haro-docs/reviews/RR-YYYYMMDD-HHmmss-<slug>.md` with frontmatter (`topic, verdict, reviewers, date, sources`) + the synthesis + per-reviewer summaries, then append one entry (`id | topic | verdict | reviewers | date | sources`) to `.haro-docs/reviews/index.yaml`. Never write without asking.
6. **Next-step popup** — after the synthesis, always propose follow-ups (picker when available): e.g. `generate <related file>`, `remember <new fact surfaced>`, `review again with more evidence`, `stop`. Wait for the pick; do NOT auto-run.

### Examples

```
/haro-docs review Should we use microservices for this project?
/haro-docs review 05-security/01-threat-model.md
/haro-docs review --no-agents Is the current SLA realistic?
```
