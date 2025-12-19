from pydantic import BaseModel, Field
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, String, Enum, Boolean, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from .index import Base


if TYPE_CHECKING:
    from .user_model_orm import UserORM


class RealtyORM(Base):
    __tablename__ = 'realty'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    title: Mapped[str] = mapped_column(Text, nullable=False)
    
    price: Mapped[int] = mapped_column(nullable=False)
    
    city: Mapped[str] = mapped_column(Text, nullable=False)

    address: Mapped[str] = mapped_column(Text, nullable=False)

    image: Mapped[str] = mapped_column(Text, nullable=False)

    # TODO datetime DateTime(timezone=True)
    created_at: Mapped[str] = mapped_column(Text, default=lambda: datetime.now(timezone.utc), server_default=func.now())

    #published_at: Mapped[str | None] = mapped_column(Text, default=lambda: datetime.now(timezone.utc), server_default=func.now())
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, server_default=func.now())
    status: Mapped[str] = mapped_column(Text, default='inactive')
    #role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    
    is_deleted: Mapped[bool] = mapped_column(default=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="realty")

    def __repr__(self) -> str:
        return f"<Realty(id={self.id}, title='{self.title}', address='{self.address}')>"
    
