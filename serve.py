#!/usr/bin/env python3
"""
Simple HTTP server for testing the Homeland Map locally.

Serves on all interfaces (0.0.0.0) so Windows hosts on the same LAN
can access via the WSL IP address. CORS headers are set on every response
so tiles loaded from CDN tile servers are not blocked.

Usage:
    python3 serve.py [port]

Default port: 8000
"""

import http.server
import socketserver
import sys
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Get the directory this script is in
SCRIPT_DIR = Path(__file__).parent.resolve()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SCRIPT_DIR), **kwargs)

    def end_headers(self):
        # Allow CORS so the map works when accessed from any origin
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        # Serve .js as application/javascript (Python's http.server may
        # serve it as text/plain on some systems, breaking ES modules)
        path = Path(self.path)
        if path.suffix == '.js':
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
        elif path.suffix == '.json':
            self.send_header('Content-Type', 'application/json; charset=utf-8')
        super().end_headers()

    def do_OPTIONS(self):
        """Handle preflight CORS requests."""
        self.send_response(200)
        self.end_headers()


if __name__ == '__main__':
    # Bind to all interfaces so Windows can access via WSL IP
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        # Find WSL IP for the user's convenience
        import subprocess
        try:
            result = subprocess.run(
                ['ip', 'addr', 'show', 'eth0'],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split('\n'):
                if 'inet ' in line:
                    wsl_ip = line.strip().split()[1].split('/')[0]
                    break
            else:
                wsl_ip = '127.0.0.1'
        except Exception:
            wsl_ip = '127.0.0.1'

        print(f"")
        print(f"  Métis Homeland Map — Server Running")
        print(f"  ────────────────────────────────────")
        print(f"  WSL (this terminal): http://localhost:{PORT}")
        print(f"  Windows browser:     http://{wsl_ip}:{PORT}")
        print(f"  Any device on LAN:   http://{wsl_ip}:{PORT}")
        print(f"")  
        print(f"  Press Ctrl+C to stop")
        print(f"")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")