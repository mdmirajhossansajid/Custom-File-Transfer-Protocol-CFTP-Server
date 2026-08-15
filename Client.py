import socket
import os

HOST = "127.0.0.1"
PORT = 5000

CLIENT_FOLDER = "Client_file"

os.makedirs(CLIENT_FOLDER, exist_ok=True)


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
    sock.sendall(
        f"{message}\n".encode()
    )


def main():

    # =========================
    # CREATE SOCKET
    # =========================

    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # =========================
    # CONNECT TO SERVER
    # =========================

    try:

        client_socket.connect(
            (HOST, PORT)
        )

    except (
        ConnectionRefusedError,
        OSError
    ) as e:

        print(
            f"Could not connect to server "
            f"at {HOST}:{PORT} ({e})"
        )

        print(
            "Make sure Server.py is running first."
        )

        return

    print("=" * 50)
    print("       CUSTOM FTP CLIENT")
    print("=" * 50)
    print("Connected to server.")
    print()

    reader = SocketReader(client_socket)

    try:

        while True:

            try:

                command = input(
                    "FTP> "
                ).strip()

            except (
                KeyboardInterrupt,
                EOFError
            ):

                print("\nExiting...")

                break

            if not command:
                continue

            # =========================
            # LIST
            # =========================

            if command.upper() == "LIST":

                send_line(
                    client_socket,
                    "LIST"
                )

                response = reader.receive_line()

                if response is None:

                    print(
                        "Server closed the connection."
                    )

                    break

                if response.startswith("OK"):

                    try:

                        file_size = int(
                            response.split()[1]
                        )

                    except (
                        IndexError,
                        ValueError
                    ):

                        print(
                            "Invalid server response."
                        )

                        continue

                    data = reader.receive_exact(
                        file_size
                    )

                    print("\nServer files:")

                    if data:

                        print(
                            data.decode(
                                errors="replace"
                            )
                        )

                    else:

                        print(
                            "Server folder is empty."
                        )

                    print()

                else:

                    print(
                        "Server:",
                        response
                    )

            # =========================
            # DOWNLOAD
            # =========================

            elif command.upper().startswith(
                "DOWNLOAD"
            ):

                parts = command.split(
                    maxsplit=1
                )

                if len(parts) < 2:

                    print(
                        "Usage: DOWNLOAD filename"
                    )

                    continue

                filename = os.path.basename(
                    parts[1]
                )

                send_line(
                    client_socket,
                    f"DOWNLOAD {filename}"
                )

                response = reader.receive_line()

                if response is None:

                    print(
                        "Server closed the connection."
                    )

                    break

                if response.startswith("OK"):

                    try:

                        file_size = int(
                            response.split()[1]
                        )

                    except (
                        IndexError,
                        ValueError
                    ):

                        print(
                            "Invalid file size received."
                        )

                        continue

                    file_path = os.path.join(
                        CLIENT_FOLDER,
                        filename
                    )

                    print(
                        f"Downloading: {filename}"
                    )

                    print(
                        f"File size: "
                        f"{file_size} bytes"
                    )

                    received = 0

                    try:

                        with open(
                            file_path,
                            "wb"
                        ) as file:

                            while received < file_size:

                                remaining = (
                                    file_size
                                    - received
                                )

                                data = (
                                    reader.sock.recv(
                                        min(
                                            4096,
                                            remaining
                                        )
                                    )
                                )

                                if not data:

                                    break

                                file.write(data)

                                received += len(data)

                        if received == file_size:

                            print(
                                "Download completed."
                            )

                            print(
                                f"Saved to: "
                                f"{file_path}"
                            )

                        else:

                            print(
                                "Download incomplete."
                            )

                            if os.path.exists(
                                file_path
                            ):

                                os.remove(
                                    file_path
                                )

                    except OSError as e:

                        print(
                            f"Error saving file: {e}"
                        )

                else:

                    print(
                        "Server:",
                        response
                    )

            # =========================
            # UPLOAD
            # =========================

            elif command.upper().startswith(
                "UPLOAD"
            ):

                parts = command.split(
                    maxsplit=1
                )

                if len(parts) < 2:

                    print(
                        "Usage: UPLOAD filename"
                    )

                    continue

                filename = os.path.basename(
                    parts[1]
                )

                file_path = os.path.join(
                    CLIENT_FOLDER,
                    filename
                )

                if not os.path.isfile(
                    file_path
                ):

                    print(
                        "File not found in "
                        "Client_file folder."
                    )

                    continue

                try:

                    file_size = os.path.getsize(
                        file_path
                    )

                except OSError as e:

                    print(
                        f"Error accessing file: {e}"
                    )

                    continue

                send_line(
                    client_socket,
                    f"UPLOAD "
                    f"{filename} "
                    f"{file_size}"
                )

                response = reader.receive_line()

                if response is None:

                    print(
                        "Server closed the connection."
                    )

                    break

                if response == "READY":

                    print(
                        f"Uploading: {filename}"
                    )

                    print(
                        f"File size: "
                        f"{file_size} bytes"
                    )

                    try:

                        with open(
                            file_path,
                            "rb"
                        ) as file:

                            while True:

                                data = file.read(
                                    4096
                                )

                                if not data:

                                    break

                                client_socket.sendall(
                                    data
                                )

                        result = (
                            reader.receive_line()
                        )

                        if result == "UPLOAD_SUCCESS":

                            print(
                                "Upload completed."
                            )

                        else:

                            print(
                                "Server:",
                                result
                            )

                    except OSError as e:

                        print(
                            f"Error reading file: {e}"
                        )

                else:

                    print(
                        "Server:",
                        response
                    )

            # =========================
            # QUIT
            # =========================

            elif command.upper() == "QUIT":

                send_line(
                    client_socket,
                    "QUIT"
                )

                response = (
                    reader.receive_line()
                )

                if response:

                    print(
                        "Server:",
                        response
                    )

                break

            # =========================
            # INVALID COMMAND
            # =========================

            else:

                print(
                    "Available commands:"
                )

                print(
                    "  LIST"
                )

                print(
                    "  DOWNLOAD filename"
                )

                print(
                    "  UPLOAD filename"
                )

                print(
                    "  QUIT"
                )

    except (
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError
    ):

        print(
            "\nConnection to server was lost."
        )

    except ConnectionError as e:

        print(
            f"\nConnection error: {e}"
        )

    finally:

        client_socket.close()

        print(
            "Disconnected from server."
        )


if __name__ == "__main__":
    main()