
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import unittest
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))) + '/server')

from model.task import Task
from services.task_manager import TaskManager

class TaskManagerTests(unittest.TestCase):
    task_manager: TaskManager
    engine = None

    def setUp(self):
        if os.path.exists('test.db'):
            os.remove('test.db')
        self.engine = create_engine("sqlite:///test.db", echo=True)
        Task.metadata.create_all(self.engine)
        self.task_manager = TaskManager(self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_create_task(self):
        task = Task(title='title', description='description', status='status', priority='priority')
        self.assertEqual(None, task.id)
        task = self.task_manager.add_task(task)
        self.assertEqual(1, task.id)

    def test_create_task_by_fields(self):
        task = self.task_manager.add_task_by_fields('Buy milk', 'Walmart supermarket', 'in progress', 'high')
        self.assertEqual(1, task.id)
        self.assertEqual('Buy milk', task.title)
        self.assertEqual('Walmart supermarket', task.description)
        self.assertEqual('high', task.priority)
        self.assertEqual('in progress', task.status)
        with self.assertRaises(ValueError):
            self.task_manager.add_task_by_fields('Buy milk', 'Walmart supermarket', 'in progress', 'high')

    def test_update_task(self):
        task = self.task_manager.add_task_by_fields('Buy milk', 'Walmart supermarket', 'in progress', 'high')
        self.task_manager.update_task(task.id, 'Buy chocolate milk', 'Walmart supermarket', 'in progress', 'high')
        self.assertEqual(1, task.id)
        self.assertEqual('Buy chocolate milk', task.title)
        self.assertEqual('Walmart supermarket', task.description)
        self.assertEqual('high', task.priority)
        self.assertEqual('in progress', task.status)

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
