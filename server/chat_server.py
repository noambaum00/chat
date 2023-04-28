import socket
from mongoDB import ChatDB
import os
from _thread import *

#global variables
global rooms

HELP_MASSAGE = """
the list comend is:
\tlsr: = list room
\tjnr: = join room
\tlvr: = leave room
\tlsur:= list users in room
\tmsg: = send message
\tadr: = add room to user list
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
\tachp: = admin change password
\text: = exit
"""

def main():
    #connect db
    db = ChatDB("mongodb+srv://noambaum:noambaums@cluster0.ec4wlbs.mongodb.net")
    rooms = []
    rooms = db.get_rooms_list()


    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = "127.0.0.1"

    port = 585

    print("STSRT")

    # bind to the port
    server_socket.bind((host, port))

    print("BIND")

    # queue up to 50 requests
    server_socket.listen(50)

    print("LISENING")

    #threading staf
    ThreadCount = 0



    # create a dictionary of connected clients, with the key being the client's
    # socket and the value being the client's username
    global clients
    clients = {}


    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        start_new_thread(multi_threaded_client, (client_socket, db))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))


def multi_threaded_client(client_socket , db):
    
    global stop_threads
    stop_threads = False
    # send a thank you message to the client
    client_socket.send(("Thank you for connecting").encode())

    # get the client's username and password
    client_socket.send(("sooo... what your name is? ").encode())

    username = get(client_socket)
    client_socket.send(("and what your passward?").encode())
    password = get(client_socket)

    
    if db.login(username, password) == 2:
        if db.is_server_admin(username):
            isadmin = True
            client_socket.send(("admin\n").encode())
        else:
            client_socket.send(("user\n").encode())
            isadmin = False

        # if the user is not an admin, add the user to the list of connected
        # clients and set the user's status to "user"
        clients[client_socket] = username
                
        #join loby

        # receive the user's commands and act on them
        while True:
            try:
                if stop_threads == True:
                    break
                
                # receive the user's command
                command = get(client_socket)



                error_chack = False

                if isadmin:
                    #admin staff
                    if command[:4] == "lsu:":
                        client_socket.send(str(clients).encode())

                    elif command[:4] == "dlr:":
                            # delete the room from the list of rooms
                        if db.is_room_admin(command[4:], username):
                            for room in rooms:
                                if room["name"] == room_name:
                                    rooms.remove(room)
                            # send a confirmation message to the admin
                            db.delete_room(command[4:], username)
                            client_socket.send(("Room deleted").encode())
                        else:
                            client_socket.send(("{username} non room admin").encode())
                        
                    

                    elif command[:4] == "dlu:":
                    # delete the user from the list of connected clients
                        db.delete_user(command[4:], username)
                        client_socket.send(("User deleted").encode())

                                        
                    elif command[:9] == "shutdown:":
                        db.close()
                        os.close()

                    elif command[:5] == "dlta":
                        if command[5:] == "secretPassward":
                            db.deleteAll()
                        else:
                            send(client_socket, "wrong passward")
                    
                    elif command[:5] == "achp:":#---------------------------------need to add function to mongoDB class.
                        command = command[:5].split(",")
                        if db.admin_change_password(db, command[1], command[2]):
                            # Do something if the password was successfully updated
                            client_socket.send(("Your password has been changed.").decode())
                        else:
                            # Do something if the password change failed
                            client_socket.send(("Please try again.").decode())

                    else:
                        error_chack += 1
                    
                    
                # user staff
                elif command[0:4] == "crr:":
                    try:
                        db.add_room(room_name, username)
                        room = {"name": room_name, "clients": []}
                        rooms.append(room)
                        client_socket.send(("Room created").encode())
                    except:
                        client_socket.send(("error").encode())

                if command[:4] == "lsr:":
                    client_socket.send(str(rooms).encode())

                elif command[:4] == "jnr:":
                    room_name = command[4:]
                    if db.allowed_user_in_room(username,room_name) == True:
                        db.add_user_to_room(username, room_name)  
                        for room in rooms:
                            if room["name"] == room_name:
                                room["clients"].append(username)
                        # send a confirmation message to the user
                        client_socket.send((room_name + " joined\n").encode())
                    else:
                        send(client_socket, "you not allow in her.\n")
                        
                
                elif command[:4] == "lvr:":
                    room_name = command[4:]
                    for room in rooms:
                        if room["name"] == room_name:
                            room["clients"].remove(username)
                            # send a confirmation message to the user
                            db.delete_user_from_room(username, room_name)
                            client_socket.send((room_name + " left\n").encode())


                elif command[:5] == "lcur:":
                    if db.user_inside_room(username, room_name):
                        db.get_users_in_room(room_name)
                        
                elif command[:4] == "msg:": #todo wrote this again.
                    break
                    message =username + ": " + command[4:]
                    msg(message, room_name, client_socket, clients, isadmin)

                elif command[:4] == "hlp":
                    client_socket.send(HELP_MASSAGE.encode())

                elif command[:4] == "ext:":
                    # close the admin's connection
                    client_socket.close()
                    return 0
                    break
                
                


                elif command[:4] == "chp:":
                    command = command[:4].split(",")

                    if db.change_password(username, command[1], command[2])==1:
                    # Do something if the password was successfully updated
                        client_socket.send(("Your password has been changed.").decode())
                    else: #todo add errors messages
                    # Do something if the password change failed
                        client_socket.send(("Please try again.").decode())

                elif command == "hlp":
                    client_socket.send(HELP_MASSAGE.encode())

                else:
                    error_chack = True

                
                if error_chack == True:
                    send(client_socket, command + " : not found")
                    pass

                
            except Exception as e:
                print(e)
                lvr(username,client_socket)

    #wromg password massge.
    elif db.login(username, password) == 1:#----------------add function to mongoDb class
        client_socket.send(("password not connected to username.\n pleas try agaim").encode())
        multi_threaded_client(client_socket , db)
        

    #sing up
    else:
        client_socket.send(("do you want to sing up(y/n)? ").encode())#------------------add function to mongoDB class
        ans = get(client_socket)
        if ans == "y":
            client_socket.send(("what yout email is? ").encode())
            email = get(client_socket)
            #sent email with code. cansled

            #add user to database.
            db.add_user(username, password, email)




def get(s):
    try:
        a = ''
        while(len(a) < 3):
            a= s.recv(1024).decode().replace('\r\n', '')
        return a
    except ConnectionResetError:
        stop_threads = True


def send(s,a):
    s.send((a).encode())


print(ADMIN_COMMENDS + "\n\n\n" + HELP_MASSAGE)
main()

"""try:
    main()
except:
    print(error)"""