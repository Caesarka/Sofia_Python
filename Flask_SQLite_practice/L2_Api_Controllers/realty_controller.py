from datetime import datetime
from flask_restx import Resource
from flask import request
from L4_Data_Access.orm.session import get_session
from L3_Business_Logic.realty_service import RealtyService
from L2_Api_Controllers.schemas.realty_model import Realty, RealtyPatch
from L2_Api_Controllers.realty_api_model import ns_realty, realty_model
from .auth.jwt_utils import jwt_required
from .auth.role_utils import role_required
from pydantic import ValidationError
import L4_Data_Access.db_sql as db_sql


@ns_realty.route("/")
class RealtyList(Resource):
    #@jwt_required
    #@role_required(['realtor', 'admin', 'buyer'])
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        DBSession = get_session()
        #user = request.user
        #user_id = user["user_id"]
        #user_role = user["role"]

        #if user_role == 'buyer':
        #    realties = RealtyService(DBSession).get_all_active_realties()

        #elif user_role == 'realtor':
        #    realties = RealtyService(DBSession).get_my_realties(user_id)

        #else:
        #    realties = db_sql.get_all_realties()
        realties = RealtyService(DBSession).get_all_active_realties()
        return realties, 200
    
    @jwt_required
    @role_required(['realtor', 'admin'])
    @ns_realty.expect(realty_model, validate=True)
    @ns_realty.marshal_with(realty_model)
    def post(self):
        DBSession = get_session()
        try:
            user_id = request.user["user_id"]
            realty_data = request.json
            print(realty_data)
            realty_data["user_id"] = user_id

            try:
                new_realty = RealtyService(DBSession).create_realty(realty_data)

            except ValidationError as e:
                return {"error": e.errors()}, 400
            
            return new_realty, 201

        except ValidationError as e:
            print("Unexpected error:", e)
            return {"message": "Internal server error"}, 500
        
        finally:
            DBSession.close()


@ns_realty.route("/<int:realty_id>")
class RealtyItem(Resource):
    @ns_realty.marshal_with(realty_model)
    def get(self, realty_id):
        DBSession = get_session()
        try:
            realty = RealtyService(DBSession).get_realty(realty_id)
            return realty, 200
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")

    @jwt_required
    @role_required(['realtor', 'admin'])
    @ns_realty.expect(realty_model)
    @ns_realty.doc(responses={200: "Updated"})
    # !! doesn't work as expected !! Lost realty model fields that came epmty !! Use patch instead
    def put(self, realty_id):
        DBSession = get_session()
        user_id = request.user["user_id"]
        #request.json["user_id"] = user_id
        realty = Realty.model_validate(request.json)
        # todo: переделать под использование декоратора
        if realty.user_id != user_id:
            ns_realty.abort(403, "You are not authorized to modify this realty listing.")
            
        #try:
        RealtyService(DBSession).replace_realty(realty, realty_id)
        return {"message": "Updated"}, 200
        #except Exception as ex:
            #ns_realty.abort(404, f"Realty with id={realty_id} not found. Ex: {ex}")
            #raise ex

    @jwt_required
    @role_required(['realtor', 'admin'])
    @ns_realty.doc(responses={200: "Updated"})
    def patch(self, realty_id):
        DBSession = get_session()
        realty = RealtyPatch.model_validate(request.json)
        update_data = realty.model_dump(exclude_unset=True, exclude_none=True)
        print(realty)
        user_role = request.user.get("role")
        print(user_role)
        if "status" in update_data and user_role == 'realtor':
            ns_realty.abort(403, "You are not authorized to change the publish status.")
        RealtyService(DBSession).patch_realty(realty, realty_id)

    @jwt_required
    @role_required(['realtor', 'admin'])
    def delete(self, realty_id):
        try:
            DBSession = get_session()
            realty = RealtyService(DBSession).get_realty(realty_id)
        except Exception:
            ns_realty.abort(404, f"Realty with id={realty_id} not found")
        user = request.user
        user_id = user["user_id"]
        user_role = user["role"]
        can_delete = (
            user_role == "admin" or
            (realty.user_id == user_id)# and realty.published_at is None)

        )
        if not can_delete:
            print("You do not have permission for deleting this realty")

        try:
            is_deleted = RealtyService(DBSession).delete_realty(realty_id)
            if is_deleted:
                return {'message': f'Task {realty_id} deleted'}, 200
            else:
                return {'message': f'Task {realty_id} not found'}, 404
        except Exception as e:
            return {'message': str(e)}, 500



@ns_realty.route("/<int:realty_id>/publish")
class RealtyPublish(Resource):
    @jwt_required
    @role_required(['admin'])
    def patch(self, realty_id):
        DBsession = get_session()
        try:
            RealtyService(DBsession).publish_realty(realty_id)
        except Exception:
            raise
            #ns_realty.abort(404, f"Realty with id={realty_id} not found")


@ns_realty.route("/my")
class RealtyCreatorList(Resource):
    @jwt_required
    @role_required(['realtor', 'admin'])
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        DBSession = get_session()
        user = request.user
        user_id = user["user_id"]

        status = request.args.get('status')
        is_deleted = request.args.get('is_deleted')

        # Логика такая, что мы передаем в метод id пользователя и фильтруем сразу по этому id
        realties = RealtyService(DBSession).get_my_realties(user_id, status=status, is_deleted=is_deleted)
        print(realties)
        return realties, 200

@ns_realty.route("/my/<int:realty_id>")
class RealtyCreatorList(Resource):
    @jwt_required
    @role_required(['realtor', 'admin'])
    @ns_realty.marshal_list_with(realty_model)
    def get(self, realty_id):
        DBSession = get_session()
        user = request.user
        user_id = user["user_id"]
        user_role = user["role"]

        # Логика такая, что мы передаем в метод id пользователя и фильтруем сразу по этому id
        realty = RealtyService(DBSession).get_active_realty(user_id, realty_id)
        print(realty)
        return realty, 200
