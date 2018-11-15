import http.server
import socketserver

PORT = 8000

# This is set to serve local only on purpose.  QuickData is crap on security.  Don't expose it to the world.
ADDR = "127.0.0.1"

Handler = http.server.CGIHTTPRequestHandler

with http.server.HTTPServer((ADDR, PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
    
   