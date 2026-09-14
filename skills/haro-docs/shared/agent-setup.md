# Agent setup (shared flow)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the shared agent-setup flow, called by `/haro-docs init` (§5.2 step 3c), `/haro-docs review` (lazy gate), and `/haro-docs config agents`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> Called only when agents are NOT set up: `.haro-docs/config/agents.yaml` missing or holding zero enabled entries.

## Setup flow

1. **Present presets in chat first** — render the table below from the skill's `features/agents.yaml` (id | lens 1-line | runs via | suggested). Never compress it into picker options.

   | Pick | Lens | Runs via | Suggested |
   |------|------|----------|-----------|
   | `critic` | logic, hidden assumptions, bias | inline | on |
   | `researcher` | evidence gathering, no judging | inline | on |
   | `po` | product value, scope, priority | inline | off |
   | `pm` | schedule, risk, resourcing | inline | off |
   | `ba` (`sub_ba`) | requirements, flows, acceptance | Task `sub_ba` | off |
   | `arch` (`sub_arch`) | architecture, contracts, data model | Task `sub_arch` | off |
   | `sec` (`sub_sec`) | auth, vulnerabilities, hardening | Task `sub_sec` | off |
   | `qc` (`sub_qc`) | functional correctness, coverage | Task `sub_qc` | off |
   | `e2e` (`sub_e2e`) | user journeys, usability | Task `sub_e2e` | off |
   | `reviewer` (`sub_reviewer`) | final quality gate | Task `sub_reviewer` | off |
   | `docs` (`sub_docs`) | doc consistency | Task `sub_docs` | off |
   | `data` (`sub_data`) | SQL, data model, migration | Task `sub_data` | off |
   | `lead` | coordinates multi-reviewer synthesis | `@agent_lead` | off |
   | `expert` (`domain-expert`) | feasibility from practice | inline | off |
   | `custom (blank)` | your own persona | inline | off |

2. **Picker (Mode: multiple)** — tick roles to use. Suggested rows are pre-selected. Picking nothing (or `stop`) = **skip: write nothing, create no file**. Skipping is final for this turn; the setup returns automatically the next time a command needs agents.
3. **Name each pick (single per pick)** — default name = preset id. Rules: lowercase-hyphen, unique within the project. On clash, report and ask again — never overwrite silently.
4. **Invoke (default per preset, changeable)** — inline presets run as-is; `task` presets use `type` = filename stem (no typing needed); `command` asks for the `@name` (default `@agent_lead` for lead). `custom (blank)` creates `.haro-docs/agents/<name>.md` from `features/agents/_blank.md` for the user to fill.
5. **Default reviewer (single)** — pick from the named set (default `critic` when picked, else first pick).
6. **Write (only on confirm)** — confirm the summary table `name | preset | invoke | default?` first (`proceed / edit`), then write:
   - copy each picked template file into `.haro-docs/agents/` (only files still missing — never overwrite a user-tuned file);
   - write `.haro-docs/agents/index.yaml` entries (`id | file | model | enabled | template | invoke`);
   - write `.haro-docs/config/agents.yaml` entries from the registry (with user names, invoke choices, default).
   Report what was created and return to the caller workflow.
