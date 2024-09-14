import http.server
import socketserver

Handler = http.server.SimpleHTTPRequestHandler
PORT = 81
httpd = None
def startServer():
    global httpd
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print(httpd)
    httpd.serve_forever()
def stopServer():
    global httpd
    print(httpd)
    if httpd:
        httpd.shutdown()
        httpd.server_close()