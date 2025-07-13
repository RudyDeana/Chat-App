import socket
import threading
import json

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):
        self.host = host
        self.port = port
        self.rooms = {}

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client, address = self.server.accept()
            print(f"New connection from {address}")
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client):
        room_code = None  # Initialize to avoid UnboundLocalError
        try:
            while True:
                data = client.recv(1024).decode()
                if not data:
                    break

                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    print("Invalid JSON received from client")
                    break  # or continue if you prefer to keep the client alive

                if 'action' in message:
                    action = message['action']

                    if action == 'create_room':
                        room_code = message['room_code']
                        self.rooms[room_code] = {'clients': [client]}
                        print(f"Room {room_code} created")
                        client.send(json.dumps({'status': 'room_created'}).encode())

                    elif action == 'join_room':
                        room_code = message['room_code']
                        if room_code in self.rooms:
                            self.rooms[room_code]['clients'].append(client)
                            print(f"Client joined room {room_code}")
                            client.send(json.dumps({'status': 'room_joined'}).encode())
                        else:
                            client.send(json.dumps({'status': 'room_not_found'}).encode())

                    elif action == 'send_message':
                        room_code = message['room_code']
                        msg = message['message']
                        if room_code in self.rooms:
                            for c in self.rooms[room_code]['clients']:
                                if c != client:
                                    try:
                                        c.send(json.dumps({'message': msg}).encode())
                                    except:
                                        pass

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:
            print("Client disconnected: Connection closed")
            if room_code and room_code in self.rooms and client in self.rooms[room_code]['clients']:
                self.rooms[room_code]['clients'].remove(client)
                if not self.rooms[room_code]['clients']:
                    del self.rooms[room_code]
            client.close()


if __name__ == '__main__':
    server = ChatServer()
    server.start()
