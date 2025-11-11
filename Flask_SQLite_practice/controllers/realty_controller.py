from flask_restx import Resource
from flask import request
from models.realty_model import Realty, RealtyPatch
from api_models.realty_api_model import ns_realty, realty_model
from auth.jwt_utils import jwt_required
from auth.role_utils import role_required
from pydantic import ValidationError
import db


@ns_realty.route("/")
class RealtyList(Resource):
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        realties = db.get_all_realties()
        return [r.model_dump() for r in realties], 200
    
    @jwt_required
    @role_required(['realtor', 'admin'])
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
    @role_required(['realtor', 'admin'])
    @ns_realty.expect(realty_model)
    @ns_realty.doc(responses={200: "Updated"})
    def put(self, realty_id):
        user_id = request.user["user_id"]
        realty = Realty.model_validate(request.json)
        if realty.user_id != user_id:
            ns_realty.abort(403, "You are not authorized to modify this realty listing.")
            
        try:
            db.replace_realty(realty, realty_id)
            return {"message": "Updated"}, 200
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")

    @jwt_required
    @role_required(['realtor', 'admin'])
    @ns_realty.doc(responses={200: "Updated"})
    def patch(self, realty_id):
        realty = RealtyPatch.model_validate(request.json)
        update_data = realty.model_dump(exclude_unset=True, exclude_none=True)
        print(realty)
        user_role = request.user.get("role")
        print(user_role)
        if "status" in update_data and user_role == 'realtor':
            ns_realty.abort(403, "You are not authorized to change the publish status.")
        db.patch_realty(realty, realty_id)

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


@ns_realty.route("/<int:realty_id>/publish")
class RealtyPublish(Resource):
    @jwt_required
    @role_required(['admin'])
    def patch(self, realty_id):
        try:
            realty = db.get_realty(realty_id, filter = 'AND is_deleted = 0')
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")

        db.patch_realty(RealtyPatch(status=1), realty_id)
