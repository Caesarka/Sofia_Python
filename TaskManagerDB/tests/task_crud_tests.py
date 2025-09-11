import unittest
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))) + '/server')


import views.crud


class DataAccessTests(unittest.TestCase):

    def test_should_create_task():

