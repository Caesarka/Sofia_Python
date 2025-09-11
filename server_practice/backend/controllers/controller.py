from flask import session
from flask_restx import Resource
#from schemas import realty_model
from models.model import RealtyModel
from app import api


#@api.route("/api/v1/realty/")
#class Realty(Resource):
#
#    def get(self):
#        return f"Get {id}"
#    
#    def post(self, id):
#        return "Post"
#    
#    def put(self, id):
#        return "Put"
#
#    def delete(self, id):
#        return "Delete"
#    
# all objects


#@api.route("/api/v1/realty/<id>")
#class RealtyOne(Resource):
#    @api.doc(description="Get property by id")
#    def get(self, id):
#        return {"id": id, "name": "Property {id}"}
#
#    @api.doc(description="Update property by id")
#    def put(self, id):
#        return {"message": f"Property {id} updated"}
#    
#    @api.doc(description="Delete property by id")
#    def delete(self, id):
#        return {"message": f"Property {id} deleted"}
#
#
#@api.route("/api/v1/realty/search")
#class RealtySearch(Resource):
#    @api.doc(description="Search property by filters")
#    def get(self):
#        city = request.args.get("city")
#        price_lte = request.args.get("price_lte")
#        return {
#            "filters": {"city": city, "price_lte": price_lte},
#            "results": []
#        }