from sqlite3 import IntegrityError
from flask_restx import Resource
from flask import jsonify, request, make_response
from L4_Data_Access import db_sql
from L4_Data_Access.orm.session import get_session
from L3_Business_Logic.user_service import UserService
from L2_Api_Controllers.schemas.user_model import UserAuth, UserCreate, UserLogin, UserUpdate
from L2_Api_Controllers.user_api_model import ns_user, user_model, auth_model, update_model
from .auth.utils import create_access_token
from .auth.jwt_utils import jwt_required
from pydantic import ValidationError

@ns_user.route("/register")
class Register(Resource):
    @ns_user.expect(user_model)
    def post(self):
        DBSession = get_session()
        try:
            user_data = request.json
            if not user_data:
                return {"message": "Missing JSON body"}, 400
            try:
                user_create = UserService(DBSession).register_user(user_data)

            except ValidationError as e:
                return {"message": "Invalid imput", "errors": e.errors()}, 422

            return user_create, 201
    
        except Exception as e:
            print("Unexpected error in registration:", e)
            return {"message": "Internal server error"}, 500
        finally:
            DBSession.close()


@ns_user.route("/")
class UserList(Resource):
    @ns_user.expect(user_model)
    def get(self):
        DBSession = get_session()
        users = UserService(DBSession).get_all_users()
        return users, 200


@ns_user.route("/login")
class Login(Resource):
    @ns_user.expect(auth_model)
    def post(self):
        DBSession = get_session()
        user_request = UserLogin.model_validate(request.json)
        print("Login attempt for:", user_request.email)
        user = UserService(DBSession).get_user_by_email(user_request.email)
        if user and user.password == UserAuth.hash_password(user_request.password):
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
        return {"message": "Invalid credentials"}, 401


@ns_user.route("/logout")
class Logout(Resource):
    @jwt_required
    def post(self):
        resp = make_response(jsonify({"message": "Logged out successfully"}, 200))
        resp.set_cookie("access_token", "", expires=0, httponly=True, samesite="Strict")
        return resp
    

@ns_user.route("/<int:user_id>")
class UserDetail(Resource):
    @jwt_required
    @ns_user.doc(responses={200: "No content"})
    def get(self, user_id):
        DBSession = get_session()
        user_id = request.user["user_id"]
        user = UserService(DBSession).get_user_by_id(user_id)
        if not user:
            return {"error": f"User with id={user_id} not found"}, 404
        user_auth = UserAuth.model_validate(user)
        return user_auth.model_dump(), 200

    @jwt_required
    @ns_user.doc(responses={200: "No content"})
    @ns_user.marshal_with(update_model)
    def put(self, user_id):
        try:
            DBSession = get_session()
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
            UserService(DBSession).update_user(update_data, user_id)
        except ValueError as e:
            ns_user.abort(409, f'Conflict data: {e}')
        except KeyError as e:
            ns_user.abort(404, f'User not found')
        except Exception as e:
            ns_user.abort(500, f'An unexcpected error occured! {e}')

        return {"message": "Profile updated"}, 200

#    @jwt_required
#    @ns_user.doc()
#    def delete(self, user_id):
#        try:
#            is_deleted = db_sql.delete_user_orm(user_id)
#            if is_deleted:
#                return {'message': f'User with id {user_id} deleted'}, 200
#            else:
#                return {'message': f'User with id {user_id} not found'}, 403
#        except Exception as e:
#            return {'message': str(e)}, 500
#        


@ns_user.route("/profile")
class UserProfile(Resource):
    @jwt_required
    def get(self):
        DBSession = get_session()
        user_id = request.user["user_id"]
        user = UserService(DBSession).get_user_by_id(user_id)
        if not user:
            return {"error": f"User with id={user_id} not found"}, 404
        user_auth = UserAuth.model_validate(user)
        return user_auth.model_dump(), 200

    @jwt_required
    @ns_user.expect(update_model)
    @ns_user.doc(responses={200: "Updated"})
    def put(self):
        try:
            DBSession = get_session()
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
            UserService(DBSession).update_user(update_data, user_id)
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
        DBSession = get_session()
        user_id = request.user["user_id"]
        is_deleted = UserService(DBSession).delete_user(user_id)

        if is_deleted:
            return {'message': f'User with id {user_id} deleted'}, 200
        else:
            return {'message': f'User with id {user_id} not found'}, 404
