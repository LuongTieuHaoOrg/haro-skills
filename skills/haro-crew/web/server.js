// Haro Crew web viewer — zero-dependency static file server (Node.js stdlib only).
// Serves the .haro-crew/ workspace ROOT (not web/ itself) so app.js can fetch
// ../decisions.yaml, ../meetings/..., ../docs/... via relative paths.
// Usage: node server.js [--root <path>] [--port <port>]
// Binds 127.0.0.1 only. Prints the URL to stdout for the agent to relay.

const http = require("http");
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const argVal = (flag, fallback) => {
  const i = args.indexOf(flag);
  return i >= 0 && args[i + 1] ? args[i + 1] : fallback;
};

// Default root = parent of this file's directory (i.e. .haro-crew/ when
// server.js lives at .haro-crew/web/server.js).
const ROOT = path.resolve(argVal("--root", path.join(__dirname, "..")));
const PORT = parseInt(argVal("--port", "8791"), 10);

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".yaml": "text/yaml; charset=utf-8",
  ".yml": "text/yaml; charset=utf-8",
  ".md": "text/markdown; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
};

const server = http.createServer((req, res) => {
  try {
    const urlPath = decodeURIComponent(req.url.split("?")[0]);
    // JSON directory-listing APIs so app.js never hardcodes file lists.
    if (urlPath === "/api/docs" || urlPath === "/api/meetings") {
      res.writeHead(200, { "Content-Type": "application/json; charset=utf-8" });
      res.end(JSON.stringify(urlPath === "/api/docs" ? listDocs() : listMeetings()));
      return;
    }
    let filePath = path.normalize(path.join(ROOT, urlPath === "/" ? "/web/index.html" : urlPath));
    if (!filePath.startsWith(ROOT)) {
      res.writeHead(403);
      res.end("Forbidden");
      return;
    }
    if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
      filePath = path.join(filePath, "index.html");
    }
    if (!fs.existsSync(filePath)) {
      res.writeHead(404);
      res.end("Not found: " + urlPath);
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, { "Content-Type": MIME[ext] || "application/octet-stream" });
    fs.createReadStream(filePath).pipe(res);
  } catch (err) {
    res.writeHead(500);
    res.end("Server error");
  }
});

// Recursively list *.md files under <ROOT>/docs, returned as paths
// relative to docs/ (e.g. "01-proposal/scope.md", "_views/01-proposal.md").
function listDocs() {
  const out = [];
  const walk = (dir, rel) => {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (err) {
      return;
    }
    entries.sort((a, b) => (a.isDirectory() === b.isDirectory() ? (a.name < b.name ? -1 : 1) : (a.isDirectory() ? -1 : 1)));
    for (const e of entries) {
      const full = path.join(dir, e.name);
      if (!full.startsWith(ROOT)) continue;
      if (e.isDirectory()) walk(full, path.join(rel, e.name));
      else if (/\.md$/i.test(e.name)) out.push(rel ? rel + "/" + e.name : e.name);
    }
  };
  walk(path.join(ROOT, "docs"), "");
  return out;
}

// List meetings: [{ id, meetingYaml, rounds: [<md paths>] }].
// app.js fetches + parses each meeting.yaml itself (vendored js-yaml).
function listMeetings() {
  const out = [];
  const base = path.join(ROOT, "meetings");
  let ids;
  try {
    ids = fs.readdirSync(base).sort();
  } catch (err) {
    return out;
  }
  for (const id of ids) {
    const dir = path.join(base, id);
    let st;
    try {
      st = fs.statSync(dir);
    } catch (err) {
      continue;
    }
    if (!st.isDirectory()) continue;
    const roundsDir = path.join(dir, "rounds");
    let rounds = [];
    try {
      rounds = fs.readdirSync(roundsDir).filter((f) => /\.md$/i.test(f)).sort()
        .map((f) => "meetings/" + id + "/rounds/" + f);
    } catch (err) { /* no rounds yet */ }
    const yamlPath = "meetings/" + id + "/meeting.yaml";
    if (!fs.existsSync(path.join(ROOT, yamlPath))) continue;
    out.push({ id, meetingYaml: yamlPath, rounds });
  }
  return out;
}

server.listen(PORT, "127.0.0.1", () => {
  const url = `http://127.0.0.1:${PORT}/web/`;
  console.log(`haro-crew web serving ${ROOT}`);
  console.log(url);
});
