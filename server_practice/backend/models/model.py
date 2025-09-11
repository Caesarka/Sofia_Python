from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class RealtyModel(Base):
    __tablename__ = "realty"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    city = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "city": self.city,
        }