"""Development server for Smart Photo Gallery visual shell."""

import http.server
import json
import os
import sys
from urllib.parse import urlparse

# Ensure the parent directory is in python path to import gallery package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from gallery.core.engine import evaluate
from gallery.core.models import Request


class GalleryShellRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler that serves visual shell assets and handles API evaluations."""

    def __init__(self, *args, **kwargs):
        # Override the directory to serve assets from src/gallery/shell
        shell_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, directory=shell_dir, **kwargs)

    def do_POST(self):
        """Intercepts and processes evaluation API requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/api/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode("utf-8"))
                event = data.get("event", "load_gallery")
                viewport_width = int(data.get("viewport_width", 1200))
                photo_id = data.get("photo_id", None)
                category = data.get("category", None)

                # Instantiate request and evaluate using Python Core engine
                core_request = Request(
                    event=event,
                    viewport_width=viewport_width,
                    photo_id=photo_id,
                    category=category,
                )

                decision = evaluate(core_request)

                # Serialize and return the decision
                response_payload = {
                    "outcome": decision.outcome,
                    "rule_ids": decision.rule_ids,
                    "evaluated_at": decision.evaluated_at,
                    "photos": [
                        {
                            "id": p.id,
                            "title": p.title,
                            "category": p.category,
                            "image_url": p.image_url,
                            "likes": p.likes,
                        }
                        for p in decision.photos
                    ],
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload).encode("utf-8"))

            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run(port=8080):
    """Runs the HTTP development server."""
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, GalleryShellRequestHandler)
    print(f"🚀 Smart Photo Gallery Visual Shell running at: http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping development server...")
        httpd.server_close()


if __name__ == "__main__":
    run()
