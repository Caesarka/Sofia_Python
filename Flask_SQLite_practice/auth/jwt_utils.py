from functools import wraps
from flask import jsonify, request
from .utils import decode_access_token


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        token = request.cookies.get("access_token")
        if not token:
            return {"message": "Missing token"}, 401
        #auth_header = request.headers.get("Authorization", None)
        #if not auth_header:
        #    return jsonify({"message": "Missing authorization header"}), 401
        #
        #parts = auth_header.split()
        #if len(parts) != 2 or parts[0].lower() != "bearer":
        #    return jsonify({"message": "Invalid authorization header"}), 401
        #
        #token = parts[1]
        try:
            payload = decode_access_token(token)
            request.user = payload
        except ValueError as e:
            return {"message": str(e)}, 401
        
        return f(*args, **kwargs)
    return decorated
