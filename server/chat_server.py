import sys
import socket
import os
from _thread import *
import atexit

from defins import *
from mongoDB import ChatDB
from MYconnection import connection


#global variables
global rooms

def main(server_socket):
    #connect db
    global db
    print("connecting to db")
    db = ChatDB("mongodb+srv://noambaum:noambaums@cluster0.ec4wlbs.mongodb.net")
    rooms = db.get_rooms_list()

    # queue up to 50 requests
    server_socket.listen(50)

    print("LISENING")

    #threading staf
    ThreadCount = 0



    # create a dictionary of connected clients, with the key being the client's
    # socket and the value being the client's username; need to anderstand whay it is
    global clients
    clients = {}

    # start a new thread for the admin terminul command loop
    #start_new_thread(terminal_command_loop(""))#--------------------------------------------
    while True:
        # establish a connection
        client_socket, addr = server_socket.accept()

        print('Connected to: ' + addr[0] + ':' + str(addr[1]))

        sock = client_socket(client_socket)

        start_new_thread(multi_threaded_client, (sock, db))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))


def multi_threaded_client(sock , db):
    
    global stop_thread
    stop_thread = False
    # send a thank you message to the client
    sock.send("Thank you for connecting")

    # get the client's username and password
    sock.send("sooo... what your name is? ")

    username = sock.resv()
    sock.send(("and what your passward?").encode())
    password = sock.resv()

    
    if db.login(username, password) == 2:
        if db.is_server_admin(username):
            isadmin = True
            sock.send("admin\n")
        else:
            sock.send("user\n")
            isadmin = False

        # clients and set the user's status to "user"
        clients[sock] = username
                
        # receive the user's commands and act on them
        while True:
            try:
                if stop_thread == True:
                    break
                
                # receive the user's command
                command = sock.recv().split(':')



                error_chack = False

                if isadmin:
                    #admin staff
                    if command[0] == "lsu":#todo use mongo function
                        sock.send(str(clients).encode())

                    elif command[0] == "dlr":
                            # delete the room from the list of rooms
                        if db.is_room_admin(command[4:], username):
                            for room in rooms:
                                if room["name"] == room_name:
                                    rooms.remove(room)
                            # send a confirmation message to the admin
                            db.delete_room(command[4:], username)
                            sock.send("Room deleted")
                        else:
                            sock.send("{username} non room admin")
                        

                    elif command[0] == "dlu":
                    # delete the user from the list of connected clients
                        db.delete_user(command[1], username)
                        sock.send("User deleted")

                                        
                    elif command[0] == "shutdown":
                        db.close()
                        os.close()

                    elif command[0] == "dlta":
                        if command[1] == "secretPassward":
                            db.deleteAll()
                        else:
                            sock.send("wrong passward")
                    
                    elif command[0] == "achp":#---------------------------------need to add function to mongoDB class.
                        commandor = command[2].split(",")
                        if db.admin_change_password(db, commandor[1], commandor[2]):
                            # Do something if the password was successfully updated
                            sock.send("Your password has been changed.")
                        else:
                            # Do something if the password change failed
                            sock.send("Please try again.")

                    else:
                        error_chack += 1
                    
                    
                # user staff
                elif command[0] == "crr":
                    try:
                        db.add_room(room_name, username)
                        room = {"name": room_name, "clients": []}
                        rooms.append(room)
                        sock.send("Room created")
                    except:
                        sock.send("error")

                if command[0] == "lsr":
                    sock.send(str(rooms))

                elif command[0] == "jnr":
                    room_name = command[1]
                    if not db.room_exists(room_name):
                        socket.send("room anexisting")
                    elif db.allowed_user_in_room(username,room_name):
                        db.add_user_to_room(username, room_name)  
                        for room in rooms:
                            if room["name"] == room_name:
                                room["clients"].append(username)
                        # send a confirmation message to the user
                        sock.send(room_name + " joined\n")
                    else:
                        sock.send("you are not allow in her.\n")
                        
                
                elif command[0] == "lvr":
                    room_name = command[1]
                    for room in rooms:
                        if room["name"] == room_name:
                            room["clients"].remove(username)
                            # send a confirmation message to the user
                            db.delete_user_from_room(username, room_name)
                            sock.send(room_name + " left\n")

                elif command[0] == "lcur":
                    if db.user_inside_room(username, command[1]):
                        db.get_users_in_room(room_name)
                        
                elif command[0] == "msg": #todo wrote this again.
                    break
                    message =username + ": " + command[4:]
                    msg(message, room_name, client_socket, clients, isadmin)

                elif command[0] == "hlp":
                    sock.send(HELP_MASSAGE)

                elif command[0] == "ext":
                    # close the admin's connection
                    sock.close()
                    return 0
                    break
                
                


                elif command[0] == "chp":
                    commandor = command[2].split(",")

                    if db.change_password(username, commandor[1], commandor[2])==1:
                    # Do something if the password was successfully updated
                        sock.send("Your password has been changed.")
                    else: #todo add errors messages
                    # Do something if the password change failed
                        sock.send("Please try again.")

                elif command == "hlp":
                    sock.send(HELP_MASSAGE)

                else:
                    error_chack = True

                
                if error_chack == True:
                    sock.send(command + " : not found")
                    pass




                
            except Exception as e:
                print(e)

    #wromg password massge.
    elif db.login(username, password) == 1:#----------------add function to mongoDb class
        sock.send("password not connected to username.\n pleas try agaim")
        multi_threaded_client(sock , db)
        

    #sing up
    else:
        sock.send("do you want to sing up(y/n)? ")#todo rewrite
        ans = sock.recv()
        if ans == "y":
            sock.send(("what yout email is? ").encode())
            email = sock.recv()
            #sent email with code. #todo future

            #add user to database.
            db.add_user(username, password, email)



def terminal_command_loop(a):
    pass
    print("Terminal command")
    return 1

@atexit.register
def say_goodbye():
    for client in clients:
        client.send("goodbye\n")
        client.close()
        clients.pop(client)
        ThreadCount -= 1
        print('Thread Number:'+ str(ThreadCount))
    db.close()
    print("Goodbye")
    
    sys.exit(0)


if __name__ == "__main__":
    print(ADMIN_COMMENDS + "" + HELP_MASSAGE)
    main()
