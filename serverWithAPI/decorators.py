# app/decorators.py

from functools import wraps
from flask import request, abort
from . import ROLES

def require_privilege(privilege):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                abort(401)  # Unauthorized - Token not provided

            # In a real application, you would validate the token and get the user's role
            # For the sake of simplicity, let's assume the role is included in the token
            user_role = extract_user_role_from_token(token)

            if user_role is None or privilege not in ROLES.get(user_role, []):
                abort(403)  # Forbidden - User doesn't have the required privilege

            return func(*args, **kwargs)

        return wrapper
    return decorator

def extract_user_role_from_token(token):
    # In a real application, you would implement logic to extract the user's role from the token
    # For demonstration purposes, let's assume the role is included in the token as a header
    return request.headers.get('X-User-Role')
