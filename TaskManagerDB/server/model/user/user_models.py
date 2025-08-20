from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"ID(id={self.id!r}, user_name={self.user_name!r}, password={self.password!r})"
'''
def setup_User_db(engine):
    declarative_base().metadata.create_all(engine)
'''