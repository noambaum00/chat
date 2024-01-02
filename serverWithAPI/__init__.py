# app/__init__.py

from . import defines
from flask import Flask, jsonify, url_for
from flask_restful import Resource
from flask_jwt_extended import JWTManager
from mongoDBnew import ChatDB

defines.init()
defines.app = Flask(__name__)
defines.app.config['SECRET_KEY'] = '8bce79858b4c431a195654743417ddaa437b7b1b08da9f6bd3336ca0192188a6'
defines.app.config['JWT_SECRET_KEY'] = '97675bc0bbf3960f40071b30b9cbc18a50cf259622dbbfc5b478ee2198bc7e1e'  # Change this to a secure key in production- done

defines.jwt = JWTManager(defines.app)

# Import and register blueprints
from .routes.user_management import user_blueprint
from .routes.room_management import room_blueprint
from .api_info import info_blueprint

# Register blueprints
defines.app.register_blueprint(room_blueprint)
defines.app.register_blueprint(user_blueprint)
defines.app.register_blueprint(info_blueprint)

defines.db = ChatDB()

def run(debug):
    defines.app.run(debug=True)
    print(defines.app.url_map.iter_rules())
   


if __name__ == '__main__':
    defines.app.run(debug=True)
    print(defines.app.url_map.iter_rules())
