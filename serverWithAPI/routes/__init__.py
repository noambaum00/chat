# app/routes/__init__.py

from flask import Blueprint

user_management = Blueprint('user_management', __name__)
room_management = Blueprint('room_management', __name__)

from . import messages, user_management, room_management
