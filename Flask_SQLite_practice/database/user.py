import sqlite3
from flask import g
from database.config import USER_DB_PATH, SCHEMA_SQL_USER

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(str(USER_DB_PATH))
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db_if_needed():
    USER_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(USER_DB_PATH))
    db.executescript(SCHEMA_SQL_USER)
    db.commit()
    db.close()
