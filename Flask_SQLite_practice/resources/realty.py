# SYSTEM
from flask import request
from flask_restx import Resource

# PROJECT
from models.realty import ns, realty_model, realty_input
from services.realty import sql
from utils.utils import row_to_dict

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
        """Get by filter"""
        data = {
            'city': request.args.get("city"),
            'min_price': request.args.get("min_price", type=int),
            'max_price': request.args.get("max_price", type=int)
        }
        rows = sql.get_by_filter(data)
        return rows

    @ns.expect(realty_input, validate=True)
    @ns.marshal_with(realty_model, code=201)
    def post(self):
        """Create new listing"""
        data = self.api.payload
        row = sql.create(data)
        return row, 201


@ns.route("/<int:realty_id>")
@ns.param("realty_id", "ID")
class RealtyItem(Resource):
    @ns.marshal_with(realty_model)
    def get(self, realty_id):
        """Get by ID"""
        row = sql.get_by_id(realty_id)
        return row

    @ns.expect(realty_input, validate=True)
    @ns.marshal_with(realty_model)
    def patch(self, realty_id):
        """Renew1111 listing (title, price, city)"""
        data = self.api.payload
        row = sql.update(realty_id, data)
        return row

    def delete(self, realty_id):
        """Delete listing"""
        sql.delete(realty_id)
        return {"message": "deleted", "id": realty_id}, 202