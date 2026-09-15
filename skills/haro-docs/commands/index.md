# Index (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the `/` landing and the fallback: it runs for `/haro-docs` with no arguments, for `help` / `--help` / `-h`, and for any unknown first token. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** reply in `language.response` when known (ask the user first when missing). This workflow is strictly read-only: never create or write any file.

## Index — Introduce + List Commands + Suggest

`haro-docs` organizes project documentation as Atomic Content Blocks (one file per section, written once) and assembles them into BRD/PRD/SAD/FSD. Full concept: `SKILL.md` §1.

1. **Introduce (chat, 3–4 lines)** — what the skill does + the single rule that matters here: every command's workflow lives in its own file (see routing below); docs state lives in `.haro-docs/`.
2. **List commands:** render the Command index table from `SKILL.md` (with examples). Do not duplicate it here.
3. **Light status (one check only):** when `.haro-docs/config/project.yaml` exists → `Initialized at <docroot>`; otherwise → `Not initialized — run init first`.
4. **Action picker (popup) — one response, chat text then tool call last (Turn discipline, `SKILL.md` Presentation rule item 6; SHORT content may live in the payload):** block 1 = chat text with the intro + light status; block 2 (FINAL, same response) = the next-action picker (Mode: single; picker tool when available, otherwise numbered list): list all 6 commands (`init`, `generate`, `review`, `knowledge`, `config`, `stop`) with one-line "when to use" each. When not initialized, pre-suggest `init`. Once picked, follow the MANDATORY ROUTING in `SKILL.md`: read that command's workflow file fully before acting. Do NOT auto-run side effects.
5. **Fallback (unknown token):** when the first token matches nothing (e.g. `/haro-docs foo`), prefix this index with `Unknown command 'foo'. Valid: init, generate, review, knowledge, knowledge --ingest, knowledge --index, knowledge --clean, knowledge --delete, config.` and suggest the closest match. Matching is case-insensitive, trim whitespace. For deep project reading, point to `/haro-docs init` (it re-reads state on every run).
