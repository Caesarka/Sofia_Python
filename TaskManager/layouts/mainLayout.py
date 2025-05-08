from tkinter import LabelFrame, Frame
from components.ui.uiTaskCreator import UiTaskCreator
from components.ui.uiTask import UiTask

from models.crud import readBD

class MainLayout:
    def __init__(self, root):
        self.frame_tasks = Frame()

        self.frame = LabelFrame(root, text='Add new task')
        self.taskCreator = UiTaskCreator(self.frame)
        self.tasks = []

    def render(self):
        self.render_tasks()
        self.taskCreator.render()
        self.frame_tasks.pack()
        self.frame.pack()

    def render_tasks(self):
        data = readBD()
        
        if data:
            for d in data:
                task = UiTask(self.frame_tasks, d)
                self.tasks.append(task)
                task.render()
