import socket
#import mongoDB
from chat_server import db
from mongoDB import ChatDB

# create a list of rooms
global rooms

rooms = []
rooms = db.get_rooms_list()






def lsr(s):
    # send the list of rooms to the admin
    pass
    
    


def lsu(s,clients):
    # send the list of connected users to the admin
    

def crr(room_name,s):
    # send a confirmation message to the admin
    pass


def dlr(room_name,s):
    # delete the room from the list of rooms
    for room in rooms:
        if room["name"] == room_name:
            rooms.remove(room)
    # send a confirmation message to the admin
    s.send(("Room deleted").encode())


def jnr(room_name,username,s):
    # join the room
    for room in rooms:
        if room["name"] == room_name:
            room["clients"].append(username)
    # send a confirmation message to the user
    s.send((room_name + " joined\n").encode())

def adr(username, roomname, s):
    db.add_user_to_room(username, roomname)
    s.send(("room added to user " + username).encode())

def lvr(username,s):
    # leave the room
    for room in rooms:
        try:
            room.remove(username)
        except:
            pass

    # send a confirmation message to the user
    s.send(("Room left").encode())


def lcur(room_name,s):
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


def msg(message, room_name ,s, clients, isadmin):

    # send the message to the room
    for room in rooms:
        if room["name"] == room_name:
            for client in room["clients"]:
                for client_socket in clients:
                    if clients[client_socket] == client:
                        if isadmin:
                            client_socket.send((room_name+",admin>> " + message + "\n").encode())
                        else:
                            client_socket.send((room_name+","+message + "\n").encode())

    db.add_message(client, room_name, message)

    # send a confirmation message to the user
    s.send(("Message sent").encode())


def dm(message, receive, s, clients, isadmin):
    for client_socket in clients:
        if clients[client_socket] == receive:
            if isadmin:
                client_socket.send(("admin>> " + message + "\n").encode())
            else:
                client_socket.send((message + "\n").encode())
            break
