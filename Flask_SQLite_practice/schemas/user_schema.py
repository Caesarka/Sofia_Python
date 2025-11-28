from pydantic import BaseModel, Field
from sqlalchemy import DateTime, String, Enum, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
import hashlib
#from enum import Enum

from models.index import Base

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

    #class Config:
    #    orm_mode = True
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None

    #class Config:
    #    orm_mode = True

class UserCreate(BaseModel):
    id: int | None = None
    name: str | None = None
    email: str | None = None
    password: str | None = None
    role: str | None = None

    #class Config:
    #    orm_mode = True

class UserORM(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(Text, nullable=False)
    
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    
    password: Mapped[str] = mapped_column(Text, nullable=False)
    
    # TODO datetime DateTime(timezone=True)
    reg_date: Mapped[str] = mapped_column(Text, default=lambda: datetime.now(timezone.utc), server_default=func.now())
    
    role: Mapped[str] = mapped_column(Text, nullable=False)
    #role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    
    status: Mapped[str] = mapped_column(Text, default='active')
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', role='{self.role}')>"
    

class RealtyORM(Base):
    __tablename__ = 'realty'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(Text, nullable=False)
    
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    
    password: Mapped[str] = mapped_column(Text, nullable=False)
    
    # TODO datetime DateTime(timezone=True)
    reg_date: Mapped[str] = mapped_column(Text, default=lambda: datetime.now(timezone.utc), server_default=func.now())
    
    role: Mapped[str] = mapped_column(Text, nullable=False)
    #role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    
    status: Mapped[str] = mapped_column(Text, default='active')
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', role='{self.role}')>"