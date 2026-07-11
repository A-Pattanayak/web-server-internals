# WSGI Server Notes

Namaste! This note explains the `wbsgi.py` program so future readers can understand not only what the code does, but also what happens under the hood.

This program is a tiny WSGI-compatible web server. It sits between a browser/client and a Python WSGI application.

```text
Browser / Client
      |
      | HTTP request over TCP
      v
WSGIServer in wbsgi.py
      |
      | environ + start_response
      v
WSGI Application
      |
      | status + headers + body
      v
WSGIServer
      |
      | HTTP response over TCP
      v
Browser / Client
```

Trust me, it is very simple once the request-response flow becomes clear.

## 1. What Problem This Program Solves

A normal Python web framework like Flask or Django does not directly talk to the browser socket by itself. Instead, a web server receives the HTTP request, converts it into a standard WSGI format, calls the Python application, and sends the response back to the browser.

This file is a learning version of that server.

It teaches:

- How a TCP socket accepts browser connections.
- How raw HTTP request text is read.
- How the request method, path, and query string are parsed.
- How the WSGI `environ` dictionary is built.
- How a WSGI application is called.
- How the final HTTP response is constructed and sent.

## 2. What Is WSGI?

WSGI stands for Web Server Gateway Interface.

It is a standard contract between:

- a web server
- a Python web application or framework

The server says:

```text
I will give you an environ dictionary and a start_response function.
```

The application says:

```text
I will call start_response with status and headers, then return response body bytes.
```

This is a very famous interview question because it explains how Python web frameworks connect to real web servers.

## 3. Main Parts Of The Program

The file has four important pieces:

```python
class WSGIServer:
    ...
```

This class owns the socket server and handles requests.

```python
SERVER_ADDRESS = ("", 8888)
```

This means the server listens on port `8888` on the local machine.

```python
def make_server(server_address, application):
    return WSGIServer(server_address, application)
```

This helper creates the server object with an application attached.

The application is not defined inside `wbsgi.py`. It is passed into the server from outside. That is the whole point of WSGI: the server and the application are separate.

## 4. Server Initialization

Inside `__init__`, the server creates a TCP socket:

```python
self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

What happens under the hood?

- `AF_INET` means IPv4.
- `SOCK_STREAM` means TCP.
- TCP gives reliable byte delivery between browser and server.

Then the server allows address reuse:

```python
self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

This helps restart the server quickly without waiting for the operating system to fully release the port.

Then the server binds and starts listening:

```python
self.listen_socket.bind(server_address)
self.listen_socket.listen(1)
```

The `listen(1)` means the socket is ready to accept connections, with a small connection queue.

## 5. The Infinite Server Loop

The `serve_forever` method keeps the server alive:

```python
while True:
    client_connection, _ = self.listen_socket.accept()
    try:
        self.handle_request(client_connection)
    finally:
        client_connection.close()
```

The key line is:

```python
client_connection, _ = self.listen_socket.accept()
```

This pauses the program until a browser connects.

When a browser visits:

```text
http://localhost:8888/hello
```

the browser opens a TCP connection to port `8888`. The server accepts that connection and passes it to `handle_request`.

The `finally` block is important because it closes the client connection even if an error happens while handling the request.

## 6. Reading The HTTP Request

Inside `handle_request`:

```python
request_text = client_connection.recv(1024).decode("utf-8")
```

The server reads up to `1024` bytes from the browser and converts those bytes into a string.

Example request:

```http
GET /hello?name=robot HTTP/1.1
Host: localhost:8888
User-Agent: browser
```

Then the first line is parsed:

```python
method, target, version = request_text.splitlines()[0].split()
```

For this request:

```text
method  = GET
target  = /hello?name=robot
version = HTTP/1.1
```

## 7. Parsing Path And Query String

The program uses:

```python
url = urlsplit(target)
```

This separates the requested path from the query string.

For:

```text
/hello?name=robot
```

the result is:

```text
url.path  = /hello
url.query = name=robot
```

This is better than storing the whole target as `PATH_INFO`, because WSGI expects the path and query string separately.

## 8. start_response

Inside `handle_request`, the program defines a nested function:

```python
def start_response(status, response_headers, exc_info=None):
    server_headers = [
        ("Date", formatdate(usegmt=True)),
        ("Server", "WSGIServer 0.2"),
    ]
    headers_set[:] = [status, response_headers + server_headers]
```

The WSGI application calls this function to give the server:

- HTTP status, such as `200 OK`
- response headers, such as `Content-Type: text/plain`

The server also adds its own headers:

- `Date`
- `Server`

The important concept is closure.

`start_response` is defined inside `handle_request`, but it can still access `headers_set` from the outer function.

What happens under the hood?

Python remembers the surrounding variables used by the nested function. That remembered environment is called a closure.

This line mutates the existing list:

```python
headers_set[:] = [status, response_headers + server_headers]
```

That allows the outer `handle_request` function to read the status and headers after the WSGI app has called `start_response`.

## 9. Building The WSGI environ

The `env` dictionary is the bridge between the server and the application:

```python
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
```

Required WSGI keys:

| Key | Meaning |
| --- | --- |
| `wsgi.version` | WSGI version being used |
| `wsgi.url_scheme` | Usually `http` or `https` |
| `wsgi.input` | Input stream for request body |
| `wsgi.errors` | Error stream |
| `wsgi.multithread` | Whether multiple threads are used |
| `wsgi.multiprocess` | Whether multiple processes are used |
| `wsgi.run_once` | Whether app runs only once |

Important CGI-style keys:

| Key | Meaning |
| --- | --- |
| `REQUEST_METHOD` | HTTP method, like `GET` |
| `PATH_INFO` | Requested path, like `/hello` |
| `QUERY_STRING` | Query string, like `name=robot` |
| `SERVER_NAME` | Server host name |
| `SERVER_PORT` | Server port |

The WSGI application can inspect this dictionary to decide what response to return.

## 10. Calling The WSGI Application

This is the most important line:

```python
result = self.application(env, start_response)
```

The server gives the app:

- `env`, containing request information
- `start_response`, used by the app to set status and headers

The app returns an iterable of bytes.

Example WSGI app:

```python
def app(environ, start_response):
    status = "200 OK"
    headers = [("Content-Type", "text/plain")]
    start_response(status, headers)
    return [b"Hello from WSGI"]
```

## 11. Creating The HTTP Response

After the app runs:

```python
status, response_headers = headers_set
```

Then the server creates the HTTP response start line:

```python
response = f"HTTP/1.1 {status}\r\n"
```

Example:

```http
HTTP/1.1 200 OK
```

Then it adds headers:

```python
for name, value in response_headers:
    response += f"{name}: {value}\r\n"
```

Then it adds a blank line:

```python
response += "\r\n"
```

In HTTP, the blank line separates headers from the body.

Finally, the body is joined:

```python
body = b"".join(result)
```

And the full response is sent:

```python
client_connection.sendall(response.encode("utf-8") + body)
```

## 12. Full Request-Response Flow

When the browser visits:

```text
http://localhost:8888/hello?name=robot
```

this happens:

1. Browser creates a TCP connection to port `8888`.
2. Server accepts the connection.
3. Browser sends an HTTP request.
4. Server reads the request bytes.
5. Server parses method, path, and query string.
6. Server builds the WSGI `environ`.
7. Server calls the WSGI application.
8. Application calls `start_response`.
9. Application returns response body bytes.
10. Server builds raw HTTP response text.
11. Server sends response bytes to browser.
12. Server closes the client connection.

## 13. Why This Design Is Cleaner Than A Raw Server

The earlier `webserver1.py` file directly sends the same hardcoded response for every request.

This WSGI version is cleaner because responsibilities are separated:

| Layer | Responsibility |
| --- | --- |
| `WSGIServer` | Socket, HTTP parsing, WSGI conversion, HTTP response |
| WSGI app | Business logic and response content |

This is similar to a clean React architecture.

In a Robot Fleet Manager frontend, we separate:

- UI components
- custom hooks
- API service functions
- state logic

Here we separate:

- socket server logic
- request parsing
- WSGI environment creation
- application response logic

Same principle: single responsibility.

## 14. Limitations Of This Learning Server

This server is good for learning, but it is not production-ready.

Limitations:

- It reads only `1024` bytes from the request.
- It handles one request at a time.
- It does not support concurrent clients.
- It does not fully parse HTTP headers.
- It does not handle POST request bodies properly.
- It does not handle malformed requests gracefully.
- It does not implement every detail of the WSGI specification.
- It does not support HTTPS.

That is okay. The purpose is to understand the foundation.

## 15. How It Connects To React

Imagine your React Robot Fleet Manager calls:

```javascript
fetch("http://localhost:8888/api/robots")
```

Behind the scenes:

1. React renders the component.
2. `useEffect` runs after render.
3. Browser sends an HTTP request to `/api/robots`.
4. This WSGI server receives the request.
5. The WSGI app returns robot telemetry JSON.
6. Browser gives JSON back to React.
7. React calls `setRobots(data)`.
8. React creates a new virtual DOM.
9. Reconciliation compares old virtual DOM with new virtual DOM.
10. React updates only the changed parts of the real DOM.

Let us dive deep into this important connection:

```text
Backend WSGI response
      |
      v
fetch() resolves
      |
      v
setState()
      |
      v
new virtual DOM
      |
      v
reconciliation
      |
      v
minimal real DOM update
```

The backend sends data. React turns that data into UI.

## 16. Quick Revision

| Concept | Meaning |
| --- | --- |
| Socket | Low-level network connection endpoint |
| TCP | Reliable connection protocol |
| HTTP | Web request-response message format |
| WSGI | Python standard between web server and web app |
| `environ` | Dictionary containing request/server information |
| `start_response` | Function used by app to set status and headers |
| Response body | Iterable of bytes returned by the WSGI app |
| Closure | Inner function remembering outer variables |

## 17. Mental Model

Remember this:

```text
Socket accepts the browser.
HTTP gives the message format.
WSGI gives the Python app contract.
The app decides the content.
The server sends bytes back.
```

For this program:

```text
client_connection.recv()
        |
        v
parse request
        |
        v
build environ
        |
        v
application(environ, start_response)
        |
        v
build HTTP response
        |
        v
client_connection.sendall()
```

This is the bridge from a raw socket server to real Python web frameworks.

