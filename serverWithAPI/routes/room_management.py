# app/routes/room_management.py

from flask import jsonify, request, abort, Blueprint
from ..defines import app
from ..decorators import require_privilege
from ..mongoDBnew import ChatDB

db = ChatDB()
room_blueprint = Blueprint('room_management', __name__)
#@require_privilege("")
@room_blueprint.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms_list = db.get_rooms_list()
    return jsonify(rooms_list)

@room_blueprint.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.get_json()
    room_name = data.get('room_name')
    admin = data.get('admin')

    existing_room = db.get_room(room_name)
    if existing_room:
        abort(400)  # Bad Request - Room already exists

    db.add_room(room_name, admin)  # You might need to specify the admin based on your application logic
    return jsonify({'message': f'Room {room_name} added successfully'})

@room_blueprint.route('/api/rooms/<room>', methods=['DELETE'])
def delete_room(room):
    existing_room = db.get_room(room)
    if not existing_room:
        abort(404)  # Not Found - Room not exists

    db.delete_room(room)
    return jsonify({'message': f'Room {room} deleted successfully'})

@room_blueprint.route('/api/rooms/<room>/messages', methods=['GET'])
def get_room_messages(room):
    existing_room = db.get_room(room)
    if not existing_room:
        abort(404)  # Not Found - Room not exists

    room_messages = db.get_messages(room)
    return jsonify(room_messages)

@room_blueprint.route('/api/rooms/<room>/messages', methods=['POST'])
def send_message(room):
    existing_room = db.get_room(room)
    if not existing_room:
        abort(404)  # Not Found - Room not exists

    data = request.get_json()
    user = data.get('user')
    message = data.get('message')

    db.add_message(user, room, message)

    return jsonify({'message': 'Message sent successfully'})