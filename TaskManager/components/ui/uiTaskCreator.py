import tkinter
from components.ui.uiTask import UiTask
from components.ui.uiModalAddTask import ModalWindow

# def add():
#
#    ui_task = UiTask(root, 'new_task')
#    ui_task.render()


class UiTaskCreator:

    def __init__(self, frame, main_root):
        self.root = main_root
        self.title_var = tkinter.StringVar(frame, value="Add a task")
        self.frame = tkinter.Frame(frame, background='white', padx=5, pady=5)
        self.btn_add = tkinter.Button(self.frame, text='Add', command=self.add)

    def render(self):
        self.btn_add.grid(column=1, row=0)
        self.frame.grid()

    def add(self):
        # ui_task = UiTask(self.frame, 'new_task')
        # ui_task.render()
        ui_new_task = ModalWindow(self.root)
