from flask import Flask, jsonify, url_for
from flask_restful import Resource
from flask_jwt_extended import JWTManager


class Defines:
    def __init__(self):
        self.app = Flask(__name__)
        #app.config['SECRET_KEY'] = 'secret_key_for_demo_purposes'
        self.app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key in production

        self.jwt = JWTManager(self.app)

        # Define user roles and associated privileges
        self.ROLES = {
            'user': ['read_messages', 'send_messages', 'add_rooms','see_room', 'change_password'],
            'admin': ['read_messages', 'send_messages', 'manage_users', 'manage_rooms', 'start_service', 'close_service', 'force_change_password'],
        }
global const
