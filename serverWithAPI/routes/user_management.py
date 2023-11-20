# app/routes/user_management.py

from flask import jsonify, request, abort
from app import app, ROLES, users, generate_token, require_privilege

# Assume rooms are stored in a simple list for demonstration purposes
rooms = ['room1', 'room2', 'room3']

@app.route('/api/users', methods=['GET'])
@require_privilege('manage_users')
def get_users():
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
@require_privilege('manage_users')
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')

    if username in users:
        abort(400)  # Bad Request - User already exists

    if not email:
        abort(400)  # Bad Request - Email is required

    users[username] = {'password': password, 'role': role, 'email': email}
    return jsonify({'message': f'User {username} created successfully'})

@app.route('/api/users/<username>', methods=['PUT'])
@require_privilege('manage_users')
def update_user(username):
    if username not in users:
        abort(404)  # Not Found - User not exists

    data = request.get_json()
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if password:
        users[username]['password'] = password
    if email:
        users[username]['email'] = email
    if role:
        users[username]['role'] = role

    return jsonify({'message': f'User {username} updated successfully'})

@app.route('/api/users/<username>', methods=['DELETE'])
@require_privilege('manage_users')
def delete_user(username):
    if username not in users:
        abort(404)  # Not Found - User not exists

    del users[username]
    return jsonify({'message': f'User {username} deleted successfully'})

@app.route('/api/rooms', methods=['GET'])
@require_privilege('manage_rooms')
def get_rooms():
    return jsonify(rooms)

@app.route('/api/rooms', methods=['POST'])
@require_privilege('manage_rooms')
def add_room():
    data = request.get_json()
    room_name = data.get('room_name')

    if room_name in rooms:
        abort(400)  # Bad Request - Room already exists

    rooms.append(room_name)
    return jsonify({'message': f'Room {room_name} added successfully'})

@app.route('/api/rooms/<room>', methods=['DELETE'])
@require_privilege('manage_rooms')
def delete_room(room):
    if room not in rooms:
        abort(404)  # Not Found - Room not exists

    rooms.remove(room)
    return jsonify({'message': f'Room {room} deleted successfully'})

@app.route('/api/start_service', methods=['POST'])
@require_privilege('start_service')
def start_service():
    # Add code here to start the service
    return jsonify({'message': 'Service started successfully'})

@app.route('/api/close_service', methods=['POST'])
@require_privilege('close_service')
def close_service():
    # Add code here to close the service
    return jsonify({'message': 'Service closed successfully'})

@app.route('/api/change_password', methods=['PUT'])
@require_privilege('change_password')
def change_password():
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if username not in users or users[username]['password'] != old_password:
        abort(401)  # Unauthorized - Incorrect username or old password

    users[username]['password'] = new_password
    return jsonify({'message': 'Password changed successfully'})

@app.route('/api/force_change_password/<username>', methods=['POST'])
@require_privilege('force_change_password')
def force_change_password(username):
    if username not in users:
        abort(404)  # Not Found - User not exists

    data = request.get_json()
    new_password = data.get('new_password')

    users[username]['password'] = new_password
    return jsonify({'message': f'Password for user {username} changed by admin'})
