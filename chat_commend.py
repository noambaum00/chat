import socket
import mongoDB



# create a list of rooms
global rooms
rooms = []
rooms = mongoDB.get_rooms()





def lsr(s):
    # send the list of rooms to the admin
    s.send(str(rooms).encode())


def lsu(s,clients):
    # send the list of connected users to the admin
    s.send(str(clients).encode())

def crr(room_name,s):
    room = {"name": room_name, "clients": []}
    rooms.append(room)
    
    # send a confirmation message to the admin
    s.send(("Room created").encode())


def dlr(room_name,s):
    # delete the room from the list of rooms
    for room in rooms:
        if room["name"] == room_name:
            rooms.remove(room)
    # send a confirmation message to the admin
    s.send((b"Room deleted").encode())


def jnr(room_name,username,s):
    # join the room
    for room in rooms:
        if room["name"] == room_name:
            room["clients"].append(username)
    # send a confirmation message to the user
    s.send(("Room joined").encode())


def lvr(room_name, username,s):
    # leave the room
    for room in rooms:
        if room["name"] == room_name:
            room["clients"].remove(username)

    # send a confirmation message to the user
    s.send(("Room left").encode())


def lsur(room_name,s):
    # send the list of users in the room to the admin
    for room in rooms:
        if room["name"] == room_name:
            s.send(str(room["clients"]).encode())


def kcu(usernameToKick, s, clients):
    # kick the user
    for client in clients:
        if clients[client] == usernameToKick:
            client.close()
            del clients[client]
    # send a confirmation message to the admin
    s.send('User : {usernameToKick} kicked')


def dlu(usernameToKick,s):
    #delete username frome database
    #mongoDB.delete_user(conn, usernameToDelete)
    s.send('User : {usernameToDelete} deleted')

def ADmsg(message, room_name ,s, clients):

    # send the message to the room
    for room in rooms:
        if room["name"] == room_name:
            for client in room["clients"]:
                for client_socket in clients:
                    if clients[client_socket] == client:
                        client_socket.send(("admin>> " + message + "\n").encode())

    # send a confirmation message to the user
    s.send(("Message sent").encode())

    #mongoDB.sendMassge(conn, room, username, message)


def msg(message, room_name ,s, clients):

    # send the message to the room
    for room in rooms:
        if room["name"] == room_name:
            for client in room["clients"]:
                for client_socket in clients:
                    if clients[client_socket] == client:
                        client_socket.send((message + "\n").encode())

    # send a confirmation message to the user
    s.send(("Message sent").encode())

    #mongoDB.sendMassge(conn, room, username, message)
