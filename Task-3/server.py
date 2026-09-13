import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

# topic -> set of subscriber sockets
subscribers = {}

clients_lock = threading.Lock()


def broadcast(topic, message):

    with clients_lock:

        # Get subscribers interested in this topic
        topic_subscribers = subscribers.get(topic, set())

       
        current_subscribers = list(topic_subscribers)

    for subscriber_socket in current_subscribers:

        try:
            subscriber_socket.sendall(
                message.encode("utf-8")
            )

        except (ConnectionError, OSError):

            with clients_lock:
                subscribers.get(topic, set()).discard(
                    subscriber_socket
                )


def remove_subscriber(client_socket, topic):

    with clients_lock:

        if topic in subscribers:
            subscribers[topic].discard(client_socket)

            # Remove topic if no subscribers remain
            if not subscribers[topic]:
                del subscribers[topic]


def handle_client(client_socket, client_address):

    role = None
    topic = None

    try:

        data = client_socket.recv(1024)

        if not data:
            return

        role, topic = data.decode("utf-8").split("|", 1)
        

        print(
            f"{role} connected from "
            f"{client_address} "
            f"Topic: {topic}"
        )

       
        # SUBSCRIBER
        

        if role == "Subscriber":

            with clients_lock:

                if topic not in subscribers:
                    subscribers[topic] = set()

                subscribers[topic].add(client_socket)

            # Keep subscriber connection alive
            while True:

                data = client_socket.recv(1024)

                if not data:
                    break

        # -------------------------
        # PUBLISHER
        # -------------------------

        elif role == "Publisher":

            while True:

                data = client_socket.recv(1024)

                if not data:
                    break

                message = data.decode("utf-8")

                if message == "terminate":

                    print(
                        f"Publisher {client_address} "
                        "terminated."
                    )

                    break

                print(
                    f"Published to [{topic}]: {message}"
                )

                # Send only to subscribers
                # interested in this topic
                broadcast(topic, message)

        else:

            print(
                f"Invalid role from {client_address}"
            )

    except (ConnectionError, OSError):

        print(
            f"Connection lost: {client_address}"
        )

    finally:

        if role == "Subscriber" and topic is not None:
            remove_subscriber(
                client_socket,
                topic
            )

        client_socket.close()

        print(
            f"Disconnected: {client_address}"
        )


# Create server socket
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(
    f"Server listening on port {PORT}"
)


try:

    while True:

        client_socket, client_address = (
            server_socket.accept()
        )

        client_thread = threading.Thread(
            target=handle_client,
            args=(
                client_socket,
                client_address
            ),
            daemon=True
        )

        client_thread.start()


except KeyboardInterrupt:

    print("\nServer shutting down.")


finally:

    server_socket.close()