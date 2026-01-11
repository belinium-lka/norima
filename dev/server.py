
#!/usr/bin/env python3
"""Simple dev server scaffold created by `hem -c.dev go`.

Run: python3 dev/server.py
"""
import http.server
import socketserver

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    pass

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Dev server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Stopping dev server")
