from sqlalchemy import Table, Column, ForeignKey
from .index import Base

favorite_table = Table(
    "favorite",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("realty_id", ForeignKey("realty.id"), primary_key=True),
)