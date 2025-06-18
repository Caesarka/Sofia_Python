from email.mime import text
from models.crud import deleteDB_task
from tkinter import *
from tkinter import Tk
from components.ui.uiModalViewTask import ModalViewTask


class UiTask:
    def __init__(self, root, title):
        self.title = title
        self.var = IntVar()
        self.frame = Frame(root, background='white', padx=5, pady=5)
        self.check_box = Checkbutton(self.frame, text=title, variable=self.var)
        self.btn_remove = Button(
            self.frame, text='Delete', command=self.remove)
        self.btn_show = Button(self.frame, text='Show', command=self.view)

    def render(self):
        self.check_box.grid(column=0, row=0)
        self.btn_remove.grid(column=1, row=0)
        self.btn_show.grid(column=2, row=0)
        self.frame.grid()

    def remove(self):
        self.frame.destroy()
        deleteDB_task(self.title)

    def view(self):
        ModalViewTask(self.title)
