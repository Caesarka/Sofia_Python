from functools import wraps
from flask import jsonify, request


def role_required(required_role: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user:
                return jsonify({"message": "Unautorized"}), 401
            if user.get("role") != required_role:
                return jsonify({"message": "Forbidden: insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorator