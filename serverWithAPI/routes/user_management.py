# app/routes/user_management.py

from flask import jsonify, request, abort,Blueprint
from flask_jwt_extended import create_access_token
from ..defines import app
from ..decorators import require_privilege
from ..mongoDBnew import ChatDB

db = ChatDB()
# Define your routes and other functionalities
user_blueprint = Blueprint('user_management', __name__)

@user_blueprint.route('/api/users', methods=['GET'])
def get_users():
    users_list = db.get_users_list()
    return jsonify(users_list)

@user_blueprint.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')

    existing_user = db.get_user(username)
    if existing_user:
        abort(400)  # Bad Request - User already exists

    if not email:
        abort(400)  # Bad Request - Email is required

    db.add_user(username, password)
    return jsonify({'message': f'User {username} created successfully'})

@user_blueprint.route('/api/users/<username>', methods=['PUT'])
def update_user(username):
    user = db.get_user(username)
    if not user:
        abort(404)  # Not Found - User not exists

    data = request.get_json()
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if password:
        db.update_user_password(username, password)
    if email:
        # Update email logic if needed
        pass
    if role:
        # Update role logic if needed
        pass

    return jsonify({'message': f'User {username} updated successfully'})

@user_blueprint.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    user = db.get_user(username)
    if not user:
        abort(404)  # Not Found - User not exists

    db.delete_user(username)
    return jsonify({'message': f'User {username} deleted successfully'})

@user_blueprint.route('/api/users/<username>/join_room', methods=['POST'])
def join_room(username):
    data = request.get_json()
    room_name = data.get('room_name')

    user = db.get_user(username)
    if not user:
        abort(404)  # Not Found - User not exists

    room = db.get_room(room_name)
    if not room:
        abort(404)  # Not Found - Room not exists

    db.add_user_to_room(username, room_name)

    return jsonify({'message': f'User {username} joined room {room_name}'})

@user_blueprint.route('/api/users/<username>/exit_room', methods=['POST'])
def exit_room(username):
    data = request.get_json()
    room_name = data.get('room_name')

    user = db.get_user(username)
    if not user:
        abort(404)  # Not Found - User not exists

    room = db.get_room(room_name)
    if not room:
        abort(404)  # Not Found - Room not exists

    db.remove_user_from_room(username, room_name)

    return jsonify({'message': f'User {username} joined room {room_name}'})


@user_blueprint.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not db.login(username, password):
        abort(401)  # Unauthorized - Incorrect username or password

    user = db.get_user(username)
    access_token = create_access_token(identity={'username': username, 'role': db.get_user(username)['role']})
    return jsonify(access_token=access_token), 200

@user_blueprint.route('/api/users/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role', 'user')  # Default role is 'user'

    if not email:
        abort(400, message= "Email is required")  # Bad Request - Email is required

    if not password:
        abort(400, message= "Password is required")  # Bad Request - Password is required

    existing_user = db.user_exists(username)
    if existing_user:
        abort(420)  # Bad Request - User already exists


    db.add_user(username, password,role)
    access_token = create_access_token(identity={'username': username, 'role': role})
    return jsonify(access_token=access_token)#), message=f'User {username} signed up successfully'), 201


@user_blueprint.route('/api/archive', methods=['GET'])
def get_archive():
    archive_list = list(db.get_archive())
    return jsonify(archive_list)

@user_blueprint.route('/api/change_password', methods=['PUT'])
#@require_privilege('')
def change_password():
    data = request.get_json()
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not db.login(username, old_password):
        abort(401)  # Unauthorized - Incorrect username or old password

    db.update_user_password(username, new_password)
    return jsonify({'message': 'Password changed successfully'})

@user_blueprint.route('/api/force_change_password/<username>', methods=['POST'])
#@require_privilege('force_change_password')
def force_change_password(username):
    user = db.get_user(username)
    if not user:
        abort(404)  # Not Found - User not exists

    data = request.get_json()
    new_password = data.get('new_password')

    db.update_user_password(username, new_password)
    return jsonify({'message': f'Password for user {username} changed by admin'})

