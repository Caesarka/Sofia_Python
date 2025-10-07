from db import get_db
from entities.realty import Realty

class RealtyModel:
    @staticmethod
    def create(title, price, city, address, image=None):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO realty (title, price, city, address, image) VALUES (?, ?, ?, ?, ?)",
            (title, price, city, address, image)
        )
        db.commit()
        db.close()
        return RealtyModel.get_by_id(cursor.lastrowid)
    
    @staticmethod
    def get_by_id(realty_id):
        db = get_db()
        row = db.execute("SELECT * FROM realty WHERE id=?", (realty_id,)).fetchone()
        if row:
            return Realty(dict(row))
        db.close()
        return None

    @staticmethod
    def list_all():
        db = get_db()
        rows = db.execute("SELECT * FROM realty").fetchall()
        db.close()
        return [Realty(dict(row)) for row in rows]
    