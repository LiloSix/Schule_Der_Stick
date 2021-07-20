import tkinter as tk
from constants import *
from window_main import *


root = tk.Tk()
root.title("Der Schtick")

window = WindowMain(root)

#print(window.queries)

if __name__ == "__main__":
    root.mainloop()
