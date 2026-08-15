import socket
import os

HOST = "127.0.0.1"
PORT = 5000

CLIENT_FOLDER = "Client_file"

os.makedirs(CLIENT_FOLDER, exist_ok=True)


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
            raise ConnectionError(
                "Connection closed during file transfer."
            )

        data += chunk

    return data


# Create TCP socket
client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Connect to server
client_socket.connect((HOST, PORT))

print("=" * 50)
print("       CUSTOM FTP CLIENT")
print("=" * 50)
print("Connected to server.")
print()

while True:

    command = input("FTP> ").strip()

    if not command:
        continue

    # =========================
    # LIST
    # =========================

    if command.upper() == "LIST":

        client_socket.sendall(b"LIST\n")

        response = receive_line(client_socket)

        if response.startswith("OK"):

            file_size = int(response.split()[1])

            data = receive_exact(
                client_socket,
                file_size
            )

            print("\nServer files:")

            if data:
                print(data.decode())

            print()

        else:
            print("Server:", response)

    # =========================
    # DOWNLOAD
    # =========================

    elif command.upper().startswith("DOWNLOAD"):

        parts = command.split(maxsplit=1)

        if len(parts) < 2:
            print("Usage: DOWNLOAD filename")
            continue

        filename = os.path.basename(parts[1])

        client_socket.sendall(
            f"DOWNLOAD {filename}\n".encode()
        )

        response = receive_line(client_socket)

        if response.startswith("OK"):

            file_size = int(response.split()[1])

            file_path = os.path.join(
                CLIENT_FOLDER,
                filename
            )

            print(f"Downloading: {filename}")
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

                print("Download completed.")
                print(f"Saved to: {file_path}")

            else:

                print("Download incomplete.")

        else:

            print("Server:", response)

    # =========================
    # UPLOAD
    # =========================

    elif command.upper().startswith("UPLOAD"):

        parts = command.split(maxsplit=1)

        if len(parts) < 2:
            print("Usage: UPLOAD filename")
            continue

        filename = os.path.basename(parts[1])

        file_path = os.path.join(
            CLIENT_FOLDER,
            filename
        )

        if not os.path.isfile(file_path):

            print("File not found in Client_file folder.")

            continue

        file_size = os.path.getsize(file_path)

        client_socket.sendall(
            f"UPLOAD {filename} {file_size}\n".encode()
        )

        response = receive_line(client_socket)

        if response == "READY":

            print(f"Uploading: {filename}")
            print(f"File size: {file_size} bytes")

            with open(file_path, "rb") as file:

                while True:

                    data = file.read(4096)

                    if not data:
                        break

                    client_socket.sendall(data)

            result = receive_line(client_socket)

            if result == "UPLOAD_SUCCESS":

                print("Upload completed.")

            else:

                print("Server:", result)

        else:

            print("Server:", response)

    # =========================
    # QUIT
    # =========================

    elif command.upper() == "QUIT":

        client_socket.sendall(b"QUIT\n")

        response = receive_line(client_socket)

        print("Server:", response)

        break

    # =========================
    # INVALID
    # =========================

    else:

        print("Available commands:")
        print("  LIST")
        print("  DOWNLOAD filename")
        print("  UPLOAD filename")
        print("  QUIT")


client_socket.close()

print("Disconnected from server.")