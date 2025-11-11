import os
import tempfile
import unittest

#from database.config import DB_PATH
import db as db
from models.realty_model import Realty
from models.user_model import User

class DatabaseTests(unittest.TestCase):

    def setUp(self):
        db_fd, self.temp_path = tempfile.mkstemp()
        os.close(db_fd)
        db.DB_PATH = self.temp_path
        print("\nSetup...")
        db.init_db_if_needed()
        print("\nSetup Done")


    def tearDown(self):
        os.unlink(self.temp_path)


    def test_empty_db_schema(self):
        #print(f"\nTesting DB at {db.DB_PATH}")
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn('realty', tables)
        self.assertIn('user', tables)
        self.assertIn('favorite', tables)
        conn.close()


# realty
    def test_create_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        print(realty.id)
        new_realty = db.get_realty(realty.id)
        self.assertEqual(new_realty.id, realty.id)
        self.assertEqual(new_realty.title, realty.title)


    def test_get_realties(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        realties = db.get_all_realties()
        self.assertEqual(len(realties), 1)


    def test_get_realties_list_is_emply(self):
        realties = db.get_all_realties()
        self.assertEqual(realties, [])


    def test_get_realty(self):
        with self.assertRaises(KeyError) as context:
            db.get_realty(1)
        self.assertIn("not found", str(context.exception))


    def test_delete_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        result = db.delete_realty(realty.id)
        self.assertTrue(result)
        result = db.delete_realty(10)
        self.assertFalse(result)


    def test_update_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        update_realty = Realty(title="Mishkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", id=realty.id)
        db.update_realty(update_realty)
        new_realty = db.get_realty(update_realty.id)
        self.assertEqual(new_realty, update_realty)
        update_realty.title = "aeraherh"
        self.assertNotEqual(new_realty, update_realty)

        realty.title = "Mishkin dom"
        realty.price = 1001
        db.replace_realty(realty, realty.id)
        replaced_realty = db.get_realty(realty.id)
        self.assertEqual(replaced_realty.title, "Mishkin dom")
        self.assertEqual(replaced_realty.price, 1001)

    def test_patch_realty(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", created_at="", status=1, user_id=1)
        db.create_realty(realty)

        patch_realty = RealtyPatch(title="Mishkin dom", price=1001, city="Katcity", address="Tree street", image="some_image")
        db.patch_realty(patch_realty, realty.id)
        patched_realty = db.get_realty(realty.id)
        self.assertEqual(patched_realty.title, patch_realty.title)
        self.assertEqual(patched_realty.price, patch_realty.price)

        self.assertNotEqual(patched_realty, patch_realty)

        update_field = RealtyPatch(title="New dom")
        db.patch_realty(update_field, realty.id)
        new_field_realty = db.get_realty(patched_realty.id)
        self.assertEqual(new_field_realty.title, update_field.title)

#user
    def test_register_user(self):
        user = User(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="10.15.2025.11:00AM", role="user", status="active")
        db.register_user(user)
        print(user.id)
        new_user = db.get_user(user.id)
        self.assertEqual(new_user.id, user.id)
        self.assertEqual(new_user.email, user.email)


    def test_get_user_by_email(self):
        user = User(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="10.15.2025.11:00AM", role="user", status="active")
        db.register_user(user)
        get_user = db.get_by_email(user.email)
        self.assertEqual(get_user.email, user.email)
        self.assertNotEqual(get_user, "wrong@email.com")


    def test_get_users(self):
        user = User(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="10.15.2025.11:00AM", role="user", status="active")
        user1 = User(name="Dmitry", email="another@mail.com", password="trjtyjetyj56456756et", reg_date="10.16.2025.11:39AM", role="user", status="active")
        db.register_user(user)
        db.register_user(user1)
        users = db.get_all_users()
        self.assertEqual(len(users), 2)


    def test_delete_user(self):
        user = User(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="10.15.2025.11:00AM", role="user", status="active")
        db.register_user(user)
        db.delete_user(user.id)
        inactive_user = db.get_user(user.id)
        self.assertEqual(inactive_user.status, "inactive")


    def test_update_user(self):
        user = User(name="Julianna", email="my@mail.com", password="hetryi459865ruhyrkjt86", reg_date="10.15.2025.11:00AM", role="user", status="active")
        db.register_user(user)
        update_user = User(name="Julia", email="mew@mail.com", password="newpassword4353", reg_date=user.reg_date, role=user.role, status=user.status, id=user.id)
        db.update_user(update_user)
        new_user = db.get_user(update_user.id)
        self.assertEqual(new_user, update_user)
        update_user.name = "Anna"
        self.assertNotEqual(new_user, update_user)


if __name__ == "__main__":
    unittest.main()

