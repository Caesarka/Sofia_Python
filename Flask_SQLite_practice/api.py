# SYSTEM
from flask import request
from flask_restx import Resource

# PROJECT
from model import ns, realty_model, realty_input
import realty_sql
import utils

#from .model import ns, realty_input, realty_model
#from services.realty.realty_methods import get_realties_by_filter, post_realty, get_by_id


@ns.route("/")
class RealtyList(Resource):
    @ns.doc(params={
        "city": "City",
        "min_price": "Min price",
        "max_price": "Max price",
    })
    @ns.marshal_list_with(realty_model)
    def get(self):
        """All listings"""
        data = {
            'city': request.args.get("city"),
            'min_price': request.args.get("min_price", type=int),
            'max_price': request.args.get("max_price", type=int)
        }
        rows = get_realties_by_filter(data)
        """
        db = get_db()
        rows = db.execute("SELECT * FROM realty").fetchall()
        return [row_to_dict(r) for r in rows]
        """
        return [row_to_dict(row) for row in rows]

    
    @ns.expect(realty_input, validate=True)
    @ns.marshal_with(realty_model, code=201)
    def post(self):
        """Create new listing"""
        data = self.api.payload
        row = realty_sql.create(data)
        return row, 201


@ns.route("/<int:realty_id>")
@ns.param("realty_id", "ID")
class RealtyItem(Resource):
    @ns.marshal_with(realty_model)
    def get(self, realty_id):
        row = realty_sql.get_by_id(realty_id)
        return row

    @ns.expect(realty_input, validate=True)
    @ns.marshal_with(realty_model)
    def put(self, realty_id):
        """Renew listing (title, price, city)"""
        data = self.api.payload
        db = get_db()
        cur = db.execute(
            "UPDATE realty SET title = ?, price = ?, city = ? WHERE id = ?",
            (data["title"], data["price"], data["city"], realty_id),
        )
        db.commit()
        if cur.rowcount == 0:
            self.api.abort(404, "Realty not found")
        row = db.execute("SELECT * FROM realty WHERE id = ?", (realty_id,)).fetchone()
        return row_to_dict(row)

    def delete(self, realty_id):
        """Delete listing"""
        db = get_db()
        cur = db.execute("DELETE FROM realty WHERE id = ?", (realty_id,))
        db.commit()
        if cur.rowcount == 0:
            self.api.abort(404, "Realty not found")
        return {"message": "deleted", "id": realty_id}, 200