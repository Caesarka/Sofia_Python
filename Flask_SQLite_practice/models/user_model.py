from pydantic import BaseModel
import hashlib

class User(BaseModel):
    id: int | None = None
    name: str
    email: str
    password: str
    reg_date: str
    role: str
    status: str

    class Config:
        orm_mode = True
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()