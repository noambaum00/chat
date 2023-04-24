import datetime
import pymongo
from pymongo import MongoClient

class ChatDB:
    def __init__(self, url):
        self.client = MongoClient(url)
        self.db = self.client.chat_db
        self.users = self.db.users
        self.rooms = self.db.rooms
        self.archive = self.db.archive

    def add_user(self, username, password, email):
        user = {"_id": username,
                "password": password,
                "email": email,
                "rooms": []}
        self.users.insert_one(user)

    def add_room(self, room_name, admin):
        room = {"_id": room_name,
                "admin": admin,
                "users": [],
                "messages": []}
        self.rooms.insert_one(room)
        add_user_to_room(admin, room_name)

    def add_user_to_room(self, username, room_name):
        try:
            self.rooms.find_one{"_id": room_name}
            self.rooms.update_one({"_id": room_name}, {"$push": {"users": username}})
            self.users.update_one({"_id": username}, {"$push": {"rooms": room_name}})
            return True
        except:
            return False

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

    def get_rooms(self, username):#make working
        return self.users.find_one({"_id": username})["rooms"]

    def get_users(self, room_name):
        return self.rooms.find_one({"_id": room_name})["users"]

    def get_room_admin(self, room_name):
        return self.rooms.find_one({"_id": room_name})["admin"]

    def get_all_rooms_and_users(self):
        rooms = self.get_rooms_list()
        rooms_and_users = []
        for room in rooms:
            rooms_and_users.append({'name': room['_id'], 'clients': room['users']})
        return rooms_and_users
    
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
    
    def add_permission(self, username, permission):
        self.users.update_one({"_id": username}, {"$push": {"permissions": permission}})

    def remove_permission(self, username, permission):
        self.users.update_one({"_id": username}, {"$pull": {"permissions": permission}})

    def get_permissions(self, username):
        return self.users.find_one({"_id": username})["permissions"]

    def is_server_admin(self, username):
        try:
            return "server_admin" in self.get_permissions(username)
        except:
            return 0

    def get_room(self, room_name):
        return self.rooms.find_one({"_id": room_name})

    def get_user_password(self, username):
        return self.users.find_one({"_id": username})["password"]

    def login(self, username, password):
        user = self.users.find_one({"_id": username})
        if user is None:
            return 0
        if user["password"] == password:
            return 2
        return 1


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





class mongo_permission:
    def is_moderator(self, username):
        return "moderator" in self.get_permissions(username)

    def is_user(self, username):
        return "user" in self.get_permissions(username)

    def is_guest(self, username):
        return "guest" in self.get_permissions(username)

    def is_banned(self, username):
        return "banned" in self.get_permissions(username)

    def is_muted(self, username):
        return "muted" in self.get_permissions(username)

    def is_kicked(self, username):
        return "kicked" in self.get_permissions(username)

    def is_room_admin(self, username, room_name):
        return username in self.get_room_admin(room_name)

    def is_server_admin(self, username):
        return username == self.get_server_admin(username)

    def is_room_moderator(self, username, room_name):
        return username in self.get_room_moderators(room_name)

    def is_server_moderator(self, username):
        return username in self.get_server_moderators(username)

    def is_room_user(self, username, room_name):
        return username in self.get_room_users(room_name)

    def is_server_user(self, username):
        return username in self.get_server_users(username)

    def is_room_guest(self, username, room_name):
        return username in self.get_room_guests(room_name)

    def is_server_guest(self, username):
        return username in self.get_server_guests(username)

    def is_room_banned(self, username, room_name):
        return username in self.get_room_banned(room_name)

    def is_server_banned(self, username):
        return username in self.get_server_banned(username)

    def is_room_muted(self, username, room_name):
        return username in self.get_room_muted(room_name)

    def is_server_muted(self, username):
        return username in self.get_server_muted(username)

    def is_room_kicked(self, username, room_name):
        return username in self.get_room_kicked(room_name)

    def is_server_kicked(self, username):
        return username in self.get_server_kicked(username)

    def get_room_moderators(self, room_name):
        return self.rooms.find_one({"_id": room_name})["moderators"]

    def get_server_moderators(self, username):
        return self.users.find_one({"_id": username})["moderators"]

    def get_room_users(self, room_name):
        return self.rooms.find_one({"_id": room_name})["users"]

    def get_server_users(self, username):
        return self.users.find_one({"_id": username})["users"]

    def get_room_guests(self, room_name):
        return self.rooms.find_one({"_id": room_name})["guests"]

    def get_server_guests(self, username):
        return self.users.find_one({"_id": username})["guests"]

    def get_room_banned(self, room_name):
        return self.rooms.find_one({"_id": room_name})["banned"]

    def get_server_banned(self, username):
        return self.users.find_one({"_id": username})["banned"]

    def get_room_muted(self, room_name):
        return self.rooms.find_one({"_id": room_name})["muted"]

    def get_server_muted(self, username):
        return self.users.find_one({"_id": username})["muted"]

    def get_room_kicked(self, room_name):
        return self.rooms.find_one({"_id": room_name})["kicked"]

    def get_server_kicked(self, username):
        return self.users.find_one({"_id": username})["kicked"]

    def add_room_moderator(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"moderators": username}})

    def add_server_moderator(self, username, room_name):
        self.users.update_one({"_id": username}, {"$push": {"moderators": username}})

    def add_room_user(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"users": username}})

    def add_server_user(self, username, room_name):
        self.users.update_one({"_id": username}, {"$push": {"users": username}})

    def add_room_guest(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"guests": username}})

    def add_server_guest(self, username, room_name):
        self.users.update_one({"_id": username}, {"$push": {"guests": username}})

    def add_room_banned(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"banned": username}})

    def add_server_banned(self, username, room_name):
        self.users.update_one({"_id": username}, {"$push": {"banned": username}})

    def add_room_muted(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"muted": username}})

    def add_server_muted(self, username, room_name):
        self.users.update_one({"_id": username}, {"$push": {"muted": username}})

    def add_room_kicked(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$push": {"kicked": username}})

    def add_server_kicked(self, username, room_name):
        self.users.update_one({"_id": username}, {"$push": {"kicked": username}})

    def remove_room_moderator(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$pull": {"moderators": username}})

    def remove_server_moderator(self, username, room_name):
        self.users.update_one({"_id": username}, {"$pull": {"moderators": username}})

    def remove_room_user(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$pull": {"users": username}})

    def remove_server_user(self, username, room_name):
        self.users.update_one({"_id": username}, {"$pull": {"users": username}})

    def remove_room_guest(self, username, room_name):
        self.rooms.update_one({"_id": room_name}, {"$pull": {"guests": username}})

    def remove_server_guest(self, username, room_name):
        self.users.update_one({"_id": username}, {"$pull": {"guests": username}})






if __name__ == "__main__":
    chat_db = ChatDB("mongodb+srv://noambaum:noambaum@cluster0.ec4wlbs.mongodb.net")
    #chat_db.delete_all()
    #chat_db.add_user("noam", "password")
    chat_db.add_permission("noam", "server_admin")
    print(chat_db.get_rooms_list())