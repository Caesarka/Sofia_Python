import tkinter
from layouts.mainLayout import MainLayout

from crud import create_DB_conn

create_DB_conn()
root = tkinter.Tk()

appLayout = MainLayout(root).render()

root.mainloop()
