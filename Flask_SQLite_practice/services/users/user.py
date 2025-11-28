from db.sql.session import get_db
from schemas.user_schema import UserAuth, UserUpdate

from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from db.orm.session import get_session


class User:
    def __init__(self, session):
        self.session = session

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