# Discover (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew discover`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** only `agent_lead` talks to the user, always following `shared/qa-rules.md`. Every question ships with 2–4 proposed answers + free-text. `unsure`/`skip` → agent default recorded as `unconfirmed` (`[UNCONFIRMED]`), never blocks.

## 1. Command `/haro-crew discover` — Deep-Dive the 5 Axes

### The 5 axes (ask in order, one axis per turn)

1. **Goal** — why this product exists, what success looks like. Proposals: revenue-focused / operations-efficiency / customer-experience (+ free-text).
2. **Users** — who uses it and in what roles. Proposals derived from the idea (e.g. restaurant: owner, staff/waiter, cashier, chef; plus end customers if ordering online).
3. **Scale** — size and load. Proposals: single-location small team / multi-branch / chain + expected daily transactions (small <100 / medium <1000 / large+).
4. **Scope** — feature areas in / out. Proposals: a must-have core list (4–6 areas inferred from the domain) vs nice-to-have; user ticks via multiple picker + free-text additions. Explicitly ask what is OUT of scope.
5. **Constraints** — budget, timeline, compliance, existing systems. Proposals: timeline (MVP 2–4 weeks / standard 1–3 months / no rush), hosting preference (cloud / on-premise / undecided), integrations (payments / printers / none).

### Workflow

1. **Load context** — read `config/project.yaml` + `decisions.yaml` (skip axes already `confirmed`).
2. **Per axis — one response, chat text then tool call last (Turn discipline, `shared/qa-rules.md` §2b):** block 1 = chat text with the axis context + the 2–4 proposals; block 2 (FINAL, same response) = the picker/question (Mode: single, or multiple for scope features). Record each answer immediately into `decisions.yaml` (`axis | question | answer | status: confirmed|unconfirmed | decided_at`).
3. **Defaults for `unsure`/`skip`:** pick the most standard option for the domain (defaults: efficiency goal, single-location scale, MVP timeline, Next.js + PostgreSQL stack later at blueprint), flag `[UNCONFIRMED]`.
4. **Wrap-up (chat):** render the full decision table (axis | answer | confirmed/[UNCONFIRMED]) + open items count.
5. **Next-step popup** (Mode: single): `Run blueprint meeting (recommended)` / `Re-answer an axis` / `Open web viewer` / `Stop`. On blueprint, read `commands/blueprint.md` fully first.
6. Set `phase: discover` in `config/project.yaml` at start; set `phase: blueprint` when moving on.
