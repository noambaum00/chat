from pymongo import MongoClient
import datetime



global db
global client

def __init__(self) -> None:
    pass


def init(server):
    client = MongoClient(server)
    db = client["Cluster0"]
    return db
        

def close(db):
        # Close connection to server
        client.close()



def admin_sign_in(db,username, password):
        admin = db["admin"]

        user = admin.find_one({"username": username})
        if user and user["password"] == password:
            return True
        else:
            return False

            
def client_sign_in(db,username, password):
        users = db["users"]

        user = users.find_one({"username": username})
        if user and user["password"] == password:
            return True
        else:
            return False

def add_user(db,username, password, email):
        users = db["users"]

        user = {"username": username, "password": password, "email" : email}
        users.insert_one(user)



def change_password(db, username, old_password, new_password):
        users = db["users"]

        user = users.find_one({"username": username})
        if user and user["password"] == old_password:
            user["password"] = new_password
            users.update_one({"username": username}, {"$set": user})
            return True
        else:
            return False


def user_exists(db,username):
        users = db["users"]

        user = users.find_one({"username": username})
        if user:
            return True
        else:
            return False



def get_password(db,username):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        users = db["users"]

        user = users.find_one({"username": username})
        if user:
            return user["password"]
        else:
            return None


def get_email(db,username):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        users = db["users"]

        user = users.find_one({"username": username})
        if user:
            return user["email"]
        else:
            return None


def delete_user(db,username):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        users = db["users"]

        users.delete_one({"username": username})


def sendMassge(db, room, username, message):
    collection = db["mycollection"]
    #cerrent time:
    current_time = datetime.datetime.now()

    # Create document to insert
    doc = {"room": room, "username": username, "message": message, "time": current_time}

    # Insert document into collection
    collection.insert_one(doc)

def allowsUserInRoom(username):#toDo
    pass


def returnRooms():#toDo
    pass

