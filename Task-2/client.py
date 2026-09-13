
import socket
import sys
import threading


if len(sys.argv) != 4:
    print(
        "Usage: python3 client.py "
        "<IP_ADDRESS> <PORT> <Publisher|Subscriber>"
    )
    sys.exit(1)


IP_ADDRESS = sys.argv[1]
PORT = int(sys.argv[2])
ROLE = sys.argv[3]

if ROLE not in ("Publisher", "Subscriber"):
    print("Role must be Publisher or Subscriber.")
    sys.exit(1)


client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)


def receive_messages():
    """Receive and display messages from the server."""

    try:
        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            msg = data.decode("utf-8")
            print(f"Received: {msg}")

            
    except (ConnectionError, OSError):
        pass


try:
    client_socket.connect((IP_ADDRESS, PORT))

    print(f"Connected to {IP_ADDRESS}:{PORT}")
    print(f"Role: {ROLE}")

    # Register the role
    client_socket.sendall(
        (ROLE + "\n").encode("utf-8")
    )

    if ROLE == "Publisher":
        # Publisher sends messages
        while True:
            message = input("Publish: ")

            client_socket.sendall(
                (message + "\n").encode("utf-8")
            )

            if message == "terminate":
                break

    else:
        # Subscriber receives messages in a separate thread
        receiver_thread = threading.Thread(
            target=receive_messages,
            daemon=True
        )

        receiver_thread.start()

        print("Waiting for published messages...")
        print("Press Ctrl+C to disconnect.")

        try:
            while True:
                # Keep the subscriber alive
                input()

        except KeyboardInterrupt:
            print("\nDisconnecting subscriber...")

finally:
    client_socket.close()
    print("Client closed.")
