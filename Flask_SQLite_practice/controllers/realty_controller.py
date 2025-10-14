from flask_restx import Resource
from flask import jsonify, request
from models.realty_model import Realty
from api_models.realty_api_model import ns_realty, realty_model
import db

@ns_realty.route("/")
class RealtyList(Resource):
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        realties = db.get_all_realties()
        return [r.model_dump() for r in realties], 200

    @ns_realty.expect(realty_model, validate=True)
    def post(self):
        realty = Realty.model_validate(request.json)
        db.create_realty(realty)
        return realty.model_dump(), 201



@ns_realty.route("/<int:realty_id>")
class RealtyList(Resource):
    @ns_realty.marshal_with(realty_model)
    def get(self, realty_id):
        try:
            realty = db.get_realty(realty_id)
            return realty.model_dump(), 200
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")


    @ns_realty.doc(responses={200: "No content"})
    def put(self, realty_id):
        realty = Realty.model_validate(request.json)
        if realty.id != realty_id:
            ns_realty.abort(400, f"Realty id does not match")
        try:
            db.update_realty(realty)
            return {}, 200
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")


    @ns_realty.marshal_with(realty_model)
    def delete(self, realty_id):
        try:
            is_deleted = db.delete_realty(realty_id)
            if is_deleted:
                return {'message': f'Task {realty_id} deleted'}, 200
            else:
                return {'message': f'Task {realty_id} not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500
