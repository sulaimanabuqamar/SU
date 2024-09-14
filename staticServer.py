import http.server
import socketserver

Handler = http.server.SimpleHTTPRequestHandler
PORT = 81
server: socketserver.TCPServer = None
def startServer():
    httpd = socketserver.TCPServer(("", PORT), Handler)
    # print(f"[Static Media Server] Serving files on port {PORT}")
    server = httpd
    server.serve_forever()
    server.shutdown()
def stopServer():
    server.shutdown()