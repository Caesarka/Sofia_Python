import sqlite3
import os
from pathlib import Path
from db.sql.session import get_db
from schemas.realty_schema import Realty, RealtyPatch
from schemas.user_schema import UserAuth, UserUpdate, UserORM

from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from db.orm.session import get_session

class Auth:
    def __init__(self, session):
      self.session = session
      
    def register_user(self, user_data: UserAuth):
        stmt = insert(UserORM).values(**user_data).returning(UserORM)
        result = self.session.execute(stmt)
        user = result.scalar_one()
        self.session.commit()
        return user

    def get_by_email(self, email: str):
        result = self.session.execute(select(UserORM).where(UserORM.email == email))
        data = result.scalar_one_or_none()
        return data



def register_user(self, user: UserAuth):
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


def get_by_email(self, email: str):
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

def delete_user(user_id: int):
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("UPDATE user SET status=? WHERE id=?", ("inactive", user_id,))
        db.commit()
        return True if cur.rowcount != 0 else False
    finally:
        db.close()
