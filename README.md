# Web Server From Scratch

Namaste! This repository is a hands-on learning project for understanding how a web server works at the lowest level.

Instead of starting with a full backend framework, this project begins with a tiny Python socket server. The goal is to understand what happens behind the scenes when a browser sends an HTTP request and a server sends back a response.

## What This Project Covers

- Creating a TCP socket in Python
- Binding a server to a host and port
- Listening for browser/client connections
- Reading raw HTTP request data
- Sending a basic HTTP response
- Understanding the relationship between TCP, HTTP, URLs, clients, and servers

## Current Server

The main server file is:

```text
webserver1.py
```

It starts a small HTTP server on port `8888` and returns:

```text
Hello, World!
```

This server is intentionally simple. It does not use Flask, Django, Express, or any other web framework. That makes it easier to see the foundation clearly.

## How To Run

From the project root, run:

```bash
python webserver1.py
```

Then open this URL in your browser:

```text
http://localhost:8888/hello
```

You should see:

```text
Hello, World!
```

You can also try other paths:

```text
http://localhost:8888/about
http://localhost:8888/api/robots
```

The response will still be `Hello, World!` because the current server does not parse routes yet.

## Project Structure

```text
.
+-- webserver1.py
+-- README.md
+-- Notes/
    +-- Note1.md
```

## Learning Notes

The detailed beginner-friendly notes are here:

- [Web Server Foundations](./Notes/Note1.md)

Those notes explain the core concepts step by step, including URL parts, protocol, host, port, path, TCP vs HTTP, and how this foundation connects to React apps that call backend APIs.

## Goal

The goal of this repository is to build understanding first.

Before using high-level backend tools, this project helps answer an important question:

```text
What is a web server actually doing under the hood?
```

Trust me, it is very simple once the request-response flow becomes clear.
