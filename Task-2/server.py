
import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

# Connected clients grouped by role
publishers = set()
subscribers = set()

# Protect shared sets
clients_lock = threading.Lock()


def send_message(client_socket, message):
    """Send a complete newline-terminated message."""
    client_socket.sendall(
        (message + "\n").encode("utf-8")
    )


def broadcast(message):
    """Send a published message to all subscribers."""

    with clients_lock:
        current_subscribers = list(subscribers)

    for subscriber_socket in current_subscribers:
        try:
            send_message(subscriber_socket, message)

        except (ConnectionError, OSError):
            # The subscriber may have disconnected
            remove_client(subscriber_socket)


def remove_client(client_socket):
    """Remove a client from both role sets."""

    with clients_lock:
        publishers.discard(client_socket)
        subscribers.discard(client_socket)


def handle_client(client_socket, client_address):
    role = None

    try:
        # First message must identify the client's role
        role_data = client_socket.recv(1024)

        if not role_data:
            return

        role = role_data.decode("utf-8").strip()

        if role not in ("Publisher", "Subscriber"):
            send_message(client_socket, "Invalid role.")
            return

        # Register the client
        with clients_lock:
            if role == "Publisher":
                publishers.add(client_socket)
            else:
                subscribers.add(client_socket)

        print(f"{role} connected: {client_address}")

        # Subscribers only receive messages
        if role == "Subscriber":
            while True:
                data = client_socket.recv(1024)

                if not data:
                    break

                # Ignore unexpected subscriber messages

        # Publishers send messages to the broker
        else:
            while True:
                data = client_socket.recv(1024)

                if not data:
                    break

                msg = data.decode("utf-8")

                if msg == "terminate":
                    break

                print(f"Published: {msg}")
                broadcast(msg)

    except (ConnectionError, OSError):
        print(f"Connection lost: {client_address}")

    finally:
        remove_client(client_socket)
        client_socket.close()

        print(f"Disconnected: {client_address}")


# Create the listening socket
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)



server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Broker is listening on port {PORT}")

try:
    while True:
        client_socket, client_address = server_socket.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address),
            daemon=True
        )

        client_thread.start()

except KeyboardInterrupt:
    print("\nServer shutting down.")

finally:
    server_socket.close()
