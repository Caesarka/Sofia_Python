from email.mime import text
from tkinter import *
from tkinter import Tk


def remove():
    pass


class UiTask:
    def __init__(self, root, title):
        self.var = IntVar()
        self.frame = Frame(root, background='white', padx=5, pady=5)
        self.check_box = Checkbutton(self.frame, text=title, variable=self.var)
        self.btn_remove = Button(self.frame, text='Delete', command=remove)

    def render(self):
        self.check_box.grid(column=0, row=0)
        self.btn_remove.grid(column=1, row=0)
        self.frame.grid()
