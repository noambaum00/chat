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

            
def sign_in(db,username, password):
        users = db["users"]

        user = users.find_one({"username": username})
        if user and user["password"] == password:
            return True
        else:
            return False


def isadmin(username):
    return username == "root"
    
    users = db["users"]

    user = users.find_one({"username": username})
    return user["isadmin"]

    

def add_user(db,username, password):
        users = db["users"]

        user = {"username": username, "password": password, "id": 1}#------------------------- toDo id
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


def admin_change_password(db, username, new_password):
        users = db["users"]

        user = users.find_one({"username": username})
        if user:
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
        users = db["users"]

        user = users.find_one({"username": username})
        if user:
            return user["password"]
        else:
            return None


def get_email(db,username):
        users = db["users"]

        user = users.find_one({"username": username})
        if user:
            return user["email"]
        else:
            return None


def delete_user(db,username):
        users = db["users"]

        users.delete_one({"username": username})


def addMassge(db, room, username, message):
    collection = db["mycollection"]
    #cerrent time:
    current_time = datetime.datetime.now()

    # Create document to insert
    doc = {"room": room, "username": username, "message": message, "time": current_time}

    # Insert document into collection
    collection.insert_one(doc)


def allowsUserInRoom(username):#toDo
    return True


def get_rooms():#toDo
    return[{'name': 'loby', 'clients': []}]

def deleteAll():
    pass




"""
def delete_all_data(client, database_name, collection_name):
    db = client[database_name]
    collection = db[collection_name]

    # Delete all documents in the collection
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents.")
"""