import datetime
from pymongo import MongoClient

class ChatDB:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.chat_db
        self.users = self.db.users
        self.rooms = self.db.rooms
        self.archive = self.db.archive

    def add_user(self, username, password):
        user = {"_id": username,
                "password": password,
                "rooms": []}
        self.users.insert_one(user)

    def add_room(self, room_name, admin):
        room = {"_id": room_name,
                "admin": admin,
                "users": [],
                "messages": []}
        self.rooms.insert_one(room)

    def add_user_to_room(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"users": username}})
        self.users.update_one({"_id": username}, {"$push": {"rooms": room_name}})

    def remove_user_from_room(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$pull": {"users": username}})
        self.users.update_one({"_id": username}, {"$pull": {"rooms": room_name}})

    def add_message(self, username, room_name, message):
        message = {"_id": username,
                   "message": message,
                   "time": datetime.datetime.now()}
        self.rooms.update_one({"_id": room_name}, {"$push": {"messages": message}})

    def get_messages(self, room_name):
        return self.rooms.find_one({"_id": room_name})["messages"]

    def get_users_rooms(self, username):
        return self.users.find_one({"_id": username})["rooms"]

    def get_users_in_room(self, room_name):
        return self.rooms.find_one({"_id": room_name})["users"]

        
    def get_room_admin(self, room_name):
        return self.rooms.find_one({"_id": room_name})["admin"]


    def archive_room(self, room_name):
        room = self.rooms.find_one({"_id": room_name})
        self.archive.insert_one(room)
        self.rooms.delete_one({"_id": room_name})

    def get_archive(self):
        return self.archive.find()

    def get_users_list(self):
        return self.users.find()

    def get_rooms_list(self):
        return self.rooms.find()

    def get_user(self, username):
        return self.users.find_one({"_id": username})

    def get_admin(self, username):
        return self.users.find_one({"_id": username})["isadmin"]


    def get_room(self, room_name):
        return self.rooms.find_one({"_id": room_name})

    def get_user_password(self, username):
        return self.users.find_one({"_id": username})["password"]

    def login(self, username, password):
        user = self.users.find_one({"_id": username})
        if user is None:
            return False
        if user["password"] == password:
            return True
        return False

    def delete_user(self, username):
        self.users.delete_one({"_id": username})

    def delete_room(self, room_name):
        self.rooms.delete_one({"_id": room_name})

    def delete_archive(self, room_name):
        self.archive.delete_one({"_id": room_name})

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
    chat_db.delete_all()
    chat_db.add_user("user1", "123")
    print(chat_db.get_rooms_list())