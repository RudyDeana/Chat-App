# server.py
import socket
import threading
import json
import time

class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 5555))
        self.server.listen()
        
        self.rooms = {}  # {room_code: {'clients': [], 'usernames': {}}}
        self.buffer_size = 4096
        print("Server started!")

    def handle_client(self, client):
        try:
            # Ricevi dati connessione
            data = client.recv(1024).decode()
            join_data = json.loads(data)
            username = join_data['username']
            room_code = join_data['room']
            is_host = join_data['is_host']
            
            # Gestisci creazione/join stanza
            if is_host:
                if room_code in self.rooms:
                    client.send(json.dumps({'type': 'error', 'content': 'Stanza già esistente!'}).encode())
                    return
                self.rooms[room_code] = {'clients': [], 'usernames': {}}
            elif room_code not in self.rooms:
                client.send(json.dumps({'type': 'error', 'content': 'Stanza non trovata!'}).encode())
                return

            # Aggiungi client alla stanza
            self.rooms[room_code]['clients'].append(client)
            self.rooms[room_code]['usernames'][client] = username
            
            # Invia conferma
            client.send(json.dumps({'type': 'success', 'content': 'Connesso!'}).encode())
            
            # Invia aggiornamenti
            time.sleep(0.5)  # Piccolo delay per assicurare l'ordine dei messaggi
            self.broadcast_users(room_code)
            self.broadcast_message(room_code, f"{username} è entrato nella chat", "Sistema")
            
            # Loop messaggi
            while True:
                try:
                    data = client.recv(self.buffer_size).decode()
                    if not data:
                        raise Exception("Connessione chiusa")
                    
                    message = json.loads(data)
                    
                    if message['type'] == 'message':
                        self.broadcast_message(room_code, message['content'], username)
                    
                    elif message['type'] == 'file_info':
                        # Gestione invio file
                        file_name = message['file_name']
                        file_size = message['file_size']
                        
                        # Notifica altri utenti
                        self.broadcast_message(room_code, f"sta inviando il file: {file_name}", username)
                        
                        # Ricevi il file in chunks
                        received_data = bytearray()
                        while len(received_data) < file_size:
                            remaining = file_size - len(received_data)
                            chunk_size = min(self.buffer_size, remaining)
                            chunk = client.recv(chunk_size)
                            if not chunk:
                                raise Exception("Connessione interrotta durante il trasferimento")
                            received_data.extend(chunk)
                        
                        # Invia il file agli altri client
                        file_info = json.dumps({
                            'type': 'file',
                            'sender': username,
                            'file_name': file_name,
                            'file_size': file_size
                        }).encode()
                        
                        for c in self.rooms[room_code]['clients']:
                            if c != client:
                                try:
                                    c.send(file_info)
                                    time.sleep(0.1)  # Piccolo delay per sincronizzazione
                                    c.sendall(received_data)
                                except:
                                    print(f"Errore nell'invio del file a un client")
                        
                        self.broadcast_message(room_code, f"ha inviato il file: {file_name}", username)
                        
                except Exception as e:
                    print(f"Errore nella gestione del client: {str(e)}")
                    raise

        except Exception as e:
            print(f"Client disconnesso: {str(e)}")
        finally:
            if room_code in self.rooms and client in self.rooms[room_code]['clients']:
                username = self.rooms[room_code]['usernames'].pop(client, None)
                self.rooms[room_code]['clients'].remove(client)
                if username:
                    self.broadcast_message(room_code, f"{username} è uscito dalla chat", "Sistema")
                self.broadcast_users(room_code)
                if not self.rooms[room_code]['clients']:
                    del self.rooms[room_code]
            client.close()

    def broadcast_message(self, room_code, content, sender):
        message = json.dumps({
            'type': 'message',
            'sender': sender,
            'content': content
        }).encode()
        
        for client in self.rooms[room_code]['clients']:
            try:
                client.send(message)
            except:
                pass

    def broadcast_users(self, room_code):
        users = list(self.rooms[room_code]['usernames'].values())
        message = json.dumps({
            'type': 'users',
            'users': users
        }).encode()
        
        for client in self.rooms[room_code]['clients']:
            try:
                client.send(message)
            except:
                pass

    def start(self):
        while True:
            client, _ = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.daemon = True
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
