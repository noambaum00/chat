import socket
import sqlite3
#import mongoDB
import os
from _thread import *


HELP_MASSAGE = """
the list comend is:
\tlsr: = list room
\tjnr: = join room
\tlvr: = leave room
\tlsur:= list users in room
\tmsg: = send message
\texit
\thelp
\tchange_password
"""
ADMIN_COMMENDS= """
\tcrr: = crieit room
\tdlr: = delete room
\tdlu: = delete user
\tlsr: = list room
\tlsur:= list users in room
\tkcu: = kick user
\text: = exit
"""

def main():
    #connect db
    #conn = mongoDB.init("mongodb+srv://noambaum:152433qwe@cluster0.siz7qr0.mongodb.net/?retryWrites=true&w=majority")

    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = "127.0.0.1"

    port = 23

    print("STSRT")

    # bind to the port
    server_socket.bind((host, port))

    print("NIND")

    # queue up to 5 requests
    server_socket.listen(50)

    print("LISENING")

    #threading staf
    ThreadCount = 0


    # create a list of rooms
    global rooms
    rooms = []

    # create a dictionary of connected clients, with the key being the client's
    # socket and the value being the client's username
    global clients
    clients = {}


    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(multi_threaded_client, (client_socket, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()


def multi_threaded_client(client_socket):

        # send a thank you message to the client
        client_socket.send(("Thank you for connecting").encode())

        client_socket.send(("Always wanted your data security to be thrown out the window?\n").encode())
        client_socket.send(("Always looking for the most unreliable chat?\n").encode())
        client_socket.send(("So that's exactly why we founded '@@@'\n").encode())
        client_socket.send(("With technology from the 70's.\n").encode())
        client_socket.send(("Zero data security.\n").encode())
        client_socket.send(("And the sql server is open to all.\n").encode())
        
        # get the client's username and password
        client_socket.send(("sooo... what your name is? ").encode())

        username = get(client_socket)
        client_socket.send(("and what your passward?").encode())
        password = get(client_socket)

        # check if the user is an admin
        if username == "root": #mongoDB.admin_sign_in(conn, username, password):
            # if the user is an admin, add the user to the list of connected
            # clients and set the user's status to "admin"
            clients[client_socket] = username
            
            client_socket.send(("admin \n").encode())

            # receive the admin's commands and act on them
            while True:
                # receive the admin's command
                command = get(client_socket)
                commmmmmmend = command[:4]
                
                if command[0:4] == "crr:":
                    room_name = command [4:]
                    room = {"name": room_name, "clients": []}
                    rooms.append(room)

                    # send a confirmation message to the admin
                    client_socket.send(("Room created").encode())

                elif command[:4] == "dlr:":
                    # receive the name of the room to delete
                    room_name = get(client_socket)

                    # delete the room from the list of rooms
                    for room in rooms:
                        if room["name"] == room_name:
                            rooms.remove(room)

                    # send a confirmation message to the admin
                    client_socket.send((b"Room deleted").encode())

                elif command[:4] == "lsr:":
                    # send the list of rooms to the admin
                    client_socket.send(str(rooms).encode())

                elif command[:4] == "lsu:":
                    # send the list of connected users to the admin
                    client_socket.send(str(clients).encode())
                
                elif command[:4] == "jnr:":
                    # receive the name of the room to join
                    room_name = command[4:]

                    # join the room
                    for room in rooms:
                        if room["name"] == room_name:
                            room["clients"].append(username)

                    # send a confirmation message to the user
                    client_socket.send(("Room joined").encode())

                elif command[:4] == "lvr:":
                    # receive the name of the room to leave
                    room_name = command[4:]

                    # leave the room
                    for room in rooms:
                        if room["name"] == room_name:
                            room["clients"].remove(username)

                    # send a confirmation message to the user
                    client_socket.send(("Room left").encode())

                elif command[:5] == "lsur:":
                    # receive the name of the room to list the users in
                    room_name = get(client_socket)

                    # send the list of users in the room to the admin
                    for room in rooms:
                        if room["name"] == room_name:
                            client_socket.send(str(room["clients"]).encode())

                elif command[:4] == "kcu:":
                    # receive the username of the user to kick
                    usernameToKick = command[4:]

                    # kick the user
                    for client in clients:
                        if clients[client] == usernameToKick:
                            client.close()
                            del clients[client]
                    # send a confirmation message to the admin
                    client_socket.send('User : {usernameToKick} kicked')

                elif command[:4] == "dlu:":
                    # receive the username of the user to kick
                    usernameToKick = command[4:]

                    #delete username frome database
                    #mongoDB.delete_user(conn, usernameToKick)
                    client_socket.send('User : {usernameToKick} deleted')

                elif command[:4] == "msg:":
                    
                    message = command[4:]

                    # send the message to the room
                    for room in rooms:
                        if room["name"] == room_name:
                            for client in room["clients"]:
                                for client_socket in clients:
                                    if clients[client_socket] == client:
                                        client_socket.send(("admin>> " + message + "\n").encode())

                    # send a confirmation message to the user
                    client_socket.send(("Message sent").encode())


                    #mongoDB.sendMassge(conn, room, username, message)





                elif command[:4] == "ext:":
                    # close the admin's connection
                    client_socket.close()
                    break

                #add massge sender.

        #elif mongoDB.client_sign_in(conn, username, password):
        else:   #if username == "user":
            # if the user is not an admin, add the user to the list of connected
            # clients and set the user's status to "user"
            clients[client_socket] = username
            client_socket.send(("user").encode())

            # receive the user's commands and act on them
            while True:
                # receive the user's command
                command = get(client_socket)

                if command[:4] == "lsr:":
                    # send the list of rooms to the user
                    client_socket.send(str(rooms).encode())

                elif command[:4] == "jnr:":
                    # receive the name of the room to join
                    room_name = command[4:]

                    # join the room
                    for room in rooms:
                        if room["name"] == room_name:
                            room["clients"].append(username)

                    # send a confirmation message to the user
                    client_socket.send(("Room joined").encode())

                elif command[:4] == "lvr:":
                    # receive the name of the room to leave
                    room_name = command[4:]

                    # leave the room
                    for room in rooms:
                        if room["name"] == room_name:
                            room["clients"].remove(username)

                    # send a confirmation message to the user
                    client_socket.send(("Room left").encode())

                elif command[:5] == "lsur:":
                    # receive the name of the room to list the users in
                    room_name = get(client_socket)

                    # send the list of users in the room to the user
                    for room in rooms:
                        if room["name"] == room_name:
                            client_socket.send(str(room["clients"]).encode())

                elif command[:4] == "msg:":
                    
                    message = command[4:]

                    # send the message to the room
                    for room in rooms:
                        if room["name"] == room_name:
                            for client in room["clients"]:
                                for client_socket in clients:
                                    if clients[client_socket] == client:
                                        client_socket.send((username + ": " + message + "\n").encode())

                    # send a confirmation message to the user
                    client_socket.send(("Message sent").encode())
                    #mongoDB.sendMassge(conn, room, username, message)

                """
                elif command == "change_password":
                    # Example usage 
                    if mongoDB.change_password(conn, username, password, 'new_password'):
                    # Do something if the password was successfully updated
                        client_socket.send(("Your password has been changed.").decode())
                    else:
                    # Do something if the password change failed
                        client_socket.send(("Please try again.").decode())


                elif command == "exit":
                    # close the user's connection
                    client_socket.close()
                    break

                elif command == "help":
                    # close the user's connection
                    client_socket.send(HELP_MASSAGE.encode())


        #wromg password massge.
        if mongoDB.user_exists(conn, username):
                client_socket.send(("wrong password.\n pleas try agaim").encode())

        #simg up
        else:
            client_socket.send(("do you want to sing up(y/n)? ").encode())
            ans = get(client_socket)
            if ans == "y":
                client_socket.send(("what yout email is? ").encode())
                email = get(client_socket)
                #sent email with code. cansled

                #add user to database.
                mongoDB.add_user(conn, username, password, email)
    """




def get(s):
    a = ''
    while(len(a) < 3):
        a= s.recv(1024).decode().replace('\n\r', '')
    return a











try:
    main()
except(TypeError):
    print("code ended")
