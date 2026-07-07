# Web Server Foundations

Namaste! This note is a beginner-friendly recap of the core web-server concepts we covered. The goal is to understand the foundation behind browsers, servers, APIs, React apps, and backend frameworks.

## 1. The Big Picture

When you open a website or when a React app calls an API, a client and a server are communicating.

```text
Client                         Server
Browser / React app  ----->    Web server / API
                   request

Client                         Server
Browser / React app  <-----    Web server / API
                   response
```

A web server is a program that waits for requests from clients, processes them, and sends responses back.

Examples of clients:

- Browser
- React frontend using `fetch()`
- Postman
- curl
- telnet

Examples of servers:

- Python socket server
- Express.js server
- Django server
- Flask server
- Spring Boot server

## 2. URL Parts

Example URL:

```text
http://localhost:8888/hello
```

Basic structure:

```text
protocol://host:port/path
```

For this URL:

```text
protocol = http
host     = localhost
port     = 8888
path     = /hello
```

## 3. Protocol

A protocol is a set of rules for communication.

In this URL:

```text
http://localhost:8888/hello
```

the protocol is:

```text
http
```

HTTP defines how the browser and server should format requests and responses.

Example HTTP request:

```http
GET /hello HTTP/1.1
```

Example HTTP response:

```http
HTTP/1.1 200 OK

Hello, World!
```

Common protocols:

- `http` - HyperText Transfer Protocol
- `https` - Secure HTTP
- `ws` - WebSocket
- `ftp` - File Transfer Protocol

## 4. Host

The host tells the browser which machine/server to contact.

In:

```text
http://localhost:8888/hello
```

the host is:

```text
localhost
```

`localhost` means your own computer.

For a real website:

```text
https://www.google.com/search
```

the host is:

```text
www.google.com
```

## 5. Port

A port is like a door number on a machine.

One computer can run many services at the same time:

```text
React app      -> port 3000
Backend API    -> port 5000
Python server  -> port 8888
Database       -> port 5432
```

In:

```text
http://localhost:8888/hello
```

the port is:

```text
8888
```

This means:

```text
Go to my computer and knock on door 8888.
```

Default ports:

- HTTP usually uses port `80`
- HTTPS usually uses port `443`

That is why you normally do not type the port for websites like:

```text
https://example.com
```

The browser automatically assumes port `443`.

## 6. Path

The path tells the server what resource you want.

In:

```text
http://localhost:8888/hello
```

the path is:

```text
/hello
```

Examples:

```text
/users
/products
/api/robots
/api/robots/101
```

For a Robot Fleet Manager dashboard:

```text
http://localhost:5000/api/robots
```

means:

```text
protocol = http
host     = localhost
port     = 5000
path     = /api/robots
```

The React app is saying:

```text
Using HTTP, talk to the server on my computer, at door 5000, and ask for robot data from /api/robots.
```

## 7. HTTP vs TCP

This is a very famous interview question.

TCP is responsible for creating a reliable connection between two programs.

HTTP is the request-response format used on top of that connection.

Simple way to remember:

```text
TCP  = connection and reliable byte delivery
HTTP = rules for web request and response messages
```

Flow:

```text
Browser creates TCP connection
Browser sends HTTP request over TCP
Server sends HTTP response over TCP
Browser displays the response
```

## 8. What Happens When You Visit a URL?

When you open:

```text
http://localhost:8888/hello
```

what happens under the hood?

1. Browser reads the URL.
2. Browser identifies the protocol, host, port, and path.
3. Browser connects to the host and port using TCP.
4. Browser sends an HTTP request for the path.
5. Server receives the request.
6. Server sends an HTTP response.
7. Browser displays the response body.

## 9. Tiny Python Web Server

This is a very small web server:

```python
import socket

HOST, PORT = '', 8888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)

print(f'Serving HTTP on port {PORT} ...')

while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    print(request_data.decode('utf-8'))

    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""

    client_connection.sendall(http_response)
    client_connection.close()
```

## 10. Code Breakdown

Create a TCP socket:

```python
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

Meaning:

- `AF_INET` means IPv4
- `SOCK_STREAM` means TCP

Attach the socket to a host and port:

```python
listen_socket.bind((HOST, PORT))
```

Start listening for connections:

```python
listen_socket.listen(1)
```

Wait for a client:

```python
client_connection, client_address = listen_socket.accept()
```

Read the request:

```python
request_data = client_connection.recv(1024)
```

Send the response:

```python
client_connection.sendall(http_response)
```

Close the connection:

```python
client_connection.close()
```

## 11. Important Beginner Insight

The tiny server above always returns:

```text
Hello, World!
```

It does not matter whether you request:

```text
/hello
/about
/api/robots
```

Why?

Because the server is not yet parsing the request path. It simply reads some bytes and sends the same fixed response every time.

Real servers inspect the request method and path, then decide what response to send.

Example:

```text
GET /api/robots
```

could return:

```json
[
  { "id": 1, "name": "Robot A", "status": "active" },
  { "id": 2, "name": "Robot B", "status": "charging" }
]
```

## 12. How This Connects To React

In a React app, you may write:

```javascript
useEffect(() => {
  fetch("http://localhost:5000/api/robots")
    .then((res) => res.json())
    .then((data) => setRobots(data));
}, []);
```

Behind the scenes:

1. React component renders.
2. `useEffect` runs after render.
3. Browser sends an HTTP request to `/api/robots`.
4. Backend server returns JSON.
5. `setRobots(data)` updates React state.
6. React creates a new virtual DOM.
7. React reconciliation compares old virtual DOM and new virtual DOM.
8. React updates only the changed parts of the real DOM.

That is how server data becomes UI.

## 13. Clean React Architecture For API Data

Following a clean Namaste React style architecture, keep UI and data logic separate.

Example structure:

```text
src/
  components/
    RobotCard.jsx
    RobotList.jsx
  hooks/
    useRobots.js
  services/
    robotApi.js
  App.jsx
```

`services/robotApi.js`

```javascript
export const fetchRobots = async () => {
  const response = await fetch("http://localhost:5000/api/robots");

  if (!response.ok) {
    throw new Error("Failed to fetch robots");
  }

  return response.json();
};
```

`hooks/useRobots.js`

```javascript
import { useEffect, useState } from "react";
import { fetchRobots } from "../services/robotApi";

export const useRobots = () => {
  const [robots, setRobots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadRobots = async () => {
      try {
        const data = await fetchRobots();
        setRobots(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadRobots();
  }, []);

  return { robots, loading, error };
};
```

This keeps the component clean and focused on UI.

## 14. Mental Model To Remember

Use this mental model:

```text
URL tells the browser where to go.
TCP creates the connection.
HTTP defines the request and response.
Server processes the request.
React displays the returned data.
```

For the Robot Fleet Manager:

```text
React Dashboard
  -> HTTP request
  -> Backend web server
  -> Robot telemetry data
  -> HTTP response JSON
  -> React state update
  -> UI re-render
```

## 15. Quick Revision

| Term | Meaning | Example |
| --- | --- | --- |
| Protocol | Rules of communication | `http`, `https` |
| Host | Server/machine address | `localhost`, `google.com` |
| Port | Door number on the machine | `8888`, `3000`, `443` |
| Path | Resource requested from server | `/hello`, `/api/robots` |
| TCP | Reliable connection layer | Used before HTTP request |
| HTTP | Web request-response protocol | `GET /hello HTTP/1.1` |
| Client | Program making request | Browser, React app |
| Server | Program sending response | Python server, Express API |

## 16. Final Foundation

If you understand this flow, you have built a strong foundation:

```text
protocol://host:port/path
```

Example:

```text
http://localhost:8888/hello
```

Meaning:

```text
Use HTTP rules.
Talk to my own computer.
Use door 8888.
Ask for /hello.
```

Trust me, it is very simple once this picture becomes clear.

