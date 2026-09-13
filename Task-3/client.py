import socket
import sys
import threading


def receive_messages(client_socket):

    while True:

        try:
            data = client_socket.recv(1024)

            if not data:
                print("Server disconnected.")
                break

            message = data.decode("utf-8")

            print(f"\n[Published message] {message}")

        except (ConnectionError, OSError):

            break


# --------------------------------
# Command-line arguments
# --------------------------------

if len(sys.argv) != 5:

    print(
        "Usage: python3 client.py "
        "<IP_ADDRESS> <PORT> <ROLE> <TOPIC>"
    )

    sys.exit(1)


IP_ADDRESS = sys.argv[1]
PORT = int(sys.argv[2])
ROLE = sys.argv[3]
TOPIC = sys.argv[4]


if ROLE not in ("Publisher", "Subscriber"):

    print(
        "ROLE must be Publisher or Subscriber"
    )

    sys.exit(1)


# --------------------------------
# Create socket
# --------------------------------

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


# --------------------------------
# Connect
# --------------------------------

client_socket.connect(
    (IP_ADDRESS, PORT)
)

print(
    f"Connected to {IP_ADDRESS}:{PORT}"
)

print(f"Role: {ROLE}")
print(f"Topic: {TOPIC}")


# --------------------------------
# Send role
# --------------------------------

client_socket.sendall(
    f"{ROLE}|{TOPIC}".encode("utf-8")
)


# --------------------------------
# Publisher
# --------------------------------

if ROLE == "Publisher":

    try:

        while True:

            message = input(
                "Enter message "
                "(type 'terminate' to quit): "
            )

            client_socket.sendall(
                message.encode("utf-8")
            )

            if message == "terminate":
                break

    except KeyboardInterrupt:

        print("\nPublisher disconnecting...")


# --------------------------------
# Subscriber
# --------------------------------

else:

    receiver_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,),
        daemon=True
    )

    receiver_thread.start()

    print(
        "Waiting for published messages..."
    )

    print(
        "Press Ctrl+C to disconnect."
    )

    try:

        while True:
            input()

    except KeyboardInterrupt:

        print(
            "\nSubscriber disconnecting..."
        )


client_socket.close()