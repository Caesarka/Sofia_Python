import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
# from pathlib import Path

from flask import g

from models import Base

BASE_DIR = Path(__file__).resolve().parent.parent
print(f"v2 BASE_DIR: {BASE_DIR}")

# DB_PATH = BASE_DIR / "database.db"
db_path_env = os.getenv("DB_PATH", "database.db")
print(f"v2 DB_PATH env variable: {db_path_env}")

DB_PATH = (BASE_DIR / db_path_env).resolve()
print(f"v2 Resolved DB_PATH: {DB_PATH}")

DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
print(f"v2 Database URL: {DATABASE_URL}")

#DB_PATH = os.getenv("DB_PATH", BASE_DIR / "database.db")
#DATABASE_URL = f"sqlite://{DB_PATH}"
#
engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(engine, class_=Session, expire_on_commit=False)

def get_session() -> Session:
    if 'db_session' not in g:
        g.db_session = session_factory()
    
    return g.db_session
  

def init_db_if_needed_v2() -> None:
    try:
        print("Create tables if not exists...")
        Base.metadata.create_all(engine)
        print("Tables creates succsesfully")
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def close_db_session(exception=None) -> None:
    session = g.pop('db_session', None)
    
    if session:
        try:
            if not exception:
                session.commit()
            else:
                session.rollback()
        except SQLAlchemyError as e:
            session.rollback()
        finally:
            session.close()