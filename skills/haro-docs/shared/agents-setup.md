# Agents setup (shared flow)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the shared agent-setup flow, called by `/haro-docs init` (§5.2 step 3c), `/haro-docs review` (lazy gate), and `/haro-docs config agents`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> Called only when agents are NOT set up: `.haro-docs/config/agents.yaml` missing or holding zero enabled entries.

## Setup flow

1. **Present presets (static table lives in `templates/agents.yaml` — never retype the full table into chat):** single multi-select picker call per `shared/question-rules.md` (Mode: multiple) whose question lists only the suggested (`on`) presets briefly and points to `templates/agents.yaml` for the full table. No separate text block.

   | Pick | Lens | Runs via | Suggested |
   |------|------|----------|-----------|
   | `critic` | logic, hidden assumptions, bias | inline | on |
   | `researcher` | evidence gathering, no judging | inline | on |
   | `po` | product value, scope, priority | inline | off |
   | `pm` | schedule, risk, resourcing | inline | off |
   | `lead` (`agent_lead`) | project orchestration & review | Task `agent_lead` | on |
   | `ba` (`agent_ba`) | business requirements, scope, acceptance | Task `agent_ba` | off |
   | `arch` (`agent_arch`) | system architecture & data modeling | Task `agent_arch` | off |
   | `uiux` (`agent_uiux`) | user experience & interface spec | Task `agent_uiux` | off |
   | `devops` (`agent_devops`) | infrastructure, CI/CD, runbooks | Task `agent_devops` | off |
   | `qa` (`agent_qa`) | testability & test strategy | Task `agent_qa` | off |
   | `reviewer` (`agent_reviewer`) | final quality gate & critical review | Task `agent_reviewer` | off |
   | `lead` | coordinates multi-reviewer synthesis | `@agent_lead` | off |
   | `expert` (`domain-expert`) | feasibility from practice | inline | off |
   | `custom (blank)` | your own persona | inline | off |

2. **Picker (Mode: multiple)** — tick roles to use. Suggested rows are pre-selected. Picking nothing (or `stop`) = **skip: write nothing, create no file**. Skipping is final for this turn; the setup returns automatically the next time a command needs agents.
3. **Name each pick (single per pick)** — default name = preset id. Rules: lowercase-hyphen, unique within the project. On clash, report and ask again — never overwrite silently.
4. **Invoke (default per preset, changeable)** — inline presets run as-is; `task` presets use `type` = filename stem (no typing needed); `command` asks for the `@name` (default `@agent_lead` for lead). `custom (blank)` creates `.haro-docs/agents/<name>.md` from `agents/_blank.md` for the user to fill.
5. **Default reviewer (single)** — pick from the named set (default `critic` when picked, else first pick).
6. **Write (only on confirm)** — confirm the summary table `name | preset | invoke | default?` first (`proceed / edit`), then write:
   - copy each picked template file into `.haro-docs/agents/` (only files still missing — never overwrite a user-tuned file);
   - write `.haro-docs/agents/index.yaml` entries (`id | file | model | enabled | template | invoke`);
     a fresh index file starts as `version: 1`, `updated_at: ""`, `entries: []`;
   - write `.haro-docs/config/agents.yaml` entries from the registry (with user names, invoke choices, default).
   Report what was created and return to the caller workflow.
