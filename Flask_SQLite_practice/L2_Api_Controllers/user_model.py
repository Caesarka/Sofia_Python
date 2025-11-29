from pydantic import BaseModel, Field
from datetime import datetime
import hashlib
#from enum import Enum


#class UserRole(str, Enum):
#    BUYER = "buyer"
#    REALTOR = "realtor"
#    ADMIN = "admin"
#
class UserAuth(BaseModel):
    id: int | None = None
    name: str
    email: str
    password: str
    reg_date: str = Field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    role: str
    status: str = 'active'


    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None


class UserCreate(BaseModel):
    id: int | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None
