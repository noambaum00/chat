# app/__init__.py

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_demo_purposes'

# Define user roles and associated privileges
ROLES = {
    'user': ['read_messages', 'send_messages', 'add_room', 'change_password'],
    'admin': ['read_messages', 'send_messages', 'manage_users', 'manage_rooms', 'start_service', 'close_service', 'force_change_password'],
}

from app.routes import messages, user_management, room_management
