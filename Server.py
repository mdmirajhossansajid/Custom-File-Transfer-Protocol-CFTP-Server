import socket
import os

HOST = "0.0.0.0"
PORT = 5000

SERVER_FOLDER = "server_file"

os.makedirs(SERVER_FOLDER, exist_ok=True)


class SocketReader:
    """Buffered reader for TCP socket data."""

    def __init__(self, sock):
        self.sock = sock
        self.buffer = b""

    def receive_line(self):
        """Receive data until a newline is found."""
        while b"\n" not in self.buffer:
            chunk = self.sock.recv(1024)

            if not chunk:
                return None

            self.buffer += chunk

        line, self.buffer = self.buffer.split(b"\n", 1)

        return line.decode().strip()

    def receive_exact(self, size):
        """Receive exactly 'size' bytes from the socket."""
        while len(self.buffer) < size:
            chunk = self.sock.recv(
                min(4096, size - len(self.buffer))
            )

            if not chunk:
                raise ConnectionError(
                    "Connection closed during file transfer."
                )

            self.buffer += chunk

        data = self.buffer[:size]
        self.buffer = self.buffer[size:]

        return data


def send_line(sock, message):
    """Send a text message followed by a newline."""
    sock.sendall(f"{message}\n".encode())


def handle_client(client_socket, client_address):
    """Handle one connected client."""

    print(f"Client connected: {client_address}")

    reader = SocketReader(client_socket)

    try:

        while True:

            command = reader.receive_line()

            if command is None:
                print("Client disconnected unexpectedly.")
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

                files = [
                    f
                    for f in os.listdir(SERVER_FOLDER)
                    if os.path.isfile(
                        os.path.join(SERVER_FOLDER, f)
                    )
                ]

                file_list = "\n".join(files)

                file_data = file_list.encode()

                send_line(
                    client_socket,
                    f"OK {len(file_data)}"
                )

                client_socket.sendall(file_data)

                print("Directory listing sent.")

            # =========================
            # DOWNLOAD
            # =========================

            elif operation == "DOWNLOAD":

                if len(parts) < 2:
                    send_line(
                        client_socket,
                        "ERROR Missing filename"
                    )
                    continue

                # Prevent path traversal
                filename = os.path.basename(parts[1])

                file_path = os.path.join(
                    SERVER_FOLDER,
                    filename
                )

                if not os.path.isfile(file_path):

                    send_line(
                        client_socket,
                        "ERROR File not found"
                    )

                    continue

                try:

                    file_size = os.path.getsize(file_path)

                    # Send file size first
                    send_line(
                        client_socket,
                        f"OK {file_size}"
                    )

                    print(f"Sending file: {filename}")
                    print(f"File size: {file_size} bytes")

                    # Send file as raw bytes
                    with open(file_path, "rb") as file:

                        while True:

                            data = file.read(4096)

                            if not data:
                                break

                            client_socket.sendall(data)

                    print("File sent successfully.")

                except OSError as e:

                    print(
                        f"Error reading file '{filename}': {e}"
                    )

            # =========================
            # UPLOAD
            # =========================

            elif operation == "UPLOAD":

                if len(parts) < 3:

                    send_line(
                        client_socket,
                        "ERROR Invalid upload command"
                    )

                    continue

                # Prevent path traversal
                filename = os.path.basename(parts[1])

                try:

                    file_size = int(parts[2])

                except ValueError:

                    send_line(
                        client_socket,
                        "ERROR Invalid file size"
                    )

                    continue

                if file_size < 0:

                    send_line(
                        client_socket,
                        "ERROR Invalid file size"
                    )

                    continue

                file_path = os.path.join(
                    SERVER_FOLDER,
                    filename
                )

                try:

                    # Tell client to start sending
                    send_line(
                        client_socket,
                        "READY"
                    )

                    print(f"Receiving file: {filename}")
                    print(f"File size: {file_size} bytes")

                    received = 0

                    with open(file_path, "wb") as file:

                        while received < file_size:

                            remaining = file_size - received

                            data = client_socket.recv(
                                min(4096, remaining)
                            )

                            if not data:
                                break

                            file.write(data)

                            received += len(data)

                    if received == file_size:

                        send_line(
                            client_socket,
                            "UPLOAD_SUCCESS"
                        )

                        print(
                            "File uploaded successfully."
                        )

                    else:

                        send_line(
                            client_socket,
                            "ERROR Upload incomplete"
                        )

                        if os.path.exists(file_path):
                            os.remove(file_path)

                except OSError as e:

                    print(
                        f"Error writing file "
                        f"'{filename}': {e}"
                    )

                    if os.path.exists(file_path):
                        os.remove(file_path)

            # =========================
            # QUIT
            # =========================

            elif operation == "QUIT":

                send_line(
                    client_socket,
                    "Goodbye"
                )

                print("Client disconnected.")

                break

            # =========================
            # INVALID COMMAND
            # =========================

            else:

                send_line(
                    client_socket,
                    "ERROR Invalid command"
                )

    except (
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError
    ):

        print("Client connection was reset or lost.")

    except ConnectionError as e:

        print(f"Connection error: {e}")

    finally:

        client_socket.close()


def main():

    # Create TCP socket
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Allow quick restart after server shutdown
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server_socket.bind(
        (HOST, PORT)
    )

    server_socket.listen(5)

    print("=" * 50)
    print("       CUSTOM FTP SERVER")
    print("=" * 50)
    print(f"Server started on port {PORT}")
    print("Waiting for client connection...")

    try:

        while True:

            client_socket, client_address = (
                server_socket.accept()
            )

            handle_client(
                client_socket,
                client_address
            )

            print("Waiting for client connection...")

    except KeyboardInterrupt:

        print(
            "\nShutting down server "
            "(Ctrl+C received)..."
        )

    finally:

        server_socket.close()

        print("Server stopped.")


if __name__ == "__main__":
    main()