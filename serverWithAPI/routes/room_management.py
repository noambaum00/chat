# app/routes/room_management.py

from flask import jsonify, request, abort
from ...serverWithAPI import app, rooms, require_privilege, mongo
from ..decorators import require_privilege

# Assume rooms are stored in a simple list for demonstration purposes
rooms = ['room1', 'room2', 'room3']

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = mongo.get_rooms()
    return jsonify(rooms)

@app.route('/api/rooms', methods=['POST'])
@require_privilege('manage_rooms')
def add_room():
    data = request.get_json()
    room_name = data.get('room_name')

    if not room_name:
        abort(400)  # Bad Request - Room name is required

    # Add room to MongoDB
    mongo.add_room(room_name)

    return jsonify({'message': f'Room {room_name} added successfully'})

@app.route('/api/rooms/<room>', methods=['DELETE'])
@require_privilege('manage_rooms')
def delete_room(room):
    if room not in rooms:
        abort(404)  # Not Found - Room not exists

    rooms.remove(room)
    return jsonify({'message': f'Room {room} deleted successfully'})

@app.route('/api/rooms/<room>/messages', methods=['GET'])
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

@app.route('/api/rooms/<room_id>/messages', methods=['GET'])
def get_room_messages(room_id):
    room_messages = mongo.get_messages_in_room(room_id)
    return jsonify(room_messages)

@app.route('/api/rooms/<room_id>/messages', methods=['POST'])
@require_privilege('send_messages')
def send_message(room_id):
    data = request.get_json()
    user = get_jwt_identity()['username']
    message = data.get('message')

    # Add message to room and messages collection in MongoDB
    mongo.add_message_to_room(room_id, user, message)

    return jsonify({'message': 'Message sent successfully'})
