import sqlite3
from flask import g
from database.config import USER_DB_PATH, SCHEMA_SQL_USER

def get_db():
    if "user_db" not in g:
        g.user_db = sqlite3.connect(str(USER_DB_PATH))
        g.user_db.row_factory = sqlite3.Row
    return g.user_db

def close_db(e=None):
    user_db = g.pop("user_db", None)
    if user_db is not None:
        user_db.close()

def init_db_if_needed():
    USER_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("User DB path:", USER_DB_PATH.resolve())
    user_db = sqlite3.connect(str(USER_DB_PATH))
    try:
        user_db.executescript(SCHEMA_SQL_USER)
        user_db.commit()
        print("Tables created/checked successfully in user.db")
    except Exception as e:
        print("Error creating tables in user.db:", e)
    finally:
        user_db.close()