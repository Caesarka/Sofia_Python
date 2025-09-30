from database.realty import get_db
from models.realty import Realty

GET_BY_FILTER = """
    SELECT *
    FROM realty
    WHERE
        (city=:city OR :city IS NULL)
        AND (price>=:min_price OR :min_price IS NULL)
        AND (price<=:max_price OR :max_price IS NULL)
"""

CREATRE_LISTING = """
    INSERT INTO realty (title, price, city, address)
    VALUES (:title, :price, :city, :address)
"""

GET_BY_ID = """
    SELECT *
    FROM realty 
    WHERE id=:id
"""

UPDATE_LISTING = """
    UPDATE realty
    SET title=:title, price=:price, city=:city
    WHERE id=:id
"""

DELETE_LISTING = """
    DELETE FROM realty
    WHERE id=:id
"""

METHODS = {
  'get_filter': GET_BY_FILTER,
  'create': CREATRE_LISTING,
  'update': UPDATE_LISTING,
  'delete': DELETE_LISTING,
  'get_by_id': GET_BY_ID
}


def get_by_filter(params: dict):
    db = get_db()
    rows = db.execute(GET_BY_FILTER, params).fetchall()
    db.close()
    return [Realty(dict(row)) for row in rows]

def get_by_id(id: int) -> Realty:
    db = get_db()
    realty = db.execute(GET_BY_ID, {"id": id}).fetchone()
    db.close()
    return Realty(dict(realty))

def create(realty):
    db = get_db()
    try:
        row = db.execute(CREATRE_LISTING, realty)
        db.commit()
        realty["id"] = row.lastrowid
        return Realty(dict(realty))
    finally:
        db.close()

def update(realty_id: int, params: dict):
    db = get_db()
    try:
        rowIdData = {
            'id': realty_id
        }
        rowIdData.update(params)
        db.execute(UPDATE_LISTING, rowIdData)
        db.commit()
        
        realty = get_by_id(realty_id)
        return realty
    finally:
        db.close()

def delete(realty_id: int):
    db = get_db()
    db.execute(DELETE_LISTING, {"id": realty_id})
    db.commit()
    db.close()



# if __name__ == "__main__":
    # execute_data('get_filter', [])
