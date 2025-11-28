import sqlite3
import os
from pathlib import Path
from L5_Database.database_schema import SQL_SCHEMA
from L2_Api_Controllers.realty_model import Realty, RealtyPatch
from L2_Api_Controllers.user_model import UserAuth, UserUpdate, UserORM



from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from db.session import get_session


BASE_DIR = Path(__file__).parent
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


#def publish_realty(realty: Realty):
#    db = get_db()
#    
#    try:
#        cur = db.cursor()
#        cur.execute("UPDATE realty SET status=1, created_at=?", (realty.created_at,))
#        db.commit()
#    finally:
#        db.close()

# user

def register_user(session: Session, user_data: dict):
    stmt = insert(UserORM).values(**user_data).returning(UserORM)
    result = session.execute(stmt)
    user = result.scalar_one()
    session.commit()
    return user

def get_by_email_orm(session: Session, email: str):
    result = session.execute(select(UserORM).where(UserORM.email == email))
    data = result.scalar_one_or_none()
    return data

def register_user_sql(user: UserAuth):
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