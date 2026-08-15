# Custom FTP Server using Socket Programming

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Dependencies](https://img.shields.io/badge/Dependencies-None%20\(stdlib%20only\)-blue)

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

---

## ✨ Features

* TCP socket-based client-server communication
* View server directory using `LIST`
* Upload files from client to server
* Download files from server to client
* Binary file transfer using raw socket bytes
* Supports different text and binary file types
* Simple custom command-based protocol
* Local client-server testing using `127.0.0.1`
* Graceful handling of dropped connections, missing files, and partial transfers
* Server keeps running and accepts new clients after one disconnects
* Clean shutdown using `Ctrl+C`

---

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

---

## 📂 Project Structure

```text
SOCKET_PROGRAMMING/
│
├── Server.py
├── Client.py
├── README.md
│
├── server_file/
│   ├── Bengali_AI_Text_Detection_Proposal.pptx
│   ├── debiased_en.csv
│   ├── download.png
│   ├── ICMP-Protocol.pdf
│   ├── Insurance Premium Health card Department Students list.xlsx
│   ├── Mushroom_Task-20260803T091438Z-1-001.zip
│   └── text.txt
│
└── Client_file/
    ├── download.png
    ├── ICMP-Protocol.pdf
    └── upload_test.txt
```

---

## 🛠️ Technologies Used

* **Programming Language:** Python 3.8+
* **Networking:** TCP/IP
* **Socket API:** Python `socket`
* **File Handling:** Python File I/O
* **Protocol:** Custom FTP-like Protocol
* **Data Transfer:** Raw Socket Bytes

---

## 📡 Supported Commands

| Command             | Description                           |
| ------------------- | ------------------------------------- |
| `LIST`              | Display files available on the server |
| `UPLOAD filename`   | Upload a file from client to server   |
| `DOWNLOAD filename` | Download a file from server to client |
| `QUIT`              | Close the client-server connection    |

---

## ▶️ How to Run

### 1. Start the Server

Open a terminal in the project directory and run:

```bash
python Server.py
```

Server output:

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

Client output:

```text
CUSTOM FTP CLIENT
Connected to server.
```

---

## 📁 View Server Files

```text
FTP> LIST
```

Example output:

```text
Server files:

debiased_en.csv
download.png
ICMP-Protocol.pdf
text.txt
Bengali_AI_Text_Detection_Proposal.pptx
```

---

## ⬇️ Download a File

```text
FTP> DOWNLOAD ICMP-Protocol.pdf
```

The downloaded file will be saved inside:

```text
Client_file/
```

Example:

```text
Client_file/
└── ICMP-Protocol.pdf
```

---

## ⬆️ Upload a File

Place the file inside `Client_file/`, then run:

```text
FTP> UPLOAD upload_test.txt
```

The uploaded file will be saved inside:

```text
server_file/
```

Example:

```text
server_file/
└── upload_test.txt
```

---

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

---

## 🔐 Raw Socket File Transfer

Files are opened in binary mode:

```python
with open(file_path, "rb") as file:
    data = file.read(4096)
```

The file bytes are transmitted using:

```python
client_socket.sendall(data)
```

The receiver saves the file in binary mode:

```python
with open(file_path, "wb") as file:
    file.write(data)
```

This allows the system to transfer both text and binary files without depending on file extensions.

---

## 🛡️ Error Handling

The server and client are designed to handle common networking problems gracefully.

* Dropped connections are handled without crashing.
* Missing files return an error message instead of an exception.
* Incomplete uploads are removed automatically.
* Filenames are sanitized using `os.path.basename()`.
* The server continues accepting new clients after one client disconnects.
* The server shuts down cleanly with `Ctrl+C`.

---

## 🧪 Testing

The system was successfully tested with different file types:

* ICMP-Protocol.pdf ✅
* Bengali_AI_Text_Detection_Proposal.pptx ✅
* debiased_en.csv ✅
* XLSX file ✅
* download.png ✅
* text.txt ✅
* ZIP file ✅

Both upload and download operations were successfully tested with different file types.

---

## 🎯 Learning Outcomes

This project demonstrates practical understanding of:

* TCP socket programming
* Client-server architecture
* IP address and port configuration
* TCP byte stream communication
* File transmission over sockets
* Binary file handling
* Custom application-layer protocol design
* Error handling in network applications

---

## 👨‍💻 Author

**Md Miraj Hossan Sajid**

Department of Computer Science & Engineering
Southeast University

---

## 📚 Course

**Advanced Networking**

**Home Task:** Custom File Transfer Protocol (FTP) Server
