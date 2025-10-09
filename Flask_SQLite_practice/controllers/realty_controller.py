from flask_restx import Resource
from flask import jsonify, request
from models.realty_model import Realty
from api_models.realty_api_model import ns_realty, realty_model
import db

@ns_realty.route("/")
class RealtyList(Resource):
    @ns_realty.marshal_list_with(realty_model)
    def get(self):
        pass

    @ns_realty.expect(realty_model, validate=True)
    def post(self):
        realty = Realty.model_validate(request.json)
        db.create_realty(realty)
        return realty.model_dump(), 201
