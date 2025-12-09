from datetime import datetime
import os
import tempfile
import unittest
import uuid
import gc

#from database.config import DB_PATH
from L4_Data_Access.orm import session as orm_session
from L4_Data_Access.sql import session as sql_session
import L4_Data_Access.db_sql as db_sql
from L2_Api_Controllers.schemas.realty_model import Realty, RealtyPatch
from L2_Api_Controllers.schemas.user_model import UserAuth, UserUpdate, UserCreate

class DatabaseTests(unittest.TestCase):

    def setUp(self):
        db_fd, self.temp_path = tempfile.mkstemp()
        os.close(db_fd)
        
        sql_session.DB_PATH = self.temp_path
        orm_session.DB_PATH = self.temp_path
        
        orm_session.DATABASE_URL = f"sqlite:///{self.temp_path}"
        orm_session.engine = None
        orm_session.session_factory = None
        
        print("\nSetup...")
        sql_session.init_db_if_needed_v1()
        # v2 for ORM
        orm_session.init_db_if_needed_v2()
        self.session = orm_session.session_factory()

        print("\nSetup Done")


    def tearDown(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
            
        if orm_session.engine:
            orm_session.engine.dispose()
        
        gc.collect()
        
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)


    def test_empty_db_schema(self):
        #print(f"\nTesting DB at {db.DB_PATH}")
        conn = sql_session.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn('realty', tables)
        self.assertIn('user', tables)
        self.assertIn('favorite', tables)
        conn.close()


# realty
    def test_create_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", created_at="", status=1, user_id=1)
        db_sql.create_realty(realty)
        print(realty.id)
        new_realty = db_sql.get_realty(realty.id)
        self.assertEqual(new_realty.id, realty.id)
        self.assertEqual(new_realty.title, realty.title)


    def test_get_realties(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", created_at="", status=1, user_id=1)
        db_sql.create_realty(realty)
        realties = db_sql.get_all_realties()
        self.assertEqual(len(realties), 1)


    def test_get_realties_list_is_emply(self):
        realties = db_sql.get_all_realties()
        self.assertEqual(realties, [])


    def test_get_realty(self):
        with self.assertRaises(KeyError) as context:
            db_sql.get_realty(1)
        self.assertIn("not found", str(context.exception))


    def test_delete_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", created_at="", status=1, user_id=1)
        db_sql.create_realty(realty)
        result = db_sql.delete_realty(realty.id)
        self.assertTrue(result)
        result = db_sql.delete_realty(10)
        self.assertFalse(result)


    def test_replace_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", created_at="", status=1, user_id=1)
        db_sql.create_realty(realty)

        realty.title = "Mishkin dom"
        realty.price = 1001
        db_sql.replace_realty(realty, realty.id)
        replaced_realty = db_sql.get_realty(realty.id)
        self.assertEqual(replaced_realty.title, "Mishkin dom")
        self.assertEqual(replaced_realty.price, 1001)

    def test_patch_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", created_at="", status=1, user_id=1)
        db_sql.create_realty(realty)

        patch_realty = RealtyPatch(title="Mishkin dom", price=1001, city="Katcity", address="Tree street", image="some_image")
        db_sql.patch_realty(patch_realty, realty.id)
        patched_realty = db_sql.get_realty(realty.id)
        self.assertEqual(patched_realty.title, patch_realty.title)
        self.assertEqual(patched_realty.price, patch_realty.price)

        self.assertNotEqual(patched_realty, patch_realty)

        update_field = RealtyPatch(title="New dom")
        db_sql.patch_realty(update_field, realty.id)
        new_field_realty = db_sql.get_realty(patched_realty.id)
        self.assertEqual(new_field_realty.title, update_field.title)

#user



    def create_user(self):
        self.user = UserCreate(
            name = f"Julianna + {str(uuid.uuid4())}",
            email = f"my@mail.com + {str(uuid.uuid4())}",
            password = "hetryi459865ruhyrkjt86", 
            reg_date = "10.15.2025.11:00AM", 
            role = "buyer", 
            status = True
        )
    
        user_dict = self.user.model_dump()
        user_dict['reg_date'] = datetime.now()
        db_sql.register_user_orm(self.session, user_dict)

        

    def test_register_user(self):
        self.create_user()

        # todo: переписать get_by_email на pydantic
        new_user = db_sql.get_by_email_orm(self.session, self.user.email) #self.session, 
        self.assertIsNotNone(new_user.id)
        #self.assertEqual(new_user.email, user_dict['email'])


    def test_get_user_by_email(self):
        self.create_user() 
        get_user = db_sql.get_by_email(self.user.email) #self.session, 
        self.assertEqual(get_user.email, self.user.email)
        self.assertNotEqual(get_user, "wrong@email.com")


    def test_get_users(self):
        user = UserAuth(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="2025-10-15T11:00:00", role="buyer", status='active')
        user1 = UserAuth(name="Dmitry", email="another@mail.com", password="trjtyjetyj56456756et", reg_date="2025-10-15T11:00:00", role="buyer", status='active')
        db_sql.register_user_orm(self.session, user.model_dump())
        db_sql.register_user_orm(self.session, user1.model_dump())
        users = db_sql.get_all_users()
        self.assertEqual(len(users), 2)


    def test_delete_user(self):
        user = UserAuth(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="2025-10-15T11:00:00", role="buyer", status='active')
        userOrm = db_sql.register_user_orm(self.session, user.model_dump())
        user_id = userOrm.id
        db_sql.delete_user_orm(self.session, userOrm.id)
        inactive_user = db_sql.get_user(user_id)
        self.assertEqual(inactive_user.status, "inactive")


    def test_update_user(self):
        user = UserAuth(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="2025-10-15T11:00:00", role="buyer", status='active')
        userOrm = db_sql.register_user_orm(self.session, user.model_dump())
        update_user = UserUpdate(name="Julia", email="mew@mail.com", password="newpassword4353")
        db_sql.update_user_orm(self.session, update_user, userOrm.id)
        new_user = db_sql.get_user(userOrm.id)
        self.assertEqual(new_user.name, update_user.name)
        self.assertEqual(new_user.email, update_user.email)
        update_user.name = "Anna"
        self.assertNotEqual(new_user.name, update_user.name)


if __name__ == "__main__":
    unittest.main()

