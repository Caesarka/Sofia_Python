from flask_restx import Resource
from flask import jsonify, request
from models.realty_model import Realty
from api_models.realty_api_model import ns_realty, realty_model
import db

@ns_realty.route("/")
class RealtyList(Resource):
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        realty_id = request.args.get("id", type=int)
        if realty_id:
            try:
                realty = db.get_realty(realty_id)
                return realty.model_dump(), 200
            except Exception:
                ns_realty.abort(404, f"Realty with id={realty_id} not found")
        realties = db.get_all_realties()
        return [r.model_dump() for r in realties], 200

    @ns_realty.expect(realty_model, validate=True)
    def post(self):
        realty = Realty.model_validate(request.json)
        db.create_realty(realty)
        return realty.model_dump(), 201
    
    def delete(self):
        realty_id = request.args.get("id", type=int)
        if realty_id:
            db.delete_realty(realty_id)