# Team setup (shared flow)

> Called by `/haro-crew` (index) when `.haro-crew/config/staffing.yaml` is missing.
> Read `shared/question-rules.md` before acting — all questions follow those rules.

## Setup flow

1. **Present the crew (static table below — never retype it from memory):** per `shared/question-rules.md` — `<render text>` with the suggested roster, `<write history file>`, then a single multi-select picker (Mode: multiple) asking which members to activate.

   | Agent | Role | Suggested |
   |-------|------|-----------|
   | `agent_lead` | PM/MC — coordinates, only voice to the user | on (mandatory) |
   | `agent_ba` | Business analysis, requirements, scope | on |
   | `agent_arch` | Architecture, data model, stack | on |
   | `agent_uiux` | User journeys, screen flows, interface specs | on |
   | `agent_devops` | Environments, CI/CD, run config | on |
   | `agent_dev` | Implements code per task | on |
   | `agent_qa` | Test strategy, review gate | on |

2. **Picker (Mode: multiple)** — tick members to activate. `agent_lead` is mandatory and always on. Picking nothing besides lead = lead-only mode (specialists are consulted inline by lead when needed).
3. **Write (only on confirm)** — per `shared/question-rules.md` (`<render text>` what will be written → `<write history file>` → single picker `proceed / edit`), then write:
   - copy each agent persona from the skill's `agents/` into `.haro-crew/agents/` (only files still missing — never overwrite a user-tuned file);
   - write `.haro-crew/config/staffing.yaml` entries with `status: ready`.
   Report what was created and return to the caller workflow.
