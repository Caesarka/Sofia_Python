import sqlite3
import os
from pathlib import Path
from schemas.realty_schema import Realty, RealtyPatch
from schemas.user_schema import UserAuth, UserUpdate, UserORM



from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from db.orm.session import get_session


BASE_DIR = Path(__file__).parent
print(f"v1 BASE_DIR in db_sql.py: {BASE_DIR}")
DB_PATH = Path(os.getenv("DB_PATH", BASE_DIR / "database.db"))
print(f"v1 DB_PATH in db_sql.py: {DB_PATH}")

SQL_SCHEMA = """
CREATE TABLE IF NOT EXISTS realty (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  title TEXT NOT NULL,
  price INTEGER NOT NULL,
  city TEXT NOT NULL,
  image TEXT,
  address TEXT NOT NULL,
  created_at TEXT,
  published_at TEXT,
  status INT DEFAULT 0,
  user_id INTEGER NOT NULL,
  is_deleted INT DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  reg_date TEXT DEFAULT CURRENT_TIMESTAMP NOT NULL,
  role TEXT NOT NULL,
  status TEXT NOT NULL
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


# realty
def create_realty(realty: Realty):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO realty (title, price, city, address, image, created_at, status, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (realty.title, realty.price, realty.city, realty.address, realty.image, realty.created_at, realty.status, realty.user_id)
        )
        realty.id = cursor.lastrowid
        db.commit()
    finally:
        db.close()
    return realty


def get_realty(realty_id: int, filter: str = '') -> Realty | None:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute(f"SELECT * FROM realty WHERE id=? {filter}", (realty_id,))
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


def get_all_active_realties() -> list[Realty]:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM realty WHERE status=1")
        rows = cur.fetchall()
        return [Realty.model_validate(dict(row)) for row in rows]
    finally:
        db.close()


def get_all_realties_realtor(user_id) -> list[Realty]:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM realty WHERE status=1 OR user_id=?", (user_id,))
        rows = cur.fetchall()
        return [Realty.model_validate(dict(row)) for row in rows]
    finally:
        db.close()


def replace_realty(realty: Realty, realty_id: int):
    update_data = realty.model_dump()
    if not update_data:
        return
    db = get_db()
    try:
        update_data["id"] = realty_id
        cur = db.cursor()
        set_clause = ", ".join(f"{key}=?" for key in update_data.keys())
        values = list(update_data.values())
        #values["realty_id"] = realty_id
        #values.append(realty_id)
        cur.execute(f"UPDATE realty SET {set_clause} WHERE id={realty_id}", values)
        db.commit()
    finally:
        db.close()

def patch_realty(realty: RealtyPatch, realty_id: int):
    update_data = realty.model_dump(exclude_none=True)
    if not update_data:
        return
    db = get_db()
    try:
        cur = db.cursor()
        set_clause = ", ".join(f"{key}=?" for key in update_data.keys())
        values = list(update_data.values())
        values.append(realty_id)
        cur.execute(f"UPDATE realty SET {set_clause} WHERE id=?", values)
        db.commit()
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