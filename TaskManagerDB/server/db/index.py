from sqlalchemy import create_engine
from model import Base

database_url = "sqlite:///./to_do_data.db"
engine = create_engine(database_url)

def create_database_and_tables():
    print("Tables creating...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

if __name__ == "__main__":
    create_database_and_tables()