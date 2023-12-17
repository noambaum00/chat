# app/__init__.py

from flask import Flask, jsonify, url_for
from flask_restful import Resource
from routes import  user_management, room_management
from flask_jwt_extended import JWTManager
from api_info import ApiInfo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key_for_demo_purposes'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key in production

jwt = JWTManager(app)

# Define user roles and associated privileges
ROLES = {
    'user': ['read_messages', 'send_messages', 'add_rooms','see_room', 'change_password'],
    'admin': ['read_messages', 'send_messages', 'manage_users', 'manage_rooms', 'start_service', 'close_service', 'force_change_password'],
}

# Register blueprints
app.register_blueprint(user_management, url_prefix='/api')
app.register_blueprint(room_management, url_prefix='/api')

Api.add_resource(ApiInfo, '/api/info', endpoint='api_info')

if __name__ == '__main__':
    app.run(debug=True)
    print(app.url_map.iter_rules())
