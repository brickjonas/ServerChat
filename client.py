import socket
import threading  # Import the threading module

# Constants for network communication
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())  # Get the server's IP address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED!"

# Create a socket object for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the client to the server
client.connect(ADDR)

# Function to send a message to the server
def send(msg):
    # Include username in the message
    message = f"{username}: {msg}"
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

# Get username from the user
username = input("Enter your username: ")
# Send the username to the server only once during connection establishment
client.send(username.encode(FORMAT))

# Function to receive messages from the server
def receive_messages():
    while True:
        message = client.recv(1024).decode(FORMAT)
        print(message)

# Start receiving messages in a separate thread
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Continuously send messages to the server
while True:
    message = input("Type your message: ")
    send(message)
    print()  # Print a newline after sending the message
