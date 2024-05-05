import socket
import threading

# Constants for network communication
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Get the server's IP address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED!"

# Create a socket object for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the server address and port
server.bind(ADDR)

# List to store connected clients and their usernames
clients = []

# Function to handle each client connection
def handle_client(conn, addr):
    # Receive the username from the client
    username = conn.recv(HEADER).decode(FORMAT)
    print(f"NEW CONNECTION: {username} connected.")
    
    # Add the new client to the list of clients
    clients.append((conn, username))
    
    # Broadcast the new connection to all clients
    broadcast(f"NEW CONNECTION: {username} connected.\n")

    connected = True
    while connected:
        # Receive message length
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # Receive message
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
                break

            # Split message into username and message content
            username, message = msg.split(": ", 1)
            print(f"[{username}]: {message}")
            # Broadcast the message to all clients
            broadcast(msg)

    # Close the connection when client disconnects
    conn.close()

# Function to broadcast a message to all clients
def broadcast(msg):
    for client, _ in clients:
        client.send((msg + "\n").encode(FORMAT))  # Append a newline character

# Function to start the server and handle incoming connections
def start():
    print(f"Server is listening on {SERVER}")
    server.listen()
    while True:
        # Accept incoming connection
        conn, addr = server.accept()
        # Start a new thread to handle the connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")

# Print a message indicating that the server is starting
print("SERVER STARTING......")
# Start the server
start()
