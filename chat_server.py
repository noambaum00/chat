import socket
#import mongoDB
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
    #db = mongoDB.init("mongodb+srv://noambaum:152433qwe@cluster0.siz7qr0.mongodb.net/?retryWrites=true&w=majority")
    

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
        start_new_thread(multi_threaded_client, (client_socket, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))


def multi_threaded_client(client_socket):

    # send a thank you message to the client
    client_socket.send(("Thank you for connecting").encode())

    """
    client_socket.send(("Always wanted your data security to be thrown out the window?\n").encode())
    client_socket.send(("Always looking for the most unreliable chat?\n").encode())
    client_socket.send(("So that's exactly why we founded '@@@'\n").encode())
    client_socket.send(("With technology from the 70's.\n").encode())
    client_socket.send(("Zero data security.\n").encode())
    client_socket.send(("And the sql server is open to all.\n").encode())
    """      
    # get the client's username and password
    client_socket.send(("sooo... what your name is? ").encode())

    username = get(client_socket)
    client_socket.send(("and what your passward?").encode())
    password = get(client_socket)

    isadmin = mongoDB.isadmin(username)

    #if mongoDB.sign_in(conn, username, password):
    if True:
        if isadmin == True:
            client_socket.send(("admin\n").encode())
        else:
            client_socket.send(("user\n").encode())

        # if the user is not an admin, add the user to the list of connected
        # clients and set the user's status to "user"
        clients[client_socket] = username
            
        #join loby
        room_name = "loby"
        jnr(room_name, username, client_socket)

        # receive the user's commands and act on them
        while True:
            # receive the user's command
            command = get(client_socket)

            if isadmin:
                if command[:4] == "lsu:":
                    lsu(client_socket,clients)

                elif command[0:4] == "crr:":
                    crr(command[4:], client_socket)

                elif command[:4] == "dlr:":
                    dlr(command[4:], client_socket)
                    

                elif command[:4] == "kcu:":
                    kcu(command[4:], client_socket, clients)

                elif command[:4] == "dlu:":
                    dlu(command[4:], client_socket)
                
                """
                elif command[:5] == "achp:":
                    command = command[:5].split(",")
                    if mongoDB.admin_change_password(db, command[1], command[2]):
                        # Do something if the password was successfully updated
                        client_socket.send(("Your password has been changed.").decode())
                    else:
                        # Do something if the password change failed
                        client_socket.send(("Please try again.").decode())

                """              
                



            if command[:4] == "lsr:":
                lsr(client_socket)

            elif command[:4] == "jnr:":
                if mongoDB.allowsUserInRoom(username) == True:
                    room_name = command[4:]
                    jnr(room_name,username,client_socket)
                else:
                    send(client_socket, "you not allow in her.\n")
            elif command[:4] == "lvr:":
                lvr(command[4:], username,client_socket)

            elif command[:5] == "lsur:":
                lsur(room_name, client_socket)

            elif command[:4] == "msg:":
                    
                message =username + ": " + command[4:]
                msg(message, room_name, client_socket, clients)

            elif command[:4] == "hlp":
                client_socket.send(HELP_MASSAGE.encode())

            elif command[:4] == "ext:":
                # close the admin's connection
                client_socket.close()
                return




            else:
                send(client_socket, command + " : commend not found")
            

            """
            elif command[:4] == "chp:":
                command = command[:4].split(",")

                if mongoDB.change_password(conn, username, command[1], command[2]):
                # Do something if the password was successfully updated
                    client_socket.send(("Your password has been changed.").decode())
                else:
                # Do something if the password change failed
                    client_socket.send(("Please try again.").decode())

            elif command == "hlp":
                client_socket.send(HELP_MASSAGE.encode())

"""

"""
        #wromg password massge.
        if mongoDB.user_exists(db, username):
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
                mongoDB.add_user(db, username, password, email)
    """




def get(s):
    a = ''
    while(len(a) < 3):
        a= s.recv(1024).decode().replace('\r\n', '')
    return a

def send(s,a):
    s.send((a).encode())




try:
    main()
except:
    print("error")
