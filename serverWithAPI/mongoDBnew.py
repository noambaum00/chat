import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
class ChatDB:
    def __init__(self):
        uri = "mongodb+srv://noambaum:noambaum@cluster0.ec4wlbs.mongodb.net/?retryWrites=true&w=majority"
        # Create a new client and connect to the server
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client.chat_db
        self.users = self.db.users
        self.rooms = self.db.rooms
        self.archive = self.db.archive

    def add_user(self, username, password, role):
        user = {"username": username,
                "password": password,
                "role" : role,
                "rooms": []}
        self.users.insert_one(user)

    def add_room(self, room_name, admin):
        room = {"roomname": room_name,
                "admin": admin,
                "users": [],
                "messages": []}
        self.rooms.insert_one(room)
        self.add_user_to_room(admin,room_name)

    def add_user_to_room(self, username, room_name):
        self.rooms.update_one({"roomname": room_name}, {"$push": {"users": username}})
        self.users.update_one({"username": username}, {"$push": {"rooms": room_name}})

    def remove_user_from_room(self, username, room_name):
        self.rooms.update_one({"roomname": room_name}, {"$pull": {"users": username}})
        self.users.update_one({"username": username}, {"$pull": {"rooms": room_name}})

    def add_message(self, username, room_name, message):
        message = {"username": username,
                   "message": message,
                   "time": datetime.datetime.now()}
        self.rooms.update_one({"roomname": room_name}, {"$push": {"messages": message}})

    def get_messages(self, room_name):
        return self.rooms.find_one({"roomname": room_name})["messages"]

    def get_users_rooms(self, username):
        return self.users.find_one({"username": username})["rooms"]

    def get_users_in_room(self, room_name):
        return self.rooms.find_one({"roomname": room_name})["users"]

        
    def get_room_admin(self, room_name):
        return self.rooms.find_one({"roomname": room_name})["admin"]

    def room_exists(self, room_name):
        user = self.rooms.find_one({"roomname": room_name})
        return bool(user)


    def archive_room(self, room_name):
        room = self.rooms.find_one({"roomname": room_name})
        self.archive.insert_one(room)
        self.rooms.delete_one({"roomname": room_name})

    def get_archive(self):
        return self.archive.find()

    def get_users_list(self):
        return [doc['username'] for doc in self.users.find({}, {'_id': 0, 'username': 1})]

    def get_rooms_list(self):
        return [doc['roomname'] for doc in  self.rooms.find({}, {'_id': 0, 'roomname': 1})]

    def get_user(self, username):
        return self.users.find_one({"username": username})
    
    def user_exists(self, username):
        user = self.users.find_one({"username": username})
        return bool(user)

    def get_admin(self, username):
        return self.users.find_one({"username": username})["isadmin"]


    def get_room(self, room_name):
        return self.rooms.find_one({"roomname": room_name})

    def get_user_password(self, username):
        return self.users.find_one({"username": username})["password"]

    def login(self, username, password):
        user = self.users.find_one({"username": username})
        if user is None:
            return False
        if user["password"] == password:
            return True
        return False

    def delete_user(self, username):
        self.users.delete_one({"username": username})

    def delete_room(self, room_name):
        self.rooms.delete_one({"username": room_name})

    def delete_archive(self, room_name):
        self.archive.delete_one({"username": room_name})

    def delete_all_users(self):
        self.users.delete_many({})

    def delete_all_rooms(self):
        self.rooms.delete_many({})

    def delete_all_archive(self):
        self.archive.delete_many({})

    def delete_all(self):
        self.delete_all_users()
        self.delete_all_rooms()
        self.delete_all_archive()

    def close(self):
        self.client.close()

        
if __name__ == "__main__":
    chat_db = ChatDB()
    chat_db.get_user("user1")
    print(chat_db.get_user("user1"))