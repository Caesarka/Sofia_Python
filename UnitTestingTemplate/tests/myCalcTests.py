import unittest
import os
import sys

# important - src name matches to production root folder
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "src"))

from utils.myUtils import Calc  # must be after sys.path!

class CalcTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_add(self):
        res = Calc.add(1, 2)
        self.assertEqual(3, res)
