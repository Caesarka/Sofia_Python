from flask_restx import Namespace, fields
from models.user_model import UserRole

ns_user = Namespace("user", description="Users")

user_model = ns_user.model("User", {
    "id": fields.Integer(readonly=True),
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
    "reg_date": fields.String,
    "role": fields.String(enum=[role.value for role in UserRole]),
    "status": fields.String
})

auth_model = ns_user.model("Auth", {
    "email": fields.String(required=False),
    "password": fields.String(required=True),
})

update_model = ns_user.model("UserUpdate", {
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
})
