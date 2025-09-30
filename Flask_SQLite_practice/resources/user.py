# SYSTEM
from flask import request, session
from flask_restx import Resource

# PROJECT
from models.user import ns_user, user_model, auth_model, update_model
from database.realty import get_db
from models.user import User
from utils.utils import row_to_dict
from services.user.sql import create, execute_data


@ns_user.route("/")
class UserRegister(Resource):
    @ns_user.expect(user_model, validate=True)
    @ns_user.marshal_with(user_model, code=201)
    def post(self):
        data = self.api.payload
        user = execute_data("create_user", data)
        return user.to_dict(), 201

    def get(self):
        uid = session.get("user_id")
        if not uid:
            return {"message": "Not logged in"}, 401
        user = execute_data("get_user", {"id": uid}, fetch="one")
        if user is None:
            return {"message": "User not found"}, 404
        return user.to_dict()

    @ns_user.expect(update_model)
    def patch(self):
        uid = session.get("user_id")
        if not uid:
            return {"message": "Not logged in"}, 401
        data = request.json
        data["id"] = uid
        execute_data("update_user", data, fetch="none")
        return {"message": "User updated"}
    
    def delete(self):
        uid = session.get("user_id")
        if not uid:
            return {"message": "Not logged in"}, 401
        execute_data("delete_user", {"id": uid}, fetch="none")
        session.clear()
        return {"message": "User deleted"}

@ns_user.route("/auth")
class UserAuth(Resource):
    @ns_user.expect(auth_model)
    def post(self):
        data = self.api.payload
        user = execute_data("check_user_pass", data, fetch="one")
        if not user:
            return {"message": "Invalid credentials"}, 401
        session["user_id"] = user.id
        return {"message": "Logged in", "id": user.id}

@ns_user.route("/logout")
class UserLogout(Resource):
    def post(self):
        """Разлогиниться"""
        session.clear()
        return {"message": "Logged out"}

