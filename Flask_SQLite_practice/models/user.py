from dataclasses import dataclass
from flask_restx import Namespace, fields

ns = Namespace("user", description="Users")


user_model = ns.model("User", {
    "id":   fields.Integer(readonly=True, description="ID"),
    "name": fields.String(required=True, description="Name"),
    "password": fields.String(required=True, description="Password"),
    "email":  fields.String(required=True, description="Email"),
    "reg_date":  fields.String(required=True, description="Date of registration"),
    "role":  fields.String(required=True, description="Role"),
    "status":  fields.String(required=True, description="Status"),
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
        
    
