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
    
    def get_user_by_email(self, email: str):
        user = db_sql.get_user_by_email_orm(self.DBSession, email)
        return user
    
    def get_user_by_id(self, user_id: int):
        user = db_sql.get_user_by_id_orm(self.DBSession, user_id)
        return user
    
    def update_user(self, user_update: UserAuth, user_id: int) -> None:
        db_sql.update_user_orm(self.DBSession, user_update, user_id)

    def get_all_users(self) -> list[UserAuth]:
        db_sql.get_all_users_orm(self.DBSession)
    
    def delete_user(self, user_id: int):
        result = db_sql.delete_user_orm(self.DBSession, user_id)
        return result
