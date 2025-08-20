
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import unittest
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))) + '/server')

from server.model.user.user_models import User
from server.model.user.user_manager import UserManager

class ServerTests(unittest.TestCase):
    user_manager: UserManager
    engine = None

    def setUp(self):
        if os.path.exists('test.db'):
            os.remove('test.db')
        self.engine = create_engine("sqlite:///test.db", echo=True)
        User.metadata.create_all(self.engine)
        self.user_manager = UserManager(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_create_user(self):

        self.user_manager.add_user('Anna', 'efwef')

        user = self.user_manager.get_all_users()[0]
        self.assertEqual('Anna', user.user_name)
        self.assertEqual('efwef', user.password)

    def test_create_user_bad_name1(self):
        with self.assertRaises(ValueError):
            self.user_manager.add_user('', 'efwef')

    def test_create_user_bad_name2(self):
        with self.assertRaises(ValueError):
            self.user_manager.add_user(' ', 'efwef')

    def test_create_user_bad_name3(self):
        with self.assertRaises(ValueError):
            self.user_manager.add_user(None, 'efwef')

    def test_create_user_bad_pwd1(self):
        with self.assertRaises(ValueError):
            self.user_manager.add_user('Anna', '')

    def test_create_user_bad_pwd1(self):
        with self.assertRaises(ValueError):
            self.user_manager.add_user('Anna', '  ')

    def test_create_duplicate_user(self):
        self.user_manager.add_user('Bob', 'efwef')
        with self.assertRaises(ValueError):
            self.user_manager.add_user('Bob', 'efwef')

    def test_get_user_by_name(self):
        self.user_manager.add_user('Bob', 'wefwrg')
        user = self.user_manager.get_user_by_name('Bob')
        self.assertEqual('Bob', user.user_name)
        with self.assertRaises(Exception):
            self.user_manager.get_user_by_name('Anna')

    def test_get_all_users(self):
        count = len(self.user_manager.get_all_users())
        self.assertEqual(0, count)
        self.user_manager.add_user('Anna', 'wefwrg')
        self.user_manager.add_user('Tom', 'wefwrg')
        self.user_manager.add_user('Bob', 'wefwrg')
        count = len(self.user_manager.get_all_users())
        self.assertEqual(3, count)

    def test_delete_user(self):
        self.user_manager.add_user('Anna', 'wefwrg')
        self.user_manager.add_user('Tom', 'wefwrg')
        self.user_manager.add_user('Bob', 'wefwrg')

        self.user_manager.delete_user('Anna')
        users = self.user_manager.get_all_users()
        user_names = [user.user_name for user in users]
        self.assertIn('Bob', user_names)
        self.assertIn('Tom', user_names)
        self.assertNotIn('Anna', user_names)


if __name__ == '__main__':
    # THIS ALLOWS 'should_*' pattern instead of 'test_*'
    # def load_should_tests():
    #    loader = unittest.TestLoader()
    #    loader.testMethodPrefix = "should"
    #    suite = loader.loadTestsFromTestCase(ServerTests)
    #    return suite
    # runner = unittest.TextTestRunner()
    # runner.run(load_should_tests())
    unittest.main()
