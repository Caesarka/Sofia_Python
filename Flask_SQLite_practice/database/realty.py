import sqlite3
import database.config as config
from pathlib import Path

SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS realty (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  price INTEGER NOT NULL,
  city TEXT NOT NULL,
  image TEXT,
  address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  reg_date TEXT DEFAULT CURRENT_TIMESTAMP,
  role TEXT DEFAULT 'user',
  status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS favorite (
  user_id INTEGER,
  realty_id INTEGER,
  PRIMARY KEY (user_id, realty_id),
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (realty_id) REFERENCES realty(id)
);
"""

#__realty_db_conn = None

def get_db():
    print(f"\nConnecting to DB at {config.DB_PATH}")
    db = sqlite3.connect(str(config.DB_PATH))
    db.row_factory = sqlite3.Row
    return db

#def close_db(e=None):
#    global __realty_db_conn
#    if __realty_db_conn is not None:
#        print("\nClosing DB")
#        __realty_db_conn.close()
#        __realty_db_conn = None

def init_db_if_needed():
    Path(config.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    realty_db = get_db()
    realty_db.executescript(SQL_SCHEMA)
    realty_db.commit()
    realty_db.close()
