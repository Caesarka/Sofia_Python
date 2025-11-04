from datetime import datetime
from pydantic import BaseModel, Field

class Realty(BaseModel):
    
    id: int | None = None
    title: str
    price: float
    city: str
    address: str
    image: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    status: int = 0
    user_id: int

    class Config:
        orm_mode = True

class RealtyUpdate(BaseModel):
    
    id: int | None = None
    title: str
    price: float
    city: str
    address: str
    image: str | None = None
    status: str | None = None

    class Config:
        orm_mode = True