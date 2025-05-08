from tkinter import Tk, Entry, Text, LabelFrame, Button
from models.crud import updateDB_new


class ModalWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Add task")

        self.lbl_task_title = LabelFrame(self, text="Add task title")
        self.task_title = Entry(self.lbl_task_title)

        self.lbl_task_description = LabelFrame(self, text="Add task description")
        self.task_description = Text(self.lbl_task_description)

        self.btn_add_task = Button(self, text="Add task", command=self.create_task)

        self.lbl_task_title.pack()
        self.task_title.pack()
        self.lbl_task_description.pack()
        self.task_description.pack()
        self.btn_add_task.pack()

    def create_task(self):
        task_title = self.task_title.get()
        task_description = self.task_description.get('1.0', 'end').rstrip('\n')
        updateDB_new(
#          "title" : task_title,
#          "description" : task_description
            task_title, task_description
        )
        self.destroy()