from pydantic import BaseModel
import datetime

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



from pydantic import BaseModel

class Realty(BaseModel):
    
    id: int | None = None
    title: str
    price: float
    city: str
    address: str
    image: str | None = None

    class Config:
        orm_mode = True