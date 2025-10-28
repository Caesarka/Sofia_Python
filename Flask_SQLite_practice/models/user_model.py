from pydantic import BaseModel, Field
from datetime import datetime
import hashlib

class User(BaseModel):
    id: int | None = None
    name: str
    email: str
    password: str
    reg_date: str = Field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    role: str
    status: str

    class Config:
        orm_mode = True
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()