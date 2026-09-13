
import socket
import sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

# Create a TCP socket
server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Bind the socket to an IP address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(1)

print(f"Server is listening on port {PORT}")

# Accept a client connection
client_socket, client_address = server_socket.accept()

print("Connected to:", client_address)

# Receive messages from the client
while True:
    data = client_socket.recv(1024)

    # Client disconnected
    if not data:
        print("Client disconnected.")
        break

    msg = data.decode("utf-8")

    if msg == "terminate":
        print("Termination signal received.")
        break

    print("Client says:", msg)

# Close the connection
client_socket.close()
server_socket.close()

print("Server closed.")
