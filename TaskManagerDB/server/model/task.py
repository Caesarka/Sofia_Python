from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .index import Base

class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    priority: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"ID(id={self.id!r}, title={self.title!r}, description={self.description!r}, status={self.status!r}, priority={self.priority!r})"

