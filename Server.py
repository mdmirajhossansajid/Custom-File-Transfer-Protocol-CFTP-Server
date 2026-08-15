import socket
import os

HOST = "0.0.0.0"
PORT = 5000

SERVER_FOLDER = "server_file"

os.makedirs(SERVER_FOLDER, exist_ok=True)


def receive_line(sock):
    data = b""

    while b"\n" not in data:
        chunk = sock.recv(1024)

        if not chunk:
            return None

        data += chunk

    line, remaining = data.split(b"\n", 1)
    return line.decode().strip()


def receive_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(min(4096, size - len(data)))

        if not chunk:
            raise ConnectionError("Connection closed during file transfer.")

        data += chunk

    return data


# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))
server_socket.listen(5)

print("=" * 50)
print("       CUSTOM FTP SERVER")
print("=" * 50)
print(f"Server started on port {PORT}")
print("Waiting for client connection...")

client_socket, client_address = server_socket.accept()

print(f"Client connected: {client_address}")


while True:

    command = receive_line(client_socket)

    if command is None:
        break

    print(f"Received command: {command}")

    parts = command.split()

    if not parts:
        continue

    operation = parts[0].upper()

    # =========================
    # LIST
    # =========================

    if operation == "LIST":

        files = os.listdir(SERVER_FOLDER)

        file_list = "\n".join(files)

        response = f"OK {len(file_list.encode())}\n"
        client_socket.sendall(response.encode())
        client_socket.sendall(file_list.encode())

    # =========================
    # DOWNLOAD
    # =========================

    elif operation == "DOWNLOAD":

        if len(parts) < 2:
            client_socket.sendall(b"ERROR Missing filename\n")
            continue

        filename = os.path.basename(parts[1])
        file_path = os.path.join(SERVER_FOLDER, filename)

        if not os.path.isfile(file_path):
            client_socket.sendall(b"ERROR File not found\n")
            continue

        file_size = os.path.getsize(file_path)

        # Send file size first
        client_socket.sendall(
            f"OK {file_size}\n".encode()
        )

        print(f"Sending file: {filename}")
        print(f"File size: {file_size} bytes")

        # Send file bytes
        with open(file_path, "rb") as file:

            while True:

                data = file.read(4096)

                if not data:
                    break

                client_socket.sendall(data)

        print("File sent successfully.")

    # =========================
    # UPLOAD
    # =========================

    elif operation == "UPLOAD":

        if len(parts) < 3:
            client_socket.sendall(b"ERROR Invalid upload command\n")
            continue

        filename = os.path.basename(parts[1])

        try:
            file_size = int(parts[2])
        except ValueError:
            client_socket.sendall(b"ERROR Invalid file size\n")
            continue

        file_path = os.path.join(SERVER_FOLDER, filename)

        client_socket.sendall(b"READY\n")

        print(f"Receiving file: {filename}")
        print(f"File size: {file_size} bytes")

        received = 0

        with open(file_path, "wb") as file:

            while received < file_size:

                data = client_socket.recv(
                    min(4096, file_size - received)
                )

                if not data:
                    break

                file.write(data)
                received += len(data)

        if received == file_size:
            client_socket.sendall(b"UPLOAD_SUCCESS\n")
            print("File uploaded successfully.")
        else:
            client_socket.sendall(b"ERROR Upload incomplete\n")

    # =========================
    # QUIT
    # =========================

    elif operation == "QUIT":

        client_socket.sendall(b"Goodbye\n")

        print("Client disconnected.")

        break

    # =========================
    # INVALID COMMAND
    # =========================

    else:

        client_socket.sendall(b"ERROR Invalid command\n")


client_socket.close()
server_socket.close()

print("Server stopped.")