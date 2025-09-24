from database.realty import get_db
from models.user import User


CREATRE_USER = """
    INSERT INTO user (name, password, email)
    VALUES (:name, :password, :email)
"""

CHECK_USER_PASS = """
    SELECT *
    FROM user
    WHERE name=:name OR email=:email
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
  'create_user': CREATRE_USER,
  'check_user_pass': CHECK_USER_PASS,
  'get_user': GET_USER,
  'update_user': UPDATE_USER,
  'set_new_pass': SET_NEW_PASS,
  'delete_user': DELETE_USER,
  'set_user_active': SET_USER_ACTIVE
}


def create_user(params: dict):
    db = get_db()
    rows = db.execute(CREATRE_USER, params).fetchall()
    return [User(dict(row)) for row in rows]

#def get_by_id(id: int) -> Realty:
#    db = get_db()
#    realty = db.execute(GET_BY_ID, {"id": id}).fetchone()
#    return Realty(dict(realty))
#
#def create(realty):
#    db = get_db()
#    row = db.execute(CREATRE_LISTING, realty)
#    db.commit()
#    realty["id"] = row.lastrowid
#    return Realty(dict(realty))
#
#def update(realty_id: int, params: dict):
#    db = get_db()
#    rowIdData = {
#        'id': realty_id
#    }
#    rowIdData.update(params)
#    db.execute(UPDATE_LISTING, rowIdData)
#    db.commit()
#    
#    realty = get_by_id(realty_id)
#    return realty
#
#def delete(realty_id: int):
#    db = get_db()
#    db.execute(DELETE_LISTING, {"id": realty_id})
#    db.commit()



# if __name__ == "__main__":
    # execute_data('get_filter', [])
