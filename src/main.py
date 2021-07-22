import tkinter as tk
from constants import *
import database as db
from window_main import *


root = tk.Tk()
root.title("Der Schtick")

window = WindowMain(root)
completion_list = db.tag_hint("")
window.search_combo.set_completion_list(completion_list)

root.mainloop()
