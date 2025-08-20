from tkinter import Tk, Entry, Text, Label, Button
from crud import task_create, task_read


class ModalViewTask(Tk):
    def __init__(self, task):
        super().__init__()
        self.title("View task")
        self.task = task
        self.lbl_task_title = Label(self)

        self.lbl_task_description = Label(self)

        self.lbl_task_title.pack()
        self.lbl_task_description.pack()

        self.get_description()

    def get_description(self):
        self.lbl_task_title.config(text=self.task[1])
        self.lbl_task_description.config(text=self.task[2])
