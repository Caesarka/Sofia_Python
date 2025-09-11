from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session


database_url = "sqlite:///./to_do_data.db"
engine = create_engine(database_url)

session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db_session():
    if 'db_session' not in g:
        g.db_session = session_factory()
    return g.db_session

def close_db_session(exception=None):
    session = g.pop("db_session", None)
    if session is not None:
        session.close()

def init_app(app):
    app.teardown_appcontext(close_db_session)