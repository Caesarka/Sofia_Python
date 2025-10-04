## SYSTEM
#from flask import request
#from flask_restx import Resource
#
## PROJECT
#from models.realty import ns_realty, realty_model, realty_input
#from services.realty import sql
#from utils.utils import row_to_dict
#
#
#@ns_realty.route("/")
#class RealtyList(Resource):
#    @ns_realty.doc(params={
#        "city": "City",
#        "min_price": "Min price",
#        "max_price": "Max price",
#    })
#    @ns_realty.marshal_list_with(realty_model)
#    def get(self):
#        """Get by filter"""
#        data = {
#            'city': request.args.get("city"),
#            'min_price': request.args.get("min_price", type=int),
#            'max_price': request.args.get("max_price", type=int)
#        }
#        rows = sql.get_by_filter(data)
#        return rows
#
#    @ns_realty.expect(realty_input, validate=True)
#    @ns_realty.marshal_with(realty_model, code=201)
#    def post(self):
#        """Create new listing"""
#        data = self.api.payload
#        row = sql.create(data)
#        return row, 201
#
#
#@ns_realty.route("/<int:realty_id>")
#@ns_realty.param("realty_id", "ID")
#class RealtyItem(Resource):
#    @ns_realty.marshal_with(realty_model)
#    def get(self, realty_id):
#        """Get by ID"""
#        row = sql.get_by_id(realty_id)
#        return row
#
#    @ns_realty.expect(realty_input, validate=True)
#    @ns_realty.marshal_with(realty_model)
#    def patch(self, realty_id):
#        """Renew1111 listing (title, price, city)"""
#        data = self.api.payload
#        row = sql.update(realty_id, data)
#        return row
#
#    def delete(self, realty_id):
#        """Delete listing"""
#        sql.delete(realty_id)
#        return {"message": "deleted", "id": realty_id}, 202

from flask_restx import Resource
from flask import request
from models.realty_model import RealtyModel
from api_models.realty_api_model import ns_realty, realty_model

@ns_realty.route("/")
class RealtyList(Resource):
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        return [r.to_dict() for r in RealtyModel.list_all()]

    @ns_realty.expect(realty_model)
    def post(self):
        data = request.json
        realty = RealtyModel.create(
            data["title"], data["price"], data["city"], data["address"], data.get("image")
        )
        return realty.to_dict(), 201