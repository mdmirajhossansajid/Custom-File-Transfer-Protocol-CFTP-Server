# Custom FTP Server using Socket Programming

A custom File Transfer Protocol (FTP) server and client developed using **Python TCP Socket Programming**. The system allows clients to view server directories, upload files to the server, and download files from the server using **raw socket bytes**.

## 📌 Project Overview

This project implements a simple FTP-like file transfer system without using any built-in FTP library.

The communication is established using **TCP sockets**, and files are transferred as raw bytes. The system supports both text and binary files such as:

* PDF
* PPTX
* XLSX
* CSV
* PNG
* JPG
* TXT
* ZIP
* Other file types

## ✨ Features

* TCP socket-based client-server communication
* View server directory using `LIST`
* Upload files from client to server
* Download files from server to client
* Binary file transfer using raw socket bytes
* Supports large and different file types
* Simple custom command-based protocol
* Local client-server testing using `127.0.0.1`

## 🏗️ System Architecture

```text
                  TCP Connection
        ┌─────────────────────────────┐
        │                             │
        ▼                             ▼
 ┌──────────────┐              ┌──────────────┐
 │    Client    │◄────────────►│    Server    │
 │              │    Socket    │              │
 └──────────────┘              └──────────────┘
        │                             │
        ▼                             ▼
  Client_file/                 server_file/
```

## 📂 Project Structure

```text
SOCKET_PROGRAMMING/
│
├── Server.py
├── Client.py
│
├── server_file/
│   ├── PDF files
│   ├── PPTX files
│   ├── CSV files
│   ├── XLSX files
│   ├── PNG files
│   └── TXT files
│
└── Client_file/
    └── Client-side files
```

## 🛠️ Technologies Used

* **Programming Language:** Python
* **Networking:** TCP
* **Socket API:** Python `socket`
* **File Handling:** Python file I/O
* **Protocol:** Custom FTP-like protocol
* **Data Transfer:** Raw socket bytes

## 📡 Supported Commands

| Command             | Description                            |
| ------------------- | -------------------------------------- |
| `LIST`              | Displays files available on the server |
| `UPLOAD filename`   | Uploads a file from client to server   |
| `DOWNLOAD filename` | Downloads a file from server to client |
| `QUIT`              | Closes the client-server connection    |

## ▶️ How to Run

### 1. Start the Server

Open a terminal in the project directory and run:

```bash
python Server.py
```

The server will display:

```text
CUSTOM FTP SERVER
Server started on port 5000
Waiting for client connection...
```

### 2. Start the Client

Open another terminal in the same project directory and run:

```bash
python Client.py
```

The client will connect to the server:

```text
CUSTOM FTP CLIENT
Connected to server.
```

## 📁 View Server Files

Use:

```text
FTP> LIST
```

Example:

```text
Server files:

debiased_en.csv
download.png
ICMP-Protocol.pdf
text.txt
Bengali_AI_Text_Detection_Proposal.pptx
```

## ⬇️ Download a File

To download a file from the server:

```text
FTP> DOWNLOAD ICMP-Protocol.pdf
```

The file will be saved inside:

```text
Client_file/
```

Example:

```text
Client_file/
└── ICMP-Protocol.pdf
```

The same mechanism can download PDF, PPTX, CSV, XLSX, PNG, TXT, ZIP and other file types.

## ⬆️ Upload a File

First place the file inside:

```text
Client_file/
```

Then use:

```text
FTP> UPLOAD upload_test.txt
```

The file will be transferred to:

```text
server_file/
```

Example:

```text
server_file/
└── upload_test.txt
```

## 🔄 File Transfer Process

### Download

```text
Client                         Server
  │                              │
  │── DOWNLOAD filename ────────►│
  │                              │
  │◄──── File Size ──────────────│
  │                              │
  │◄──── Raw File Bytes ─────────│
  │                              │
  │── File Saved ────────────────│
```

### Upload

```text
Client                         Server
  │                              │
  │── UPLOAD filename size ─────►│
  │                              │
  │◄──── READY ──────────────────│
  │                              │
  │──── Raw File Bytes ─────────►│
  │                              │
  │◄──── UPLOAD_SUCCESS ─────────│
```

## 🔐 Raw Socket File Transfer

Files are opened in binary mode:

```python
with open(file_path, "rb") as file:
    data = file.read(4096)
```

The file bytes are transmitted through the TCP socket using:

```python
client_socket.sendall(data)
```

On the receiving side, the file is saved using binary write mode:

```python
with open(file_path, "wb") as file:
    file.write(data)
```

Therefore, the system can transfer both text and binary files without depending on their file extension.

## 🧪 Testing

The system was tested with multiple file types:

* `ICMP-Protocol.pdf` ✅
* `Bengali_AI_Text_Detection_Proposal.pptx` ✅
* `debiased_en.csv` ✅
* `.xlsx` file ✅
* `download.png` ✅
* `text.txt` ✅
* `.zip` file ✅

Both upload and download operations were successfully tested.

## 🎯 Learning Outcomes

Through this project, the following networking concepts were practiced:

* TCP client-server communication
* Socket programming
* IP address and port configuration
* TCP byte stream communication
* File transmission over sockets
* Binary file handling
* Custom application-layer protocol design
* Client-server architecture

## 👨‍💻 Author

**Md Miraj Hossan Sajid**

Department of Computer Science & Engineering
Southeast University

## 📚 Course

**Advanced Networking**


