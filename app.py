from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        try:
            path = os.path.join(os.path.dirname(__file__), 'index.html')
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        except Exception:
            self.wfile.write(b"<h1>Senior Daily Companion</h1>")
        return

def app(environ, start_response):
    try:
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        with open(path, 'rb') as f:
            content = f.read()
    except Exception:
        content = b"<h1>Senior Daily Companion</h1>"
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(content)))
    ]
    start_response(status, response_headers)
    return [content]

application = app
