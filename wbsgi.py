import io
import socket
import sys
from email.utils import formatdate
from urllib.parse import urlsplit


class WSGIServer:
    def __init__(self, server_address, application):
        self.application = application
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(server_address)
        self.listen_socket.listen(1)

        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

    def serve_forever(self):
        while True:
            client_connection, _ = self.listen_socket.accept()
            try:
                self.handle_request(client_connection)
            finally:
                client_connection.close()

    def handle_request(self, client_connection):
        request_text = client_connection.recv(1024).decode("utf-8")
        method, target, version = request_text.splitlines()[0].split()

        url = urlsplit(target)
        headers_set = []

        def start_response(status, response_headers, exc_info=None):
            server_headers = [
                ("Date", formatdate(usegmt=True)),
                ("Server", "WSGIServer 0.2"),
            ]
            headers_set[:] = [status, response_headers + server_headers]

        env = {
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": io.StringIO(request_text),
            "wsgi.errors": sys.stderr,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "wsgi.run_once": False,
            "REQUEST_METHOD": method,
            "PATH_INFO": url.path,
            "QUERY_STRING": url.query,
            "SERVER_NAME": self.server_name,
            "SERVER_PORT": str(self.server_port),
        }

        result = self.application(env, start_response)
        status, response_headers = headers_set

        response = f"HTTP/1.1 {status}\r\n"
        for name, value in response_headers:
            response += f"{name}: {value}\r\n"
        response += "\r\n"

        body = b"".join(result)
        client_connection.sendall(response.encode("utf-8") + body)


SERVER_ADDRESS = ("", 8888)


def make_server(server_address, application):
    return WSGIServer(server_address, application)