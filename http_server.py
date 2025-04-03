import os
import http.server
import threading
import socketserver

from .globals import SCRIPT_DIR
from .globals import GLB_PATH
from .globals import HTTP_PORT

generic_http_server = None
generic_http_server_thread = None

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class GenericHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)
    
    def do_GET(self):
        if self.path == "/scene.glb":
            try:
                with open(GLB_PATH, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "model/gltf-binary")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    fs = os.fstat(f.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(404, f"GLB file not found: {e}")
        else:
            super().do_GET()


def start_generic_http_server():
    global generic_http_server, generic_http_server_thread
    if generic_http_server is None:
        try:
            # Use the ReusableTCPServer to allow immediate reuse of the address
            generic_http_server = ReusableTCPServer(("localhost", HTTP_PORT), GenericHTTPRequestHandler)
            print(f"Starting generic HTTP server on http://localhost:{HTTP_PORT}")
            generic_http_server_thread = threading.Thread(target=generic_http_server.serve_forever, daemon=True)
            generic_http_server_thread.start()
        except Exception as e:
            print(f"Error starting HTTP server: {e}")

def stop_generic_http_server():
    global generic_http_server, generic_http_server_thread
    if generic_http_server is not None:
        print("Stopping generic HTTP server...")
        generic_http_server.shutdown()
        generic_http_server.server_close()
        generic_http_server = None
        if generic_http_server_thread is not None:
            generic_http_server_thread.join(timeout=1.0)
            generic_http_server_thread = None
