from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir(os.path.dirname(__file__))

server = HTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler)
print("Attacker site on http://127.0.0.1:8000/attacker.html")
server.serve_forever()