from dataclasses import dataclass
from flask_restx import Namespace, fields

ns_realty = Namespace("realty", description="Real Estate")


realty_model = ns_realty.model("Realty", {
    "id":   fields.Integer(readonly=True, description="ID"),
    "title": fields.String(required=True, description="Name"),
    "price": fields.Integer(required=True, description="Price"),
    "city":  fields.String(required=True, description="City"),
})

realty_input = ns_realty.model("RealtyInput", {
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
    image: str
    address: str

    def __init__(self, dictData: dict = {}):
        if not dictData:
            dictData = {}
        print(dictData)
        self.id = dictData.get("id", None)
        self.title = dictData.get("title", None)
        self.price = dictData.get("price", None)
        self.city = dictData.get("city", None)
        self.image = dictData.get("image", None)
        self.address = dictData.get("address", None)
        
    
