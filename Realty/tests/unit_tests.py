import os
import tempfile
import unittest

class UnitTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_works(self):
        self.assertEqual(2*2, 4)

    #def test_fails(self):
    #    self.assertEqual(2*2, 5)

if __name__ == "__main__":
    unittest.main()
