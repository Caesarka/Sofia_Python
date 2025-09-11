from dataclasses import dataclass
from flask_restx import Namespace, fields

ns = Namespace("realty", description="Reale Estate")


realty_model = ns.model("Realty", {
    "id":   fields.Integer(readonly=True, description="ID"),
    "title": fields.String(required=True, description="Name"),
    "price": fields.Integer(required=True, description="Price"),
    "city":  fields.String(required=True, description="City"),
})

realty_input = ns.model("RealtyInput", {
    "title": fields.String(required=True),
    "price": fields.Integer(required=True),
    "city": fields.String(required=True),
})



#@dataclass(slots=True)
class Realty:
    id: int
    title: str
    price: float
    city: str

    def __init__(self, dict :dict):
        self.id = dict["id"]
        self.title = dict["title"]
        self.price = dict["price"]
        self.city = dict["city"]
        
    
