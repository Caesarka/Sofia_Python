import sqlite3
from flask import g
from database.config import REALTY_DB_PATH, SCHEMA_SQL_REALTY

def get_db():
    if "realty_db" not in g:
        g.realty_db = sqlite3.connect(str(REALTY_DB_PATH))
        g.realty_db.row_factory = sqlite3.Row
    return g.realty_db

def close_db(e=None):
    realty_db = g.pop("realty_db", None)
    if realty_db is not None:
        realty_db.close()

def init_db_if_needed():
    REALTY_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    realty_db = sqlite3.connect(str(REALTY_DB_PATH))
    realty_db.executescript(SCHEMA_SQL_REALTY)
    realty_db.commit()
    realty_db.close()
