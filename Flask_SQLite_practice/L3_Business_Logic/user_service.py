from L2_Api_Controllers.schemas.user_model import UserAuth, UserCreate
from L4_Data_Access import db_sql


class UserService:
    def __init__(self, DBSession):
        self.DBSession = DBSession
    
    def register_user(self, user_data: dict) -> None:
        user_data['password'] = UserAuth.hash_password(user_data['password'])
        user_create = UserCreate.model_validate(user_data)
        
        db_sql.register_user_orm(self.DBSession, user_create.model_dump())

        return user_create.model_dump()