

from db import get_db
import hashlib

class UserModel:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def create(name, email, password):
        db = get_db()
        pw_hash = UserModel.hash_password(password)
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user (name, email, password) VALUES (?, ?, ?)",
            (name, email, pw_hash)
        )
        db.commit()
        db.close()
        return UserModel.get_by_id(cursor.lastrowid)

    @staticmethod
    def get_by_email(email):
        db = get_db()
        row = db.execute("SELECT * FROM user WHERE email=?", (email,)).fetchone()
        db.close()
        if row:
            return User(dict(row))
        return None

    @staticmethod
    def get_by_id(user_id):
        db = get_db()
        row = db.execute("SELECT * FROM user WHERE id=?", (user_id,)).fetchone()
        db.close()
        if row:
            return User(dict(row))
        return None
    




#def create_user(data):
#    is_user_exist = get_user_by_email(data['email'])
#    if not is_user_exist:
#        db = get_db()
#        row = db.execute(CREATE_USER, data)
#        db.commit()
#        data["id"] = row.lastrowid
#        print(f"User with id {data['id']} was created")
#        db.close()
#        return User(dict(data))
#    else:
#        raise Conflict(f"The email {data.email} is already registered")




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
