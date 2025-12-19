import sqlite3
import os
from pathlib import Path
from sqlalchemy import update

from L4_Data_Access.sql.session import get_db
from .models.user_model_orm import UserORM
from .models.realty_model_orm import RealtyORM
from L5_Database.database_schema import SQL_SCHEMA
from L2_Api_Controllers.schemas.realty_model import Realty, RealtyPatch
from L2_Api_Controllers.schemas.user_model import UserAuth, UserUpdate
from sqlalchemy import delete, select, insert
from sqlalchemy.orm import Session


# realty
    
def create_realty_orm(session: Session,  realty: dict):
    try:
        new_realty = RealtyORM(**realty)
        session.add(new_realty)
        session.commit()

    except Exception as e:
        session.rollback()
        raise
        raise ValueError(f"Error creating realty: {e}")
    return new_realty

def get_realty_orm(session: Session, realty_id: int, filter: str = '') -> RealtyORM | None:
    try:
        result = session.execute(select(RealtyORM).where(RealtyORM.id == realty_id))
        realty = result.scalar_one_or_none()
        return realty
    except Exception as e:
        raise ValueError(f"Error retrieving realty: {e}")

def patch_realty_orm(session: Session, realty: RealtyPatch, realty_id: int):
    update_data = realty.model_dump(exclude_none=True)
    if not update_data:
        return
    try:
        result = session.execute(update(RealtyORM).where(RealtyORM.id == realty_id).values(**update_data).execution_options(synchronize_session="fetch"))
        session.commit()
        if result.rowcount == 0:
            raise KeyError(f"Realty does not exist")
    except Exception as e:
        session.rollback()
        raise ValueError(f"Error updating realty: {e}")

def get_my_active_realties_orm(session: Session, user_id: int, filters: list) -> list[RealtyORM]:
    try:
        result = session.execute(select(RealtyORM).where(*filters))
        realties = result.scalars().all()
        return realties
    except Exception as e:
        raise ValueError(f"Error retrieving realty: {e}")

def get_active_realty_orm(session: Session, user_id: int, realty_id: int) -> list[RealtyORM]:
    try:
        result = session.execute(select(RealtyORM).where(RealtyORM.is_deleted == False, RealtyORM.user_id == user_id, RealtyORM.id == realty_id))
        realties = result.scalars().all()
        return realties
    except Exception as e:
        raise ValueError(f"Error retrieving realty: {e}")

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

def get_all_active_realties_orm(session: Session) -> list[Realty]:
    try:
        result = session.execute(select(RealtyORM).where(RealtyORM.status == "active"))
        realties = result.scalars().all()
        return realties
    except Exception as e:
        raise ValueError(f"Error retrieving realty: {e}")

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

def replace_realty_orm(session: Session, realty: Realty, realty_id: int):
    try:
        update_data = realty.model_dump()
        result = session.execute(update(RealtyORM).where(RealtyORM.id == realty_id).values(**update_data).execution_options(synchronize_session="fetch"))
        session.commit()
        if result.rowcount == 0:
            raise KeyError(f"Realty does not exist")
    except Exception as e:
        session.rollback()
        raise

def delete_realty_orm(session: Session, realty_id: int):
    result = session.execute(delete(RealtyORM).where(RealtyORM.id == realty_id))
    session.commit()
    if result.rowcount == 0:
        return False
    return True


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

def register_user_orm(session: Session, user_data: dict):
    print(f"Registering user with data: {user_data}")
    try:
        new_user = UserORM(**user_data)
        session.add(new_user)
        session.commit()
        
    except Exception as e:
        session.rollback()
        raise
        raise ValueError(f"Error registering user: {e}")

    return new_user

def get_user_by_email_orm(session: Session, email: str):
    result = session.execute(select(UserORM).where(UserORM.email == email))
    user = result.scalar_one_or_none()
    return user


def get_user_by_id_orm(session: Session, user_id: int) -> UserORM | None:
    result = session.execute(select(UserORM).where(UserORM.id == user_id))
    user = result.scalar_one_or_none()
    return user

def update_user_orm(session: Session, user: UserUpdate, user_id) -> None:
    update_data = user.model_dump(exclude_none=True)
    result = session.execute(update(UserORM).where(UserORM.id == user_id).values(**update_data).execution_options(synchronize_session="fetch"))
    session.commit()
    if result.rowcount == 0:
        raise KeyError(f"User does not exist")

def get_all_users_orm(session: Session) -> list[UserAuth]:
    result = session.execute(select(UserORM))
    users = result.scalars().all()
    return users

def delete_user_orm(session: Session, user_id: int):
    try:
        result = session.execute(update(UserORM).where(UserORM.id == user_id).values(status='inactive'))
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")
    session.commit()
    return result.rowcount == 1

def register_user_sql(user: UserAuth):
    print(f"Registering user with data: {user}")
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

def get_by_email_sql(email: str):
    db = get_db()
    try:
        print(f"Looking for user with email: {email}")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM user WHERE email=?", (email,))
        user = cursor.fetchone()
        if not user:
            raise KeyError(f"User with email {email} not found")
        return UserAuth.model_validate(dict(user))
    finally:
        db.close()

def get_user_sql(user_id: int) -> UserAuth | None:
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

def get_all_users_sql() -> list[UserAuth]:
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()
        return [UserAuth.model_validate(dict(row)) for row in rows]
    finally:
        db.close()

def update_user_sql(user: UserUpdate, user_id) -> None:
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

def delete_user_sql(user_id: int):
    db = get_db()
    try:
        cur = db.cursor()
        cur.execute("UPDATE user SET status=? WHERE id=?", ("inactive", user_id,))
        db.commit()
        return True if cur.rowcount != 0 else False
    finally:
        db.close()