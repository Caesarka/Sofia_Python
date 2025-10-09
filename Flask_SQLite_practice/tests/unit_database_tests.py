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
        pass
        #os.close(self.db_fd)
        os.unlink(self.temp_path)

    def test_empty_db_schema(self):
        print(f"\nTesting DB at {db.DB_PATH}")
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn('realty', tables)
        self.assertIn('user', tables)
        self.assertIn('favorite', tables)
        conn.close()

    def test_create_realty(self):
        print(f"\nTesting DB at {db.DB_PATH}")
        realty = Realty(title="Koshkin dom", price=1000, city="Katcity", address="Tree street", image="some_image")
        db.create_realty(realty)
        print(realty.id)
        new_realty = db.get_realty(realty.id)
        self.assertEqual(new_realty.id, realty.id)
        self.assertEqual(new_realty.title, realty.title)




if __name__ == "__main__":
    unittest.main()
