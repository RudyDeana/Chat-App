import socket
import threading
import json

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            try:
                message = json.loads(data)
                if 'message' in message:
                    print("Message received:", message['message'])
            except json.JSONDecodeError:
                print("Invalid JSON received")
        except:
            break

def main():
    host = input("Enter server IP (default 127.0.0.1): ") or "127.0.0.1"
    port = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print("Connected to server.")
    except:
        print("Unable to connect to the server.")
        return

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        print("\nOptions:")
        print("1. Create room")
        print("2. Join room")
        print("3. Send message")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            room_code = input("Enter new room code: ")
            message = {
                "action": "create_room",
                "room_code": room_code
            }
            client.send(json.dumps(message).encode())

        elif choice == "2":
            room_code = input("Enter room code to join: ")
            message = {
                "action": "join_room",
                "room_code": room_code
            }
            client.send(json.dumps(message).encode())

        elif choice == "3":
            room_code = input("Enter room code: ")
            msg = input("Enter message: ")
            message = {
                "action": "send_message",
                "room_code": room_code,
                "message": msg
            }
            client.send(json.dumps(message).encode())

        elif choice == "4":
            print("Disconnected from server.")
            client.close()
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
