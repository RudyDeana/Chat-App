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

