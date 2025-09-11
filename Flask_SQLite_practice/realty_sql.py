from db import get_db
from model import Realty

LISTINGS = """
    SELECT *
    FROM realty
    WHERE
        (city=:city OR :city IS NULL)
        AND (price>=:minprice OR :minprice IS NULL)
        AND (price<=:maxprice OR :maxprice IS NULL)
"""

CREATRE_LISTING = """
    INSERT INTO realty (title, price, city)
    VALUES (:title, :price, :city)
"""

GET_BY_ID = """
    SELECT *
    FROM realty 
    WHERE id=:id
"""

UPDATE_LISTING = """
    UPDATE realty
    SET title=?, price=?, city=?
    WHERE id=:id
"""

DELETE_LISTING = """
    DELETE FROM realty
    WHERE id=:id
"""

METHODS = {
  'get_filter': LISTINGS,
  'create': CREATRE_LISTING,
  'update': UPDATE_LISTING,
  'delete': DELETE_LISTING,
  'get_by_id': GET_BY_ID
}

def execute_data(q: str, params: dict):
    db = get_db()
    rows = db.execute(METHODS[q], params)
    if q == 'get_filters':
        rows = rows.fetchall()
    if q == 'create' or q == 'delete' or q == 'update':
        db.commit()
        if q == 'create':
            new_id = rows.lastrowid
            rows = db.execute(METHODS['get_by_id'], new_id).fetchone()
    return rows



def get_by_filter(params: dict):
    pass

def get_by_id(id: int) -> Realty:
    db = get_db()
    row = db.execute(GET_BY_ID, {"id": id}).fetchone()
    return Realty(row)

def create(data):
    db = get_db()
    row = db.execute(CREATRE_LISTING, data)
    db.commit()
    data["id"] = row.lastrowid
    return Realty(data)

def update():
    pass

def delete():
    pass


if __name__ == "__main__":
    execute_data('get_filter', [])
