import os
import tempfile
import unittest
#from app import app
#from db import init_db_if_needed

#class DatabaseTests(unittest.TestCase):
#    def setUp(self):
#        self.db_fd, self.temp_path = tempfile.mkstemp()
#        app.config["TESTING"] = True
#
#        global DB_PATH
#        DB_PATH = self.temp_path
#
#        init_db_if_needed()
#        self.client = app.test_client()
#
#    def tearDown(self):
#        os.close(self.db_fd)
#        os.unlink(self.temp_path)
#    def test_empty_db(self):
#        rv = self.client.get("/realty/")
#        self.assertEqual(rv.status_code, 200)
#        self.assertEqual(rv.get_json(), [])

#if __name__ == "__main__":
#    unittest.main()