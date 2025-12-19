from datetime import datetime
from L2_Api_Controllers.schemas.realty_model import RealtyPatch, Realty
import L4_Data_Access.db_sql as db_sql
from L4_Data_Access.models.realty_model_orm import RealtyORM


class RealtyService:
    def __init__(self, DBSession):
        self.DBSession = DBSession

    def create_realty(self, realty_data: dict) -> RealtyORM:
        orm_model = db_sql.create_realty_orm(self.DBSession, realty_data)
        return orm_model
    
    def publish_realty(self, realty_id: int) -> None:
        realty = db_sql.get_realty(self.DBSession, realty_id, filter = 'AND is_deleted = 0')

        now = datetime.now().isoformat(timespec='seconds')
        patch_data = RealtyPatch(status=1, published_at=now)
        db_sql.patch_realty(self.DBSession, patch_data, realty_id)

    #def get_realties(self, role: str):
    #    
    #    by_roles = {
    #        'buyer': {
    #            'status':1,
    #            "published_at": "now"
    #        }
    #    }
    #    
    #    get_data = Realty(**by_roles[role])

    def get_realty(self, realty_id: int):
        realty = db_sql.get_realty_orm(self.DBSession, realty_id)
        return realty

    def get_active_realty(self, user_id: int, realty_id: int):
        realty = db_sql.get_active_realty_orm(self.DBSession, user_id, realty_id)
        return realty
    
    def get_all_active_realties(self):
        realties = db_sql.get_all_active_realties_orm(self.DBSession)
        return realties

    def get_my_realties(self, user_id: int, status: str | None = None, is_deleted: bool | None = None):
        filters = [
            RealtyORM.user_id == user_id,
            RealtyORM.status == status if status is not None else status == 'inactive',
            RealtyORM.is_deleted == is_deleted if is_deleted is not None else False
        ]
        realties = db_sql.get_my_active_realties_orm(self.DBSession, user_id, filters)
        return realties
    

    
    def patch_realty(self, realty: RealtyPatch, realty_id: int):
        db_sql.patch_realty_orm(self.DBSession, realty, realty_id)
    
    def replace_realty(self, realty: Realty, realty_id: int):
        db_sql.replace_realty_orm(self.DBSession, realty, realty_id)

    def delete_realty(self, realty_id: int) -> bool:
        is_deleted = db_sql.delete_realty_orm(self.DBSession, realty_id)
        return is_deleted

