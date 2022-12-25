import sqlite3
import socket



def get_data():
  # Connect to the SQL database
  conn = sqlite3.connect('massges.db')

  # Query the database to get all the users
  query = "SELECT * FROM messages"
  result = conn.execute(query)

  mass = []

  for row in result:
    room = row[0]
    user = row[1]
    massge = row[2]
    time = row[3]
    mass.append((room, user, massge, time))


  return mass

  query.exit()
  conn.exit()

# Example usage
users = get_data()
print(users)



def main():
    
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = "127.0.0.1"

    port = 24

    # bind to the port
    server_socket.bind((host, port))

    # queue up to 5 requests
    server_socket.listen(5)

    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        #send all data.
        client_socket.send(str(get_data()).encode("utf-8"))

        #close connaction
        client_socket.close()

try:
    main()
except(TypeError):
    print("code ended")