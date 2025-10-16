from pydantic import BaseModel

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