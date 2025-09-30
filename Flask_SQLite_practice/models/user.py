from dataclasses import dataclass
from flask_restx import Namespace, fields

ns_user = Namespace("user", description="Users")


user_model = ns_user.model("User", {
    "id": fields.Integer(readonly=True),
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
    "reg_date": fields.String,
    "role": fields.String,
    "status": fields.String,
})

auth_model = ns_user.model("Auth", {
    "name": fields.String(required=False),
    "email": fields.String(required=False),
    "password": fields.String(required=True),
})

update_model = ns_user.model("UserUpdate", {
    "name": fields.String,
    "email": fields.String,
    "password": fields.String,
})



#@dataclass(slots=True)
class User:
    id: int
    name: str
    password: str
    email: str
    reg_date: str
    role: str
    status: str

    def __init__(self, dictData: dict = {}):
        if not dictData:
            dictData = {}
        print(dictData)
        self.id = dictData.get("id", None)
        self.name = dictData.get("name", None)
        self.password = dictData.get("password", None)
        self.email = dictData.get("email", None)
        self.reg_date = dictData.get("reg_date", None)
        self.role = dictData.get("role", None)
        self.status = dictData.get("status", None)

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
        "password": self.password,
        "email": self.email,
        "reg_date": self.reg_date,
        "role": self.role,
        "status": self.status
        }
        return data
    
