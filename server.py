from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import threading
import ssl

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        cookie = SimpleCookie()
        cookie["session"] = "test_session"
        cookie["session"]["path"] = "/"
        cookie["session"]["httponly"] = True

        self.send_response(200)
        self.send_header("Content-type", "text/html")

        for morsel in cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

        self.end_headers()
        message = "Cookie set!"
        self.wfile.write(message.encode("utf-8"))

    def do_POST(self):
        cookies = SimpleCookie(self.headers.get("Cookie"))
        session_cookie = cookies["session"].value if "session" in cookies else "No cookie"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = f"Handling POST request! Found cookie: {session_cookie}"
        self.wfile.write(message.encode("utf-8"))

def run(server_class=ThreadingHTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    # Créer un contexte SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    
    # Appliquer le contexte SSL
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Starting https server on port {port}...")
    print(f"Running in thread: {threading.current_thread().name}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
