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

server.listen(PORT, "127.0.0.1", () => {
  const url = `http://127.0.0.1:${PORT}/web/`;
  console.log(`haro-crew web serving ${ROOT}`);
  console.log(url);
});
