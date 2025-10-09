import sqlite3
from pathlib import Path
from models.realty_model import Realty

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database.db"


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

def get_db():
    print(f"\nConnecting to DB at {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db_if_needed():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    database = get_db()
    database.executescript(SQL_SCHEMA)
    database.commit()
    database.close()



def create_realty(realty: Realty):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO realty (title, price, city, address, image) VALUES (?, ?, ?, ?, ?)",
            (realty.title, realty.price, realty.city, realty.address, realty.image)
        )
        realty.id = cursor.lastrowid
        db.commit()
    finally:
        db.close()

def get_realty(realty_id: int) -> Realty | None:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM realty WHERE id=?", (realty_id,))
        realty = cur.fetchone()
        print(realty)
        print(type(realty))
        if not realty:
            raise KeyError(f"Realty with id {realty_id} not found")
        return Realty.model_validate(dict(realty))
    finally:
        db.close()

    
def get_all_realties() -> list[Realty]:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM realty")
        rows = cur.fetchall()
        return [Realty.model_validate(dict(row)) for row in rows]
    finally:
        db.close()


def delete_realty(realty_id: int):
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("DELETE FROM realty WHERE id=?", (realty_id,))
        db.commit()
        return True if cur.rowcount != 0 else False 
    finally:
        db.close()
