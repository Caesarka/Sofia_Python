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