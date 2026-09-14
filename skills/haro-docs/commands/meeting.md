# Meeting (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs meeting`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** Read `docroot` from `.haro-docs/config/project.yaml` before operating. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first.

## 11. Command `/haro-docs meeting [<topic>]` — Multi-Agent Collaborative Discussion Room

Initiate or resume a structured multi-agent collaborative meeting where specialist agents discuss, debate, and analyze a problem under the coordination of a designated Lead agent. 

### Storage Architecture
- Each meeting folder resides at `.haro-docs/meetings/<meeting_id>/`.
- Contains `meeting.yaml` (metadata, status, rounds index with structured English round summaries, and raw file pointers).
- Contains a `rounds/` subfolder storing individual raw answer markdown files (`round-<N>-<agent_id>.md`) in English to maintain deep technical context.

### Syntax

```
/haro-docs meeting
/haro-docs meeting Should we adopt a micro-frontend architecture?
```

### Workflow

1. **Initialize & Check Unfinished Meetings (Case 1 vs Case 2):**
   - **Case 1 (No argument `/haro-docs meeting`):**
     - Scan `.haro-docs/meetings/*/meeting.yaml` for any meetings with `status: "in-progress"`.
     - **If unfinished meetings found:** Display them in chat and present options:
       1. *Resume an existing meeting:* Select from the list.
       2. *Create a new meeting:* Proceed to prompt for topic and goal.
     - **If no unfinished meetings found (or user chooses new):** Ask the user:
       1. *"What topic or problem would you like to discuss in this meeting?"* (Capture input).
       2. *"What is the primary goal you want to achieve from this meeting?"* (Capture input).
   - **Case 2 (With argument `/haro-docs meeting <topic>`):**
     - Read the provided topic.
     - Confirm with user: *"You want to discuss: '<topic>'? [Confirm / Edit]"*.
     - Confirm goal: *"The primary goal is: '<goal>'? [Confirm / Enter goal]"*.
     - Create a new meeting.

2. **Select Participants (for New Meetings):**
   - Scan `.haro-docs/agents/` or read `.haro-docs/agents/index.yaml` to list available agents (e.g., `agent_ba`, `agent_arch`, `agent_uiux`, `agent_devops`, `agent_qa`, `agent_reviewer`).
   - Present the list to the user for multi-selection (Mode: multiple).
   - *If no agents exist or list is empty:* Notify the user and offer assistance to create new agents from `agents/_blank.md`.

3. **Select Lead (MC / Coordinator):**
   - Prompt the user to select **1 agent** from the chosen participant list to act as the Meeting Lead (default suggestion: `agent_lead` if present, else the first participant).

4. **Initialize or Resume Meeting Directory & Artifact:**
   - **For New Meeting:** Create directory `.haro-docs/meetings/MT-YYYYMMDD-HHmmss-<slug>/` and instantiate `meeting.yaml` from `templates/meeting.yaml` with `status: "in-progress"`, populating metadata. Also create `rounds/` subdirectory.
   - **For Resumed Meeting:** Load the selected `meeting.yaml` and verify its `rounds/` folder structure.

5. **Health Check (Smoke Test):**
   - Before kicking off or resuming, the Lead agent sends a lightweight probe (ping) in English to each participating agent: 
     *"System notice: You are participating in a meeting about '[topic]'. Please acknowledge readiness."*
   - Evaluate response speed and semantic relevance:
     - If fast and coherent -> Mark ready.
     - If slow or incoherent -> Alert the user immediately in `language.response`: *"Warning: Agent [name] is responding slowly or returning unreliably. Would you like to switch its model or replace it with another agent?"*

6. **Official Kick-off / Resume & Discussion Loop (Round-robin Debate):**
   - The Lead agent formally opens the discussion (or resumes from the last recorded round).
   - **Execution & Storage (Internal English):** 
     - Each participating agent writes their detailed analysis and arguments in English (structured points, examples, no raw source code).
     - Save each agent's raw response into `.haro-docs/meetings/<meeting_id>/rounds/round-<N>-<agent_id>.md`.
     - Record a short English `recap` sentence and a pointer (`raw_file`) in `meeting.yaml`.
   - **Structured Round Summary (Internal English, translated for User):** At the end of each round, the Lead agent writes a structured `summary_of_round` in English into `meeting.yaml`:
     ```yaml
     summary_of_round:
       consensus: [...]
       conflicts_or_disputes: [...]
       key_takeaways: [...]
       open_questions_for_next_round: [...]
     ```
   - **Human-in-the-loop Interruption:** Translate and present the structured summary in `language.response` (e.g. Vietnamese) to the user in chat. Wait for user instructions (continue, redirect, or conclude meeting with `status: "completed"`).

### Examples

```
/haro-docs meeting
/haro-docs meeting How to scale database connection pooling?
```
