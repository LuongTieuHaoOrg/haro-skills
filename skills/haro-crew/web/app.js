/* Haro Crew web viewer — view-only. Fetches source YAML/MD directly.
   No build step, no snapshots. Requires serving over http (see server.js),
   NOT file://. Uses vendored js-yaml + marked (offline-safe). */
"use strict";

const $ = (sel) => document.querySelector(sel);

async function fetchText(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
  return res.text();
}

async function fetchYaml(path) {
  const text = await fetchText(path);
  // Strip leading "#" comment lines so js-yaml stays happy with template files.
  return jsyaml.load(text);
}

function esc(s) {
  return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function badge(status) {
  return `<span class="badge ${esc(status)}">${esc(status)}</span>`;
}

const state = { project: null, staffing: null, decisions: null, tasks: null };

const TABS = [
  ["progress", "Progress"],
  ["agents", "Agents"],
  ["tasks", "Tasks"],
  ["decisions", "Decisions"],
  ["meetings", "Meetings"],
  ["docs", "Docs"],
  ["guide", "Run guide"],
];

function renderTabs(active) {
  $("#tabs").innerHTML = TABS.map(([id, label]) =>
    `<button data-tab="${id}" class="${id === active ? "active" : ""}">${label}</button>`).join("");
  document.querySelectorAll("#tabs button").forEach((b) =>
    b.addEventListener("click", () => show(b.dataset.tab)));
}

function show(tab) {
  renderTabs(tab);
  const el = $("#content");
  try {
    ({ progress: vProgress, agents: vAgents, tasks: vTasks, decisions: vDecisions,
       meetings: vMeetings, docs: vDocs, guide: vGuide })[tab](el);
  } catch (e) {
    el.innerHTML = `<div class="card"><h3>Error</h3><p class="dim">${esc(e.message)}</p></div>`;
  }
}

function vProgress(el) {
  const p = state.project || {};
  const tasks = (state.tasks && state.tasks.tasks) || [];
  const counts = {};
  tasks.forEach((t) => { counts[t.status] = (counts[t.status] || 0) + 1; });
  const decs = (state.decisions && state.decisions.decisions) || [];
  const unconf = decs.filter((d) => d.status === "unconfirmed").length;
  el.innerHTML = `
    <div class="card"><h3>${esc(p.name || "Untitled project")}</h3>
      <p>${esc(p.idea || "")}</p>
      <p class="dim">Goal: ${esc(p.goal || "—")} · Stack: ${esc(p.stack || "—")} · Phase: <b>${esc(p.phase || "?")}</b></p>
    </div>
    <div class="card"><h3>Tasks</h3><p>${Object.entries(counts).map(([k, v]) => `${badge(k)} ${v}`).join(" · ") || "No tasks yet"}</p></div>
    <div class="card"><h3>Decisions</h3><p>${decs.length} recorded · <span class="warn">${unconf} [UNCONFIRMED]</span></p></div>`;
}

function vAgents(el) {
  const crew = (state.staffing && state.staffing.crew) || [];
  el.innerHTML = `<div class="card"><h3>Crew (${crew.length})</h3>
    <table><tr><th>Agent</th><th>Status</th><th>Current task</th></tr>
    ${crew.map((a) => `<tr><td><code>${esc(a.id)}</code></td><td>${badge(a.status)}</td><td>${esc(a.current_task || "—")}</td></tr>`).join("")}
    </table></div>`;
}

function vTasks(el) {
  const tasks = (state.tasks && state.tasks.tasks) || [];
  if (!tasks.length) { el.innerHTML = `<div class="card"><p class="dim">No tasks yet — they appear after Phase 3 (docs).</p></div>`; return; }
  el.innerHTML = tasks.map((t) => `
    <div class="card"><h3><code>${esc(t.id)}</code> — ${esc(t.title)} ${badge(t.status)}</h3>
      <p>${esc(t.description)}</p>
      ${t.review_note ? `<p class="dim">Review: ${esc(t.review_note)}</p>` : ""}
    </div>`).join("");
}

function vDecisions(el) {
  const decs = (state.decisions && state.decisions.decisions) || [];
  if (!decs.length) { el.innerHTML = `<div class="card"><p class="dim">No decisions recorded yet.</p></div>`; return; }
  el.innerHTML = `<div class="card"><table><tr><th>Axis</th><th>Answer</th><th>Status</th></tr>
    ${decs.map((d) => `<tr><td><code>${esc(d.axis)}</code></td><td>${esc(d.answer)}<br><span class="dim">${esc(d.question || "")}</span></td>
    <td>${d.status === "unconfirmed" ? '<span class="warn">[UNCONFIRMED]</span>' : '<span class="ok">confirmed</span>'}</td></tr>`).join("")}
    </table></div>`;
}

async function vMeetings(el) {
  // Meeting list is derived from known meeting.yaml files — the viewer tries
  // the meetings index convention; missing files render as empty state.
  el.innerHTML = `<div class="card"><h3>Meetings</h3>
    <p class="dim">Meeting transcripts live under <code>.haro-crew/meetings/&lt;id&gt;/</code>.
    Open this viewer alongside the chat — the chair reports each round summary in chat.</p>
    <div id="mt-list"><p class="dim">Listing meetings requires a meetings index. See Run guide tab.</p></div></div>`;
}

async function vDocs(el) {
  const KNOWN = ["overview.md", "features.md", "architecture.md", "data-model.md", "tasks.md", "handover.md"];
  const found = [];
  for (const f of KNOWN) {
    try { found.push([f, await fetchText("../docs/" + f)]); } catch (e) { /* not yet generated */ }
  }
  if (!found.length) { el.innerHTML = `<div class="card"><p class="dim">No docs yet — they appear after Phase 3 (docs).</p></div>`; return; }
  el.innerHTML = found.map(([f, md]) =>
    `<div class="card"><h3><code>${esc(f)}</code></h3><div>${marked.parse(md)}</div></div>`).join("");
}

function vGuide(el) {
  el.innerHTML = `<div class="card"><h3>Run guide</h3>
    <p>This viewer is <b>read-only</b>. All answers and decisions happen in chat with <code>agent_lead</code>.</p>
    <ul>
      <li>Served from the <code>.haro-crew/</code> workspace root on <code>127.0.0.1</code> — refresh (F5) after the crew finishes a task to see fresh state.</li>
      <li>Source files: <code>config/project.yaml</code>, <code>config/staffing.yaml</code>, <code>decisions.yaml</code>, <code>knowledge/</code>, <code>tasks.yaml</code>, <code>meetings/</code>, <code>docs/</code>.</li>
      <li>Stop the server with <code>/haro-crew web --stop</code>.</li>
    </ul>
    <h3>Command Flow</h3>
    <ol>
      <li><code>/haro-crew kickoff &lt;idea&gt;</code> — Start project from a one-sentence idea.</li>
      <li><code>/haro-crew discover</code> — Deep-dive the 5 project axes (Goal, Users, Scale, Scope, Constraints).</li>
      <li><code>/haro-crew meeting [&lt;topic&gt;]</code> — Open an internal crew debate.</li>
      <li><code>/haro-crew blueprint</code> — Synthesize architecture, stack, and scope sign-off.</li>
      <li><code>/haro-crew docs</code> — Generate minimal internal documentation set.</li>
      <li><code>/haro-crew build</code> — Run the task queue (Code → Review → Report).</li>
      <li><code>/haro-crew handover</code> — Deliver docs, code, and run guide.</li>
    </ol></div>`;
}

(async function init() {
  try {
    const [project, staffing, decisions, tasks] = await Promise.all([
      fetchYaml("../config/project.yaml").catch(() => null),
      fetchYaml("../config/staffing.yaml").catch(() => null),
      fetchYaml("../decisions.yaml").catch(() => null),
      fetchYaml("../tasks.yaml").catch(() => null),
    ]);
    state.project = project; state.staffing = staffing;
    state.decisions = decisions; state.tasks = tasks;
    $("#project-name").textContent = (project && project.name) || "Haro Crew";
    $("#project-idea").textContent = (project && project.idea) || "";
    show("progress");
  } catch (e) {
    $("#content").innerHTML = `<div class="card"><h3>Cannot load workspace</h3>
      <p class="dim">${esc(e.message)}</p>
      <p class="dim">This viewer must be served over http (see server.js), not opened as file://.</p></div>`;
  }
})();
