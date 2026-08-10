import socket

HOST = "127.0.0.1"
PORT = 5000

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((HOST, PORT))

print("=" * 50)
print("       CUSTOM FTP CLIENT")
print("=" * 50)
print("Connected to server.")
print()

while True:

    command = input("FTP> ").strip()

    # Send command to server
    client_socket.sendall(command.encode())

    # Receive response
    response = client_socket.recv(1024).decode()

    print("Server:", response)

    if command == "QUIT":
        break

client_socket.close()

print("Disconnected from server.")