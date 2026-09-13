
import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python client.py <IP_ADDRESS> <PORT>")
    sys.exit(1)

IP_ADDRESS = sys.argv[1]
PORT = int(sys.argv[2])

# Create a TCP socket
client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

try:
    # Connect to the server
    client_socket.connect((IP_ADDRESS, PORT))

    print(f"Connected to server at {IP_ADDRESS}:{PORT}")

    while True:
        message = input(
            "Enter a message (type 'terminate' to quit): "
        )

        client_socket.sendall(
            message.encode("utf-8")
        )

        if message == "terminate":
            break

finally:
    client_socket.close()
    print("Client closed.")
