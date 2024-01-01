# app/__init__.py

from . import defines
from flask import Flask, jsonify, url_for
from flask_restful import Resource
from flask_jwt_extended import JWTManager

defines.init()
defines.app = Flask(__name__)
defines.app.config['SECRET_KEY'] = 'secret_key_for_demo_purposes'
defines.app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a secure key in production

defines.jwt = JWTManager(defines.app)

# Import and register blueprints
from .routes import room_management, user_management

# Register blueprints
defines.app.register_blueprint(room_management, url_prefix='/api/room_management')  # Change the url_prefix if needed
defines.app.register_blueprint(user_management, url_prefix='/api/user_management')  # Change the url_prefix if needed

if __name__ == '__main__':
    defines.app.run(debug=True)
    print(defines.app.url_map.iter_rules())
