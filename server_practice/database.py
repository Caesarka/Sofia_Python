from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.model import Base

database_url = "sqlite:///./realty.db"
engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=True)