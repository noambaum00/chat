import subprocess
import time
import socket

# Define the path to the server code and the command to start the server
SERVER_PATH = r'C:\\Users\\noamb\Documents\\GitHub\\telnet_chan_noam\server'
START_COMMAND = 'python chat_server.py'

# Define the command to update the server code
UPDATE_COMMAND = ['git', '-C', SERVER_PATH, 'pull']

# Define the server address and port
HOST = 'localhost'
PORT = 585

# Create a new socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))
print(f'Server socket bound to {HOST}:{PORT}')

# Start the server process and pass the server socket to it
server_process = subprocess.Popen(
    START_COMMAND.split(),
    cwd=SERVER_PATH,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    env={'SERVER_SOCKET': str(server_socket.fileno())}
)
print(f'Server process started with PID {server_process.pid}')

# Loop to check for user input
while True:
    user_input = input('Enter "update" to update the server, or "quit" to stop it: ')
    if user_input.lower() == 'update':
        # Update the server
        print('Updating server...')
        subprocess.run(UPDATE_COMMAND, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Restart the server
        print('Restarting server...')
        server_process.terminate()
        time.sleep(2)  # Wait for the server process to terminate
        # Start the server process again and pass the new server socket to it
        server_socket.close()  # Close the old server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new server socket
        server_socket.bind((HOST, PORT))  # Bind the new server socket to the address and port
        server_process = subprocess.Popen(
            START_COMMAND.split(),
            cwd=SERVER_PATH,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={'SERVER_SOCKET': str(server_socket.fileno())}  # Pass the new server socket to the server process
        )
        print(f'Server process started with PID {server_process.pid}')
    elif user_input.lower() == 'quit':
        # Stop the server and exit the loop
        print('Stopping server...')
        server_process.terminate()
        server_socket.close()
        break
