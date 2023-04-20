import socket
from mongoDB import ChatDB
import os
from _thread import *
from chat_commend import *

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
#connect db
db = ChatDB("mongodb+srv://noambaum:noambaums@cluster0.ec4wlbs.mongodb.net")

def main():
    

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
            client_socket.send(("admin\n").encode())
        else:
            client_socket.send(("user\n").encode())

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

                    if command[:4] == "lsu:":
                        client_socket.send(str(clients).encode())

                    elif command[:4] == "dlr:":
                        dlr(command[4:], client_socket)
                        

                    elif command[:4] == "kcu:":
                        kcu(command[4:], client_socket, clients)

                    elif command[:4] == "dlu:":
                        dlu(command[4:], client_socket)
                    
                    elif command[:4] == "ext:":
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
                        error_chack = True
                    
                    

                elif command[0:4] == "crr:":
                    try:
                        db.add_room(room_name, username)
                        room = {"name": room_name, "clients": []}
                        rooms.append(room)
                        client_socket..send(("Room created").encode())
                    except:
                        client_socket.send(("error").encode())

                if command[:4] == "lsr:":
                    client_socket.send(str(rooms).encode())

                elif command[:4] == "jnr:":
                    if db.allowsUserInRoom(username) == True:
                        room_name = command[4:]
                        jnr(room_name,username,client_socket)
                    else:
                        send(client_socket, "you not allow in her.\n")
                        
                elif command[:4] == "lvr:":
                    lvr(username,client_socket)

                elif command[:5] == "lcur:":
                    lcur(room_name, client_socket)

                elif command[:4] == "msg:":
                    message =username + ": " + command[4:]
                    msg(message, room_name, client_socket, clients, isadmin)

                elif command[:3] == "dm:":
                    message = username + ": " + command[4:].strip(",")
                    dm(message[0], message[1], client_socket, clients, isadmin)

                elif command[:4] == "hlp":
                    client_socket.send(HELP_MASSAGE.encode())

                elif command[:4] == "ext:":
                    # close the admin's connection
                    client_socket.close()
                    return


                elif command[:4] == "chp:":#---------------------- add function to mongoDb class
                    command = command[:4].split(",")

                    if db.change_password(username, command[1], command[2]):
                    # Do something if the password was successfully updated
                        client_socket.send(("Your password has been changed.").decode())
                    else:
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