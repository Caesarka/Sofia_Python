from pydantic import BaseModel
import hashlib
from enum import Enum

class UserRole(str, Enum):
    BUYER = "buyer"
    REALTOR = "realtor"
    ADMIN = "admin"

class UserAuth(BaseModel):
    id: int | None = None
    name: str
    email: str
    password: str
    reg_date: str
    role: UserRole = UserRole.BUYER
    status: str

    class Config:
        orm_mode = True
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

    class Config:
        orm_mode = True

