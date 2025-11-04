from flask_restx import Resource
from flask import jsonify, request
from models.realty_model import Realty, RealtyUpdate
from api_models.realty_api_model import ns_realty, realty_model
from auth.jwt_utils import jwt_required
from auth.utils import decode_access_token
from pydantic import ValidationError
import db
from datetime import datetime


@ns_realty.route("/")
class RealtyList(Resource):
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        realties = db.get_all_realties()
        return [r.model_dump() for r in realties], 200
    
    @jwt_required
    @ns_realty.expect(realty_model, validate=True)
    @ns_realty.marshal_with(realty_model)
    def post(self):
        user_id = request.user["user_id"]
        req = request.json
        req["user_id"] = user_id
        try:
            realty = Realty.model_validate(req)

        except ValidationError as exc:
            return {"error": exc.errors()}, 400

        new_realty = db.create_realty(realty)
        return new_realty.model_dump(), 201

@ns_realty.route("/<int:realty_id>")
class RealtyItem(Resource):
    @ns_realty.marshal_with(realty_model)
    def get(self, realty_id):
        try:
            realty = db.get_realty(realty_id)
            return realty.model_dump(), 200
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")

    @jwt_required
    @ns_realty.expect(realty_model)
    @ns_realty.doc(responses={200: "Updated"})
    def put(self, realty_id):
        user_id = request.user["user_id"]
        realty = RealtyUpdate.model_validate(request.json)
        if realty.id != realty_id:
            ns_realty.abort(400, f"Realty id does not match")
        try:
            db.update_realty(realty, user_id)
            return {"message": "Updated"}, 200
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")

    @jwt_required
    def delete(self, realty_id):
        try:
            realty = db.get_realty(realty_id)
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")
        user_id = request.user["user_id"]
        if user_id == realty.user_id:
            try:
                is_deleted = db.delete_realty(realty_id)
                if is_deleted:
                    return {'message': f'Task {realty_id} deleted'}, 200
                else:
                    return {'message': f'Task {realty_id} not found'}, 404
            except Exception as e:
                return {'message': str(e)}, 500
        else:
            print("You do not have permission for deleting this realty")
        
