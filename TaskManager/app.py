import tkinter
from layouts.mainLayout import MainLayout

from models.crud import createBD

createBD()
root = tkinter.Tk()

appLayout = MainLayout(root).render()

root.mainloop()
