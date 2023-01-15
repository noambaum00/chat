import telnetlib
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
    db = mongoDB.init("mongodb://localhost:27017")
    

    # create a socket object
    server_socket = telnetlib.Telnet()


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
    client_socket.write(("Thank you for connecting").encode())

    # get the client's username and password
    client_socket.write(("sooo... what your name is? ").encode())

    username = get(client_socket)
    client_socket.write(("and what your passward?").encode())
    password = get(client_socket)

    isadmin = mongoDB.isadmin(username)
    if isadmin == True:
        client_socket.write(("admin\n").encode())
    else:
        client_socket.write(("user\n").encode())

    # if the user is not an admin, add the user to the list of connected
    # clients and set the user's status to "user"
    clients[client_socket] = username
            
    #join loby
    room_name = "loby"
    jnr(room_name, username, client_socket)

    # receive the user's commands and act on them
    while True:
        try:

            # receive the user's command
            command = get(client_socket)

            error_chack = False

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
                    
                elif command[:4] == "cls:":
                        mongoDB.close()
                        os.close()

                elif command[:5] == "dlta":
                        if command[5:] == "secretPassward":
                            mongoDB.deleteAll()
                        else:
                            send(client_socket, "wrong passward")
                else:
                    error_chack = True
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
                    

            if isadmin==False:
                error_chack = False

            elif command[:4] == "lsr:":
                    lsr(client_socket)

            elif command[:4] == "jnr:":
                    if mongoDB.allowsUserInRoom(username) == True:
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

            elif command[:4] == "hlp:":
                    send(client_socket, HELP_MASSAGE)

            elif command[:4] == "ext:":
                    # close the admin's connection
                    client_socket.close()
                    return

            else:
                    error_chack = True



            if error_chack == False:
                send(client_socket, command + " : not found")
                pass
                

                """
                elif command[:4] == "chp:":
                    command = command[:4].split(",")

                    if mongoDB.change_password(conn, username, command[1], command[2]):
                    # Do something if the password was successfully updated
                        client_socket.write(("Your password has been changed.").decode())
                    else:
                    # Do something if the password change failed
                        client_socket.write(("Please try again.").decode())

                """
        except EOFError:
            client_socket.close()
            break

"""
            #wromg password massge.
            if mongoDB.user_exists(db, username):
                    client_socket.write(("wrong password.\n pleas try agaim").encode())

            #simg up
            else:
                client_socket.write(("do you want to sing up(y/n)? ").encode())
                ans = get(client_socket)
                if ans == "y":
                    client_socket.write(("what yout email is? ").encode())
                    email = get(client_socket)
                    #sent email with code. cansled

                    #add user to database.
                    mongoDB.add_user(db, username, password, email)
        """




def get(s):
    return s.read_until(b'\n').strip()


def send(s,a):
    s.write((a).encode())




try:
    main()
except:
    print(error)