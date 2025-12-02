from datetime import datetime
from L2_Api_Controllers.schemas.realty_model import RealtyPatch
import L4_Data_Access.db_sql as db_sql


class RealtyService:
    def __init__(self):
        pass

    def publish_realty(self, realty_id: int) -> None:
        realty = db_sql.get_realty(realty_id, filter = 'AND is_deleted = 0')

        now = datetime.now().isoformat(timespec='seconds')
        patch_data = RealtyPatch(status=1, published_at=now)
        db_sql.patch_realty(patch_data, realty_id)

