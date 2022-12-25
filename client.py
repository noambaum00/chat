import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Define the host and port to connect to
host = "www.example.com"
port = 23


print("""
Always wanted your data security to be thrown out the window?
Always looking for the most unreliablest chat?
So that's exactly why we founded "@@@"
With technology from the 70's.
Zero data security.
And the sql server is open to all.

sooo... what your name is?
""")
name = input()

# Connect to the server
s.connect((host, port))

# Send a username to the server
message = name
s.sendall(message.encode())

# Receive a response from the server
response = s.recv(1024).decode()

# Print the response
print(response)

# Close the connection
s.close()

import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port to connect to
host = "www.example.com"
port = 23

# Connect to the host
s.connect((host, port))

# Enter an infinite loop
while True:
    # Receive data from the server
    received = s.recv(1024)

    # Print the received data
    print(received.decode())

    # Wait for user input
    data = input()

    # Send the user input to the server
    s.sendall(data.encode())


# Close the socket
s.close()