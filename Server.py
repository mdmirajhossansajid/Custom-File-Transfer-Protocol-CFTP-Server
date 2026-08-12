import socket
import os

HOST = "0.0.0.0"
PORT = 5000

SERVER_FOLDER = "server_file"

# Create server folder if it does not exist
os.makedirs(SERVER_FOLDER, exist_ok=True)

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind server to IP and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)

print("=" * 50)
print("       CUSTOM FTP SERVER")
print("=" * 50)
print(f"Server started on port {PORT}")
print("Waiting for client connection...")

# Accept client connection
client_socket, client_address = server_socket.accept()

print(f"Client connected: {client_address}")

while True:

    # Receive command from client
    data = client_socket.recv(1024)

    if not data:
        break

    command = data.decode().strip()

    print(f"Received command: {command}")

    if command == "LIST":

     files = os.listdir(SERVER_FOLDER)

     if files:
        file_list = "\n".join(files)
     else:
        file_list = "Server folder is empty."

     client_socket.sendall(file_list.encode())
    elif command == "QUIT":

     client_socket.sendall(b"Goodbye!")
    print("Client disconnected.")
    break

else:

    client_socket.sendall(b"Invalid command.")
client_socket.close()
server_socket.close()

print("Server stopped.")


