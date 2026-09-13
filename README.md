# Socket Programming

This project demonstrates client-server communication with Python TCP sockets. Each task adds a new networking concept:

- **Task 1:** Basic one-client TCP communication.
- **Task 2:** A threaded publish/subscribe broker with publishers and subscribers.
- **Task 3:** Topic-based publish/subscribe messaging.

## Requirements

- Python 3.8 or later
- A terminal for the server
- One or more additional terminals for clients

No external packages are required.

## General Usage

Run the server before starting its client. Commands below assume that the terminal is opened in the relevant task directory. The default server port is `5000`; a different port can be supplied as the server's first argument.

Use `127.0.0.1` when the server and client run on the same computer. To connect from another computer, replace it with the server's IP address and ensure the selected port is reachable through the firewall.

## Task 1: Basic TCP Client and Server

The server accepts one client and prints messages received from it. The client sends interactive messages until `terminate` is entered.

### Start the server

```bash
cd Task-1
python3 server.py 5000
```

### Start the client in another terminal

```bash
cd Task-1
python3 client.py 127.0.0.1 5000
```

Enter messages at the client prompt. Type `terminate` to close the connection and stop the server.

## Task 2: Publish/Subscribe Broker

The broker accepts multiple clients concurrently:

- A **Publisher** sends messages to the broker.
- A **Subscriber** receives every message published by any publisher.

### Start the broker

```bash
cd Task-2
python3 server.py 5000
```

### Start a subscriber

```bash
cd Task-2
python3 client.py 127.0.0.1 5000 Subscriber
```

### Start a publisher

```bash
cd Task-2
python3 client.py 127.0.0.1 5000 Publisher
```

Run the subscriber before publishing so it can receive the messages. Type `terminate` in the publisher terminal to disconnect it. Press `Ctrl+C` in a subscriber terminal to disconnect that subscriber.

## Task 3: Topic-Based Messaging

Task 3 extends the broker so each publisher and subscriber joins a topic. A published message is delivered only to subscribers subscribed to the same topic.

### Start the server

```bash
cd Task-3
python3 server.py 5000
```

### Start a subscriber for a topic

```bash
cd Task-3
python3 client.py 127.0.0.1 5000 Subscriber sports
```

### Start a publisher for the same topic

```bash
cd Task-3
python3 client.py 127.0.0.1 5000 Publisher sports
```

Only subscribers using the `sports` topic receive those messages. For example, a subscriber connected to `news` will not receive messages published to `sports`.

Type `terminate` in a publisher terminal to disconnect it. Press `Ctrl+C` in a subscriber terminal to disconnect.

## Command Reference

```text
Task 1 server: python3 server.py [PORT]
Task 1 client: python3 client.py <IP_ADDRESS> <PORT>

Task 2 server: python3 server.py [PORT]
Task 2 client: python3 client.py <IP_ADDRESS> <PORT> <Publisher|Subscriber>

Task 3 server: python3 server.py [PORT]
Task 3 client: python3 client.py <IP_ADDRESS> <PORT> <Publisher|Subscriber> <TOPIC>
```

## Concepts Demonstrated

- TCP sockets using Python's `socket` module
- Binding and listening for connections
- Client-server message exchange
- Command-line arguments
- Concurrent client handling with `threading`
- Broadcasting messages to connected clients
- Topic-based message filtering
- Connection cleanup and graceful shutdown

