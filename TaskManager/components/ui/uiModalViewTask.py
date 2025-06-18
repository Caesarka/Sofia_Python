from tkinter import Tk, Entry, Text, Label, Button
from models.crud import updateDB_new, readDB_task


class ModalViewTask(Tk):
    def __init__(self, task_id):
        super().__init__()
        self.title("View task")
        self.task_id = task_id
        self.lbl_task_title = Label(self)

        self.lbl_task_description = Label(self)

        self.lbl_task_title.pack()
        self.lbl_task_description.pack()
        
        self.get_description()
    
    def get_description(self):
        self.lbl_task_title.config(text=self.task_id)
        self.lbl_task_description.config(text=readDB_task(self.task_id))
