# Python Chat App (Server & Client)

This is a simple chat application written in Python, consisting of two main components:

- **Server** (`server.py`): Handles multiple incoming client connections and broadcasts messages to all connected clients.
- **Client** (`client.py`): Connects to the server and allows the user to send and receive messages in real-time.

This project is licensed under the [MIT License](#license).

---

## How It Works

- The **server** must be started first. It listens for incoming connections on a specified IP address and port.
- Each **client** connects to the server using its IP address and port.
- Once connected, clients can exchange messages through the server, which distributes them to all other clients.

---

## Configuration

In the `client.py` file, you must manually insert the **server's IP address** where indicated in the code.

Look for the line that says:

```python
# Put the server IP here
SERVER_IP = "127.0.0.1"
```

Replace `"127.0.0.1"` with the actual IP address of the machine running the server. For example:

```python
SERVER_IP = "192.168.1.100"
```

Make sure both server and client devices are on the same network.

---

## Requirements

- Python 3.x
- Only standard libraries (no external packages required)

---

## Running the App

1. **Start the server:**

   ```bash
   python server.py
   ```

2. **Start one or more clients (on the same or different devices):**

   ```bash
   python client.py
   ```

   You should now be able to send messages between connected clients.

---
