class Realty:
    def __init__(self, dictData: dict = {}):
        self.id = dictData.get("id", None)
        self.title = dictData.get("title", None)
        self.price = dictData.get("price", None)
        self.city = dictData.get("city", None)
        self.address = dictData.get("address", None)
        self.image = dictData.get("image", None)

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "city": self.city,
            "address": self.address,
            "image": self.image
        }
        return data
