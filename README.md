# Web Server From Scratch

> A tiny Python web server built from the ground up to understand how browsers, TCP sockets, and HTTP responses work together.

```text
Browser / Client  -->  TCP Connection  -->  Python Socket Server
Browser / Client  <--  HTTP Response   <--  Hello, World!
```

## Overview

Namaste! This repository is a hands-on learning project for understanding what a web server is actually doing behind the scenes.

Instead of starting with Flask, Django, Express, or any high-level framework, this project begins with a simple Python socket server. That keeps the focus on the foundation: connection, request, response, and the basic HTTP flow.

## Quick Facts

| Item | Details |
| --- | --- |
| Language | Python |
| Main file | `webserver1.py` |
| Server port | `8888` |
| Current response | `Hello, World!` |
| Frameworks used | None |
| Purpose | Learn web server fundamentals from scratch |

## What You Will Learn

- How a TCP socket is created in Python
- How a server binds to a host and port
- How the server waits for client connections
- What a raw HTTP request looks like
- How a basic HTTP response is sent back
- Why browsers, URLs, ports, TCP, and HTTP all matter

## Run The Server

From the project root:

```bash
python webserver1.py
```

Expected terminal output:

```text
Serving HTTP on port 8888 ...
```

Now open this in your browser:

```text
http://localhost:8888/hello
```

Expected browser response:

```text
Hello, World!
```

## Try More Paths

You can also open:

```text
http://localhost:8888/about
http://localhost:8888/api/robots
```

The response will still be:

```text
Hello, World!
```

That is intentional. The current server reads the request, but it does not parse routes yet. This is the first step before adding real path-based responses.

## Project Structure

```text
.
+-- README.md
+-- webserver1.py
+-- Notes/
    +-- Note1.md
```

## Learning Notes

The detailed notes live here:

- [Web Server Foundations](./Notes/Note1.md)

These notes explain the concepts step by step, including:

- URL parts: protocol, host, port, and path
- TCP vs HTTP
- Request-response flow
- How server data later connects to frontend apps

## Current Milestone

```text
[x] Create a basic TCP socket server
[x] Accept browser connections
[x] Print incoming HTTP request data
[x] Send a simple HTTP response
[ ] Parse the request path
[ ] Return different responses for different routes
[ ] Serve HTML content
```

## Mental Model

```text
URL tells the browser where to go.
TCP creates the connection.
HTTP defines the message format.
The server receives the request.
The server sends back a response.
The browser displays the response body.
```

## Why This Exists

Before using powerful backend frameworks, this repo focuses on one very important question:

```text
What is a web server actually doing under the hood?
```

Trust me, it is very simple once the request-response flow becomes clear.
