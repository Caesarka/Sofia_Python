from database.user import get_db
from models.user import User


CREATE_USER = """
    INSERT INTO user (name, password, email)
    VALUES (:name, :password, :email)
"""

CHECK_USER_PASS = """
    SELECT *
    FROM user
    WHERE (name=:name OR email=:email)
    AND password=:password
"""

GET_USER = """
    SELECT *
    FROM user
    WHERE id=:id
"""

UPDATE_USER = """
    UPDATE user
    SET name=:name, password=:password, email=:email
    WHERE id=:id
"""

SET_NEW_PASS = """
    UPDATE user
    SET password=:password
    WHERE id=:id
"""

DELETE_USER = """
    UPDATE user
    SET status='inactive'
    WHERE id=:id
"""

SET_USER_ACTIVE = """
    UPDATE user
    SET status='active'
    WHERE id=:id AND status='inactive'
"""

METHODS = {
  'create_user': CREATE_USER,
  'check_user_pass': CHECK_USER_PASS,
  'get_user': GET_USER,
  'update_user': UPDATE_USER,
  'set_new_pass': SET_NEW_PASS,
  'delete_user': DELETE_USER,
  'set_user_active': SET_USER_ACTIVE
}

def execute_data(method: str, params: dict, fetch: str = "none"):
    sql = METHODS.get(method)
    if not sql:
        raise ValueError(f"Method {method} does not exist")
    db = get_db()
    cur = db.execute(sql, params)
    if method == "create_user":
        db.commit()
        params['id'] = cur.lastrowid
        return User(dict(params))
    if fetch == "all":
        rows = cur.fetchall()
        return [User(dict(row)) for row in rows]
    elif fetch == "one":

        row = cur.fetchone()
        return User(dict(row)) if row else None
    db.commit()



def create(user):
    db = get_db()
    row = db.execute(CREATE_USER, user)
    db.commit()
    user["id"] = row.lastrowid
    print(f"User with id {user['id']} was created")
    return User(dict(user))

