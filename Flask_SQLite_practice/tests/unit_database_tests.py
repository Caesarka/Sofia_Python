import os
import tempfile
import unittest

#from database.config import DB_PATH
import db as db

class DatabaseTests(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.temp_path = tempfile.mkstemp()
        db.DB_PATH = self.temp_path
        print("\nSetup...")
        db.init_db_if_needed()
        print("\nSetup Done")

    def tearDown(self):
        os.close(self.db_fd)
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

if __name__ == "__main__":
    unittest.main()