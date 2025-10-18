from flask_restx import Resource
from flask import request
from models.user_model import User
from api_models.user_api_model import ns_user, user_model, auth_model, update_model
import db

@ns_user.route("/register")
class Register(Resource):
    @ns_user.expect(user_model)
    def post(self):
        user = User.model_validate(request.json)
        db.register_user(user)
        return user.model_dump(), 201
    

@ns_user.route("/")
class UserList(Resource):
    @ns_user.expect(user_model)
    def get(self):
        users = db.get_all_users()
        return [user.model_dump() for user in users], 200

@ns_user.route("/login")
class Login(Resource):
    @ns_user.expect(auth_model)
    def post(self):
        data = request.json
        user = db.get_by_email(data.get("email"))
        if user and user.password == User.hash_password(data.get("password")):
            return {"message": f"Welcome {user.name}"}
        return {"message": "Invalid credentials"}, 401

@ns_user.route("/<int:user_id>")
class UserList(Resource):
    @ns_user.doc(responses={200: "No content"})
    def get(self, user_id):
        try:
            user = db.get_user(user_id)
            return user.model_dump(), 200
        except Exception:
            ns_user.abort(404, f"User with id={user_id} not found")

    @ns_user.doc(responses={200: "No content"})
    @ns_user.marshal_with(update_model)
    def put(self, user_id):
        user = User.model_validate(request.json)
        if user.id != user_id:
            ns_user.abort(400, f"User id does not match")
        try:
            db.update_user(user)
            return {}, 200
        except Exception:
            ns_user.abort(404, f"User not found")

    @ns_user.doc()
    def delete(self, user_id):
        try:
            is_deleted = db.delete_user(user_id)
            if is_deleted:
                return {'message': f'User with id {user_id} deleted'}, 200
            else:
                return {'message': f'User with id {user_id} not found'}, 403
        except Exception as e:
            return {'message': str(e)}, 500