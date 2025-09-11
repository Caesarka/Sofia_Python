from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "realty.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS realty (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  price INTEGER NOT NULL,
  city TEXT NOT NULL
);
"""