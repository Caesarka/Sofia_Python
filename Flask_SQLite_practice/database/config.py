from pathlib import Path

BASE_DIR = Path(__file__).parent
REALTY_DB_PATH = BASE_DIR / "realty.db"
USER_DB_PATH = BASE_DIR / "user.db"
FAVORITE_DB_PATH = BASE_DIR / "favorite.db"

SCHEMA_SQL_REALTY = """
CREATE TABLE IF NOT EXISTS realty (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  price INTEGER NOT NULL,
  city TEXT NOT NULL,
  image TEXT,
  address TEXT NOT NULL
);
"""

SCHEMA_SQL_USER = """
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIGUE NOT NULL,
  password TEXT NOT NULL,
  email TEXT UNIGUE NOT NULL,
  reg_date TEXT DEFAULT CURRENT_TIMESTAMP,
  role TEXT DEFAULT 'user',
  status TEXT DEFAULT 'active'
"""

SCHEMA_SQL_FAVORITE = """
CREATE TABLE IF NOT EXISTS favorite (
  user_id INTEGER,
  realty_id INTEGER,
  PRIMARY KEY (user_id, realty_id),
  FOREIN KEY (user_id) REFERENCES user(id),
  FOREIN KEY (realty_id) REFERENCES realty(id)
"""



