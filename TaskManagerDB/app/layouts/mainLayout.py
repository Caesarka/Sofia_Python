from tkinter import LabelFrame, Frame, Button
from components.ui.uiTaskCreator import UiTaskCreator
from components.ui.uiTask import UiTask

from crud import readBD

class MainLayout:
    def __init__(self, root):
        self.frame_tasks = Frame()

        self.frame = LabelFrame(root, text='Add new task')
        self.refresh_frame = LabelFrame(root, text='Refresh')
        self.btn_refresh = Button(self.refresh_frame, text='Refresh', command=self.refresh)
        self.taskCreator = UiTaskCreator(self.frame, self)
        self.tasks = []

    def render(self):
        self.render_tasks()
        self.taskCreator.render()
        self.frame_tasks.pack()
        self.frame.pack()
        self.refresh_frame.pack()
        self.btn_refresh.pack()

    def render_tasks(self):
        data = readBD()
        
        if data:
            for d in data:
                task = UiTask(self.frame_tasks, d)
                self.tasks.append(task)
                task.render()
    
    def render_task(self, data):
        task = UiTask(self.frame_tasks, data)
        self.tasks.append(task)
        task.render()

    def refresh(self):
        
        self.render_tasks()