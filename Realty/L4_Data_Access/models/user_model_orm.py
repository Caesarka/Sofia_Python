from sqlalchemy import String, Enum, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import List
#from enum import Enum
from .index import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .realty_model_orm import RealtyORM


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

    realty: Mapped[List["RealtyORM"]] = relationship("RealtyORM", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}', role='{self.role}')>"