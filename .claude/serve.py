"""Local preview server with live reload. Python standard library only.

Serves the project folder and injects a small script into each HTML page.
The script polls /__reload and reloads the page when any HTML, CSS or image
file changes.
"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
WATCH_EXT = (".html", ".css", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif")

SNIPPET = b"""<script>
(function () {
  var last = null;
  setInterval(function () {
    fetch('/__reload', { cache: 'no-store' })
      .then(function (r) { return r.text(); })
      .then(function (t) {
        if (last !== null && t !== last) location.reload();
        last = t;
      })
      .catch(function () {});
  }, 700);
})();
</script>
"""


def latest_mtime():
    newest = 0.0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in filenames:
            if name.lower().endswith(WATCH_EXT):
                try:
                    newest = max(newest, os.path.getmtime(os.path.join(dirpath, name)))
                except OSError:
                    pass
    return newest


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path == "/__reload":
            body = str(latest_mtime()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            path = os.path.join(path, "index.html")
        if path.endswith(".html") and os.path.isfile(path):
            with open(path, "rb") as f:
                html = f.read()
            if b"</body>" in html:
                html = html.replace(b"</body>", SNIPPET + b"</body>", 1)
            else:
                html += SNIPPET
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
            return

        super().do_GET()

    def log_message(self, fmt, *args):
        if "/__reload" not in (str(args[0]) if args else ""):
            super().log_message(fmt, *args)


if __name__ == "__main__":
    print(f"Serving {ROOT} with live reload at http://localhost:{PORT}")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
