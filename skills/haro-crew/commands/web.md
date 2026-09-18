# Web (Haro Crew reference)
> **STOP — READ THIS FILE FULLY BEFORE ACTING.** This file is the normative workflow for `/haro-crew web` and `/haro-crew web --stop`. Do not act, answer, edit, or call tools from memory: read every step below first. The reference always wins over memory.
> **Ground rules:** the web viewer is strictly view-only. No answers, decisions, or state changes ever happen in the browser — everything flows through chat with `agent_lead` per `shared/question-rules.md`.

## 7. Command `/haro-crew web` / `/haro-crew web --stop` — View-Only Progress Viewer

### Architecture (locked)

- Static files under `.haro-crew/web/` (`index.html`, `app.js`, `styles.css`, `vendor/js-yaml.min.js`, `vendor/marked.min.js`), copied once from the skill's `web/` template (never overwrite an existing copy).
- Served from the `.haro-crew/` workspace ROOT on `127.0.0.1` only (so `app.js` fetches `../*.yaml`, `../meetings/...`, `../docs/...` via relative paths over http — never `file://`, which browsers block).
- Server: `web/server.js` (Node.js stdlib only, zero dependencies — Node is guaranteed since skill install runs via `npx`). Default port `8791`.
- `app.js` parses YAML with vendored `js-yaml` and renders Markdown with vendored `marked` (both offline-safe, MIT-licensed, no CDN). No snapshots, no sync issues: F5 always shows current state.
- Tabs: Progress | Agents | Tasks | Decisions | Meetings | Docs | Run guide (see `web/app.js`).

### Workflow — open

> Assumes SKILL harness steps 1–2 done (workspace + language). Viewer stays view-only; the gate only ensures workspace + chat language.

1. Ensure `.haro-crew/web/` exists (copy from skill template if missing; never overwrite).
2. Check `.haro-crew/web/.port`: if a server already answers on that port → reuse it, print the existing URL, stop here.
3. Otherwise spawn detached: `node .haro-crew/web/server.js --root .haro-crew --port 8791`, write the port to `.haro-crew/web/.port`, print `http://127.0.0.1:8791/web/` in chat with one line: what the viewer shows + "refresh after each task".

### Workflow — stop (`--stop`)

1. Read `.haro-crew/web/.port`; kill the process listening on that port; delete the `.port` file.
2. Confirm `Web server stopped.` in chat.

### Fallback (no Node — should not happen, but cheap to cover)

If `node` is unavailable: print the workspace paths and note the viewer needs `node` (one-time install). Never downgrade to `file://` opening — it silently breaks fetching.
