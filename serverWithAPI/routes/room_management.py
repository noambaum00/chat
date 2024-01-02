# app/routes/room_management.py

from flask import jsonify, request, abort
from ..defines import app, ROLES
from ..decorators import require_privilege
# user_management.py
from flask import Blueprint

room_blueprint = Blueprint('room_management', __name__)

# Define your routes and other functionalities
# Assume rooms are stored in a simple list for demonstration purposes
rooms = ['room1', 'room2', 'room3']

@user_blueprint.route('/api/rooms/<name>', methods=['POST'])
@require_privilege('manage_users')
def get_users(name):
    return jsonify(users)# db get user in room 

@room_blueprint.route('/api/rooms', methods=['GET'])
@require_privilege('')
def get_rooms():
    return jsonify(rooms)

@room_blueprint.route('/api/rooms', methods=['POST'])
@require_privilege('manage_rooms')
def add_room():
    data = request.get_json()
    room_name = data.get('room_name')

    if room_name in rooms:
        abort(400)  # Bad Request - Room already exists

    rooms.append(room_name)
    return jsonify({'message': f'Room {room_name} added successfully'})


@room_blueprint.route('/api/rooms/<room>', methods=['DELETE'])
@require_privilege('manage_rooms')
def delete_room(room):
    if room not in rooms:
        abort(404)  # Not Found - Room not exists

    rooms.remove(room)
    return jsonify({'message': f'Room {room} deleted successfully'})

@room_blueprint.route('/api/rooms/<room>/messages', methods=['GET'])
def get_room_messages(room):
    if room not in rooms:
        abort(404)  # Not Found - Room not exists

    # You can modify this part to retrieve messages for the specific room from your data structure
    # For demonstration purposes, I'll create a simple structure to store messages
    room_messages = [
        {'user': 'user1', 'message': 'Hello from user1'},
        {'user': 'user2', 'message': 'Hi there, user1!'},
    ]

    return jsonify(room_messages)

@room_blueprint.route('/api/rooms/<room>/messages', methods=['POST'])
def send_message(room):
    if room not in rooms:
        abort(404)  # Not Found - Room not exists

    data = request.get_json()
    user = data.get('user')
    message = data.get('message')

    # You can modify this part to store the message for the specific room in your data structure
    # For demonstration purposes, I'll create a simple structure to store messages
    room_messages = [
        {'user': 'user1', 'message': 'Hello from user1'},
        {'user': 'user2', 'message': 'Hi there, user1!'},
    ]

    new_message = {'user': user, 'message': message}
    room_messages.append(new_message)

    return jsonify({'message': 'Message sent successfully'})

