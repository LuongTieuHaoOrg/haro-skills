# Meeting (Haro Docs reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-docs meeting`. Do not act, answer, edit, or call tools from memory: read every step below first. If in doubt at any point, re-read. The reference always wins over memory.
> **Ground rules (apply to every action in this file):** Read `docroot` from `.haro-docs/config/project.yaml` before operating. Respect `language.response` (conversation) and `language.documentation` (doc content); if either is missing, ask the user first.

## 11. Command `/haro-docs meeting [<topic>]` — Multi-Agent Collaborative Discussion Room

Initiate a structured multi-agent collaborative meeting where selected specialist agents discuss, debate, and analyze a problem under the coordination of a designated Lead agent. The conversation is logged into an active meeting YAML file, and the user can interact (human-in-the-loop) at any time.

### Syntax

```
/haro-docs meeting
/haro-docs meeting Should we adopt a micro-frontend architecture?
```

### Workflow

1. **Initialize & Clarify Topic / Goal:**
   - **Case 1 (No argument `/haro-docs meeting`):** Ask the user: 
     1. *"What topic or problem would you like to discuss in this meeting?"* (Capture input).
     2. *"What is the primary goal you want to achieve from this meeting?"* (Capture input).
   - **Case 2 (With argument `/haro-docs meeting <topic>`):** 
     - Read the provided topic. 
     - Confirm with user: *"You want to discuss: '<topic>'? [Confirm / Edit]"*.
     - Confirm goal: *"The primary goal is: '<goal>'? [Confirm / Enter goal]"*.

2. **Select Participants:**
   - Scan `.haro-docs/agents/` or read `.haro-docs/agents/index.yaml` to list available agents (e.g., `agent_ba`, `agent_arch`, `agent_uiux`, `agent_devops`, `agent_qa`, `agent_reviewer`).
   - Present the list to the user for multi-selection (Mode: multiple).
   - *If no agents exist or list is empty:* Notify the user and offer assistance to create new agents from `agents/_blank.md`.

3. **Select Lead (MC / Coordinator):**
   - Prompt the user to select **1 agent** from the chosen participant list to act as the Meeting Lead (default suggestion: `agent_lead` if present, else the first participant).

4. **Initialize Meeting Artifact (`.haro-docs/meetings/MT-YYYYMMDD-HHmmss-<slug>.yaml`):**
   - Copy or instantiate from `templates/meeting.yaml`.
   - Populate `meeting_id`, `created_at`, `topic`, `goal`, `lead_agent`, `participants`, and `rules`.

5. **Health Check (Smoke Test):**
   - Before officially kicking off, the Lead agent sends a lightweight probe (ping) to each participating agent: 
     *"System notice: You are assigned to a meeting about '[topic]'. Please acknowledge readiness."*
   - Evaluate response speed and semantic relevance:
     - If fast and coherent -> Mark ready.
     - If slow or incoherent -> Alert the user immediately: *"Warning: Agent [name] is responding slowly or returning unreliably. Would you like to switch its model or replace it with another agent?"*

6. **Official Kick-off & Discussion Loop (Round-robin Debate):**
   - The Lead agent formally opens **Round 1**, injects the meeting rules (professional analysis, structured arguments, examples, no raw source code), and dispatches the main prompt to participating agents in sequence.
   - **Full Transcript Logging:** The Lead agent records all verbatim responses into the active meeting YAML file under `rounds`.
   - **Round Summary:** At the end of each round, the Lead agent summarizes the core consensus and open disputes of that round (without bloating context with previous raw transcripts).
   - **Human-in-the-loop Interruption:** After each round summary is presented in chat to the user, the workflow pauses and waits for user input. The user can steer the meeting, ask clarifying questions, or conclude the session.

### Examples

```
/haro-docs meeting
/haro-docs meeting How to scale database connection pooling?
```
