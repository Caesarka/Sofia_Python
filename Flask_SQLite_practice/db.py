import sqlite3
from pathlib import Path
from models.realty_model import Realty
from models.user_model import UserAuth, UserUpdate

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


# realty
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


def update_realty(realty: Realty):
    if realty.id <= 0 | realty.id == None | type(realty.id) != int:
        raise KeyError(f"Realty does not have id specified")
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("UPDATE realty SET title=?, price=?, city=?, address=?, image=? WHERE id=? ", (realty.title, realty.price, realty.city, realty.address, realty.image, realty.id))
        if cur.rowcount == 0:
            raise KeyError(f"Realty with id {realty.id} does not exist")

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



# user
def register_user(user: UserAuth):
    db = get_db()
    pw_hash = UserAuth.hash_password(user.password)
    user.password = pw_hash
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (name, email, password, reg_date, role, status) VALUES (?, ?, ?, ?, ?, ?)",
            (user.name, user.email, user.password, user.reg_date, user.role, user.status)
        )
        user.id = cursor.lastrowid
        db.commit()
    
    except sqlite3.IntegrityError as e:
        db.rollback()
        raise ValueError(f"User with this email already exists: {e}")

    except sqlite3.Error as e:
        db.rollback()
        raise RuntimeError(f"Database error: {e}")

    finally:
        db.close()

def get_by_email(email: str):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        print(user)
        if not user:
            raise KeyError(f"User with email {email} not found")
        return UserAuth.model_validate(dict(user))
    finally:
        db.close()


def get_user(user_id: int) -> UserAuth | None:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM user WHERE id=?", (user_id,))
        user = cur.fetchone()
        print(user)
        print(type(user))
        if not user:
            raise KeyError(f"User with id {user_id} not found")
        return UserAuth.model_validate(dict(user))
    finally:
        db.close()


def get_all_users() -> list[UserAuth]:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()
        return [UserAuth.model_validate(dict(row)) for row in rows]
    finally:
        db.close()


def update_user(user: UserUpdate, user_id) -> None:
    if user_id <= 0 | user_id == None | type(user_id) != int:
        raise KeyError(f"User does not have id specified")
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("UPDATE user SET name=?, email=?, password=? WHERE id=?", (user.name, user.email, user.password, user_id))
        if cur.rowcount == 0:
            raise KeyError(f"User does not exist")

        db.commit()
        return UserUpdate.model_validate(dict(user))
    except Exception as e:
        raise ValueError(f'Data conflict: {e}')
    finally:
        db.close()


def delete_user(user_id: int):
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("UPDATE user SET status=? WHERE id=?", ("inactive", user_id,))
        db.commit()
        return True if cur.rowcount != 0 else False
    finally:
        db.close()