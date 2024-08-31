import threading


def DECLARATION() -> dict:
    return {
        "type": "drv",  # 3 letter type: ext, drv, svc
        "class": "serverinfra",
        "id": "iplistener",
        "name": "Internet Protocol Listener Driver",
        "version": "1.0.0",
        "description": "IP listener driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000,
        "functions": []
    }


import http.server
import socketserver
import System.stdio as stdio
import asyncio
from urllib.parse import urlparse, parse_qs

class CustomHandler(http.server.BaseHTTPRequestHandler):
    routes = {}

    def log_message(self, format, *args):
        stdio.println(f"HTTP: {format % args}", 3)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        params = parse_qs(parsed_path.query)
        if path in self.routes:
            # Call the associated function with path, params, and self as the httpSession
            exitCode, contentType, responseData = self.routes[path](path, params, self)
            self.send_response(exitCode)
            self.send_header("Content-type", contentType)
            self.end_headers()
            if responseData is None:
                self.wfile.write(b"")
            elif isinstance(responseData, bytes):
                self.wfile.write(responseData)
            else:
                self.wfile.write(responseData.encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")

    @classmethod
    def add_route(cls, path, func):
        cls.routes[path] = func

class Server:
    def __init__(self, port):
        self.port = port
        self.handler = CustomHandler
        self.httpd = socketserver.TCPServer(("", self.port), self.handler)
        self.server_task = None

    async def start(self):
        stdio.println(f"Serving on port {self.port}")
        self.server_task = asyncio.create_task(asyncio.to_thread(self.httpd.serve_forever))

    async def stop(self):
        stdio.println("Shutting down server...")
        self.httpd.shutdown()
        self.httpd.server_close()
        await self.server_task
        stdio.println("Server terminated.")


# Server instance
server = None

async def mainAsync(args: list, process):
    global server
    server = Server(53778)
    CustomHandler.add_route("/", lambda: "Welcome to KyneOS Server.")
    await server.start()
#
async def terminateAsync(code: int):
    stdio.println("Terminating server...")
    global server
    await server.stop()
    stdio.println("Goodbye")


def run():
    threading.Thread(target=asyncio.run, args=(mainAsync([], None),)).start()

def addRoute(path, func):
    CustomHandler.add_route(path, func)