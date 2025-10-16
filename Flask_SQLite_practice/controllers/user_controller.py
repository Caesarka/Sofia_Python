## SYSTEM
#from flask import request, session
#from flask_restx import Resource
#
## PROJECT
#from models.user_model import UserModel
#from api_models.user_api_model import ns_user, auth_model, user_model, update_model
#
#from werkzeug.exceptions import Conflict
#
#@ns_user.route("/")
#class UserRegister(Resource):
#    @ns_user.expect(user_model, validate=True)
#    @ns_user.marshal_with(user_model, code=201)
#    def post(self):
#        data = self.api.payload
#        try:
#            new_user = create_user(data=data)
#        except Conflict as e:
#            raise ns_user.abort(409, str(e))
#        except Exception as e:
#            raise ns_user.abort(500, str(e))
#        
#
#        return new_user.to_dict(), 201
#
#    def get(self):
#        uid = session.get("user_id")
#        if not uid:
#            return {"message": "Not logged in"}, 401
#        user = execute_data("get_user", {"id": uid}, fetch="one")
#        if user is None:
#            return {"message": "User not found"}, 404
#        return user.to_dict()
#
#    @ns_user.expect(update_model)
#    def patch(self):
#        uid = session.get("user_id")
#        if not uid:
#            return {"message": "Not logged in"}, 401
#        data = request.json
#        data["id"] = uid
#        execute_data("update_user", data, fetch="none")
#        return {"message": "User updated"}
#    
#    def delete(self):
#        uid = session.get("user_id")
#        if not uid:
#            return {"message": "Not logged in"}, 401
#        execute_data("delete_user", {"id": uid}, fetch="none")
#        session.clear()
#        return {"message": "User deleted"}
#
#@ns_user.route("/auth")
#class UserAuth(Resource):
#    @ns_user.expect(auth_model)
#    def post(self):
#        data = self.api.payload
#        user = execute_data("check_user_pass", data, fetch="one")
#        if not user:
#            return {"message": "Invalid credentials"}, 401
#        session["user_id"] = user.id
#        return {"message": "Logged in", "id": user.id}
#
#@ns_user.route("/logout")
#class UserLogout(Resource):
#    def post(self):
#        session.clear()
#        return {"message": "Logged out"}
from flask_restx import Resource
from flask import request
from models.user_model import User
from api_models.user_api_model import ns_user, auth_model, user_model

@ns_user.route("/register")
class Register(Resource):
    @ns_user.expect(auth_model)
    def post(self):
        data = request.json
        user = User.create(data.get("name"), data.get("email"), data.get("password"))
        return user.to_dict(), 201

@ns_user.route("/login")
class Login(Resource):
    @ns_user.expect(auth_model)
    @ns_user.marshal_with(user_model)
    def post(self):
        data = request.json
        user = User.get_by_email(data.get("email"))
        if user and user.password == User.hash_password(data.get("password")):
            return {"message": f"Welcome {user.name}"}
        return {"message": "Invalid credentials"}, 401
