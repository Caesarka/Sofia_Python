class User:
    def __init__(self, dictData: dict = {}):
        self.id = dictData.get("id", None)
        self.name = dictData.get("name", None)
        self.email = dictData.get("email", None)
        self.password = dictData.get("password", None)
        self.reg_date = dictData.get("reg_date", None)
        self.role = dictData.get("role", None)
        self.status = dictData.get("status", None)

    def to_dict(self):
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "reg_date": self.reg_date,
            "role": self.role,
            "status": self.status
        }
        return data
