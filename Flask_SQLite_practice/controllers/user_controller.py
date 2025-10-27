from sqlite3 import IntegrityError
from flask_restx import Resource
from flask import request, make_response
from models.user_model import UserAuth, UserUpdate, UserRole
from api_models.user_api_model import ns_user, user_model, auth_model, update_model
import db
from auth.utils import create_access_token
from auth.jwt_utils import jwt_required
from pydantic import ValidationError

@ns_user.route("/register")
class Register(Resource):
    @ns_user.expect(user_model)
    def post(self):
        try:
            user_data = request.json
            if not user_data:
                return {"message": "Missing JSON body"}, 400
            try:
                user = UserAuth.model_validate(user_data)
            except ValidationError as e:
                return {"message": "Invalid imput", "errors": e.errors()}, 422
        
            if user == UserRole.ADMIN:
                return ns_user.abort(409, "Permission error")
        
            db.register_user(user)
            return user.model_dump(), 201
    
        except Exception as e:
            print("Unexpected error in registration:", e)
            return {"message": "Internal server error"}, 500


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
        if user and user.password == UserAuth.hash_password(data.get("password")):
            access_token = create_access_token({"user_id": user.id, "role": user.role})
            resp = make_response({"message": f"Welcome {user.name}"})
            resp.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                samesite="Strict",
                max_age=60*60*24
            )
            return resp
            #return {"access token": access_token}, 200
        return {"message": "Invalid credentials"}, 401


@ns_user.route("/<int:user_id>")
class UserList(Resource):
    @jwt_required
    @ns_user.doc(responses={200: "No content"})
    def get(self, user_id):
        try:
            user = db.get_user(user_id)
            return user.model_dump(), 200
        except Exception:
            ns_user.abort(404, f"User with id={user_id} not found")

    @jwt_required
    @ns_user.doc(responses={200: "No content"})
    @ns_user.marshal_with(update_model)
    def put(self, user_id):
        user = UserAuth.model_validate(request.json)
        if user.id != user_id:
            ns_user.abort(400, f"User id does not match")
        try:
            db.update_user(user)
            return {}, 200
        except Exception:
            ns_user.abort(404, f"User not found")

    @jwt_required
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
        


@ns_user.route("/profile")
class UserProfile(Resource):
    @jwt_required
    def get(self):
        user_id = request.user["user_id"]
        try:
            user = db.get_user(user_id)
            return user.model_dump(), 200
        except Exception:
            ns_user.abort(404, f"User with id={user_id} not found")

    @jwt_required
    @ns_user.expect(update_model)
    @ns_user.doc(responses={200: "Updated"})
    def put(self):
        try:
            user_id = request.user["user_id"]
        except Exception as e:
            ns_user.abort(401, f'Invalid or missing token: {e}')

        json_data = request.json
        if not json_data:
            ns_user.abort(400, "Missing JSON body")
        try:
            update_data = UserUpdate.model_validate(json_data, strict=False)
        except ValidationError as e:
            ns_user.abort(422, f'Invalid data: {e.errors}')
        
        if update_data.password:
            update_data.password = UserAuth.hash_password(update_data.password)
        
        try:
            db.update_user(update_data, user_id)
        except ValueError as e:
            ns_user.abort(409, f'Conflict data: {e}')
        except KeyError as e:
            ns_user.abort(404, f'User not found')
        except Exception as e:
            ns_user.abort(500, f'An unexcpected error occured! {e}')

        return {"message": "Profile updated"}, 200
    
    @jwt_required
    @ns_user.doc()
    def delete(self):
        try:
            user_id = request.user["user_id"]
            is_deleted = db.delete_user(user_id)
            if is_deleted:
                return {'message': f'User with id {user_id} deleted'}, 200
            else:
                return {'message': f'User with id {user_id} not found'}, 403
        except Exception as e:
            return {'message': str(e)}, 500