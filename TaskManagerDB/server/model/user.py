from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .index import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"ID(id={self.id!r}, user_name={self.user_name!r}, password={self.password!r})"
