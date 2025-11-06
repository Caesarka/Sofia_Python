from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

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
    is_deleted: int = 0

    class Config:
        orm_mode = True

class RealtyPatch(BaseModel):
    
    title: Optional[str] = None
    price: Optional[float] = None
    city: Optional[str] = None
    address: Optional[str] = None
    image: Optional[str] = None
    status: Optional[int] = None
    is_deleted: Optional[int] = None

    class Config:
        orm_mode = True