# app/decorators.py

from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import abort

def require_privilege(privilege):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user_role = current_user.get('role')

            if user_role is None or privilege not in ROLES.get(user_role, []):
                abort(403)  # Forbidden - User doesn't have the required privilege

            return func(*args, **kwargs)

        return wrapper
    return decorator