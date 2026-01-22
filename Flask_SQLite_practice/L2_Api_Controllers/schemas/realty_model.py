from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Realty(BaseModel):
    

    title: str
    price: float
    city: str
    address: str
    image: str |None = None
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    published_at: Optional[datetime] = None
    status: str | None = 'inactive'
    user_id: int
    is_deleted: int = 0
    id: int | None = None
    
    #class Config:
    #    orm_mode = True

class RealtyPatch(BaseModel):
    
    title: Optional[str] = None
    price: Optional[float] = None
    city: Optional[str] = None
    address: Optional[str] = None
    image: Optional[str] = None
    status: Optional[int] = None
    is_deleted: Optional[int] = None
    published_at: Optional[str] = None

    #class Config:
    #    orm_mode = True