# --- server.py ---
import socket
import threading
import time

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.nicknames = []
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection established with {address}")
            
            # Request nickname
            client_socket.send("NICK".encode('utf-8'))
            nickname = client_socket.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client_socket)
            
            # Broadcast new user joined
            self.broadcast(f"{nickname} has joined the chat!".encode('utf-8'))
            client_socket.send("Connected to the server!".encode('utf-8'))
            
            # Start handling thread for client
            thread = threading.Thread(target=self.handle_client, args=(client_socket, nickname))
            thread.daemon = True
            thread.start()
            
    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message)
            except:
                pass
                
    def handle_client(self, client_socket, nickname):
        while True:
            try:
                message = client_socket.recv(1024)
                if message:
                    print(f"{nickname}: {message.decode('utf-8')}")
                    self.broadcast(f"{nickname}: {message.decode('utf-8')}".encode('utf-8'))
                else:
                    # Empty message usually means client disconnected
                    self.remove_client(client_socket, nickname)
                    break
            except Exception as e:
                print(f"Error handling client {nickname}: {e}")
                self.remove_client(client_socket, nickname)
                break
    
    def remove_client(self, client_socket, nickname):
        if client_socket in self.clients:
            index = self.clients.index(client_socket)
            self.clients.remove(client_socket)
            client_socket.close()
            nickname = self.nicknames[index]
            self.broadcast(f"{nickname} has left the chat!".encode('utf-8'))
            self.nicknames.remove(nickname)
            print(f"{nickname} disconnected")

if __name__ == "__main__":
    server = ChatServer()
    server.start()
