# app/mongo.py

from pymongo import MongoClient
from bson.objectid import ObjectId
from bcrypt import checkpw, hashpw, gensalt

class MongoDB:
    def __init__(self, connection_string, database_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def add_user(self, username, password, email, role='user'):
        users_collection = self.get_collection('users')
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        users_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'email': email,
            'role': role,
            'joined_rooms': []
        })

    def get_user_by_username(self, username):
        users_collection = self.get_collection('users')
        return users_collection.find_one({'username': username})

    def get_user_by_id(self, user_id):
        users_collection = self.get_collection('users')
        return users_collection.find_one({'_id': ObjectId(user_id)})

    def verify_password(self, provided_password, stored_password):
        return checkpw(provided_password.encode('utf-8'), stored_password)

    def add_message(self, room, user, message):
        messages_collection = self.get_collection('messages')
        messages_collection.insert_one({
            'room': room,
            'user': user,
            'message': message,
        })

    def get_messages_in_room(self, room):
        messages_collection = self.get_collection('messages')
        return list(messages_collection.find({'room': room}))

    def add_room(self, room_name):
        rooms_collection = self.get_collection('rooms')
        rooms_collection.insert_one({'room_name': room_name, 'messages': []})

    def get_rooms(self):
        rooms_collection = self.get_collection('rooms')
        return list(rooms_collection.find())

    def add_message_to_room(self, room_id, user, message):
        rooms_collection = self.get_collection('rooms')
        messages_collection = self.get_collection('messages')

        message_data = {'user': user, 'message': message}
        rooms_collection.update_one({'_id': ObjectId(room_id)}, {'$push': {'messages': message_data}})
        messages_collection.insert_one({'room_id': room_id, 'user': user, 'message': message})
