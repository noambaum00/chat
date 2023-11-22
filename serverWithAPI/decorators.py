# app/decorators.py

from functools import wraps
from flask import request, abort
from . import ROLES
import jwt

SECRET_KEY = 'your_secret_key'  # Replace with your secret key

def generate_token(username, role):
    payload = {
        'username': username,
        'role': role
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('utf-8')

def extract_user_role_from_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('role')
    except jwt.ExpiredSignatureError:
        abort(401)  # Unauthorized - Token has expired
    except jwt.InvalidTokenError:
        abort(401)  # Unauthorized - Invalid token
