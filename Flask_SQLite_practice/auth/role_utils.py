from functools import wraps
from flask import jsonify, request


def role_required(required_roles: list):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user:
                return {"message": "Unautorized"}, 401
            if user.get("role") not in required_roles:
                return {"message": "Forbidden: insufficient permissions"}, 403
            return f(*args, **kwargs)
        return wrapper
    return decorator