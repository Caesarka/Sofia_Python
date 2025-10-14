import os
import tempfile
import unittest

#from database.config import DB_PATH
import db as db
from models.realty_model import Realty

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

    def test_delete(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        result = db.delete_realty(realty.id)
        self.assertTrue(result)
        result = db.delete_realty(10)
        self.assertFalse(result)

    def test_update(self):
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        update_realty = Realty(title="Mishkin dom", price=1000, city="Katcity", address="Tree street", image="some_image", id=realty.id)
        db.update_realty(update_realty)
        new_realty = db.get_realty(update_realty.id)
        self.assertEqual(new_realty, update_realty)
        update_realty.title = "aeraherh"
        self.assertNotEqual(new_realty, update_realty)



if __name__ == "__main__":
    unittest.main()
