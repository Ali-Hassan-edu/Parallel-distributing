# Multi-Threaded TCP Server and Client in Python

A simple multi-threaded TCP server and client built with Python's `socket` and `threading` modules. The server can handle many clients at the same time, and the client keeps exchanging messages with the server until the user types `exit`.

## Features

### Server
- Accepts and handles multiple clients simultaneously.
- Starts a new thread with `threading.Thread()` for every new client connection.
- Displays the **active thread name**, **client IP** and **port number** in the terminal for each connection.
- Uses a `threading.Lock` (`acquire()` and `release()`) for thread synchronization, so shared data and terminal output are not mixed up between threads.

### Client
- Connects to the server over TCP.
- Sends messages and shows the server's reply continuously.
- Closes the connection when the user types `exit`.

## Project Structure

```
.
├── server.py
├── client.py
├── README.md
    ├── 01-server-started.jpeg
    ├── 02-server-multiple-clients.jpeg
    ├── 03-client-1.jpeg
    └── 04-client-2.jpeg
```

## Requirements

- Python 3.x
- No external libraries (only the standard library: `socket`, `threading`)

## How to Run

1. Open a terminal and start the server:

   ```bash
   python server.py
   ```

2. Open a second terminal and start a client:

   ```bash
   python client.py
   ```

3. Open a third terminal and start another client to see multi-threading in action:

   ```bash
   python client.py
   ```

4. Type messages in each client. Type `exit` to close a client.

> On Windows you can also use `py server.py` and `py client.py`.

The server listens on `127.0.0.1:5000`.

## How It Works

1. The server creates a socket, binds it to `127.0.0.1:5000` and listens for connections.
2. The main thread waits on `accept()` for new clients.
3. When a client connects, a new thread is started to handle that client.
4. The main thread goes back to `accept()` to wait for the next client.
5. Each thread receives messages from its own client, replies, and closes the connection when the client exits.
6. A `Lock` is acquired before touching shared resources (such as printing or counters) and released afterwards.

## Output Screenshots

### 1. Server started and waiting for clients

![Server started](screenshots/01-server-started.jpeg)

### 2. Server handling multiple clients (Thread-1 and Thread-2)

Each new connection gets its own thread. The server prints the active thread name, client IP, port number and the number of active threads.

![Server with multiple clients](screenshots/02-server-multiple-clients.jpeg)

### 3. Client 1 exchanging messages with the server

![Client 1](screenshots/03-client-1.jpeg)

### 4. Client 2 connected at the same time

![Client 2](screenshots/04-client-2.jpeg)

## Concepts Used

- **Socket programming:** communication between two programs over a network using IP and port.
- **TCP:** reliable, connection-based protocol.
- **Multi-threading:** one thread per client so many clients can be served at once.
- **Thread synchronization:** `Lock` with `acquire()` and `release()` prevents race conditions on shared data.

## Author

Ali Hassan
