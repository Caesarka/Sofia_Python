import sqlite3
import os
from pathlib import Path

from L5_Database.database_schema import SQL_SCHEMA


BASE_DIR = Path(__file__).parent.parent
print(f"v1 BASE_DIR in db_sql.py: {BASE_DIR}")
DB_PATH = Path(os.getenv("DB_PATH", BASE_DIR / "database.db"))
print(f"v1 DB_PATH in db_sql.py: {DB_PATH}")

def get_db():
    print(f"\nv1 Connecting to DB at {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db_if_needed_v1():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    database = get_db()
    database.executescript(SQL_SCHEMA)
    database.commit()
    database.close()