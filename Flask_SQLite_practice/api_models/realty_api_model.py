from flask_restx import Namespace, fields

ns_realty = Namespace("realty", description="Real Estate")

realty_model = ns_realty.model("Realty", {
    "id":   fields.Integer(readonly=True, description="ID"),
    "title": fields.String(required=True, description="Name"),
    "price": fields.Integer(required=True, description="Price"),
    "city":  fields.String(required=True, description="City"),
    "address":  fields.String(required=True, description="Address"),
    "image": fields.String(required=False),
})