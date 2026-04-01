import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

DB_NAME = "scores.db"
HOST, PORT = "localhost", 8000

class RequestHandler(BaseHTTPRequestHandler):
    def _json_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed = urlparse(self.path)
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if parsed.path == "/top":
            rows = cur.execute("SELECT Name, Score FROM scores").fetchall()
            if not rows:
                self._json_response(404, {"error": "No data"})
            else:
                max_score = max(r["Score"] for r in rows)
                top = sorted(r["Name"] for r in rows if r["Score"] == max_score)
                self._json_response(200, {"TopScorers": top, "Score": max_score})

        elif parsed.path == "/scores":
            query = parse_qs(parsed.query)
            name = query.get("name", [None])[0]
            if not name:
                self._json_response(400, {"error": "Name required"})
            else:
                row = cur.execute("SELECT Name, Score FROM scores WHERE Name=?", (name,)).fetchone()
                if row:
                    self._json_response(200, {"Name": row["Name"], "Score": row["Score"]})
                else:
                    self._json_response(404, {"error": "Person not found"})
        else:
            self._json_response(404, {"error": "Invalid endpoint"})

        conn.close()

    def do_POST(self):
        if self.path != "/scores":
            self._json_response(404, {"error": "Invalid endpoint"})
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length) or "{}")
        name = data.get("Name")
        score = data.get("Score")
        if not name or score is None:
            self._json_response(400, {"error": "Name and Score required"})
            return

        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO scores (Name, Score) VALUES (?, ?)", (name, score))
        conn.commit()
        conn.close()
        self._json_response(201, {"message": "Score added"})

#running the server
HTTPServer((HOST, PORT), RequestHandler).serve_forever()