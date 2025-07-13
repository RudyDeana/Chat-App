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

## License

This project is open-source and available under the MIT License.

```
MIT License

Copyright (c) 2025 Rudy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                              

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Notes

- This app is meant for learning and testing purposes.
- It does **not** include encryption or authentication.
- For use over the internet or in production, consider adding:
  - TLS/SSL encryption
  - User authentication
  - Message logging and error handling

---