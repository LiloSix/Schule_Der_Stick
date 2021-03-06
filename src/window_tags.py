from window_main import *
from constants import *
import tkinter as tk
import database as db
import backend as be


class WindowTags:
    def __init__(self, master):
        self.master = master
        self.master.minsize(200, 150)
        self.master.config(bg=BG_COL)
        self.master.iconbitmap("images/search-16.ico")

        master.columnconfigure([0, 1, 2, 3], minsize=5, weight=1)
        master.rowconfigure([0, 1, 2, 3, 4, 5], minsize=5, weight=1)

        header = tk.Label(master, text="Stichwort/Tags bearbeiten", font=FT_LBL_DESCR, fg=FG_LBL_COL, bg=BG_COL)
        header.grid(row=1, column=1, columnspan=2, sticky="w")

        self.input1 = tk.Entry(master, highlightthickness=1, highlightbackground=HL_COL, relief="flat")
        self.input1.grid(row=2, column=1, columnspan=2, sticky="we", pady=5, padx=5)

        remove = tk.Button(master, text="entfernen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL,
                           command=self.remove_tag)
        remove.grid(row=3, column=1, sticky="wn", padx=5)

        add_tags = tk.Button(master, text="Tag hinzufügen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL,
                             command=self.add_tag)
        add_tags.grid(row=3, column=2, sticky="en", padx=5)

        update = tk.Button(master, text="Index\naktualisieren", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL,
                           command=self.get_updated)
        update.grid(row=4, column=1, sticky="ws", padx=5)

        b = tk.Button(master, text="Schließen", command=self.master.destroy, width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                      bg=BG_BTN_COL)
        b.grid(row=4, column=2, sticky="es", padx=5)

    def get_updated(self):
        be.update(True)
        test = db.tag_hint("")
        for i in test:
            print(i)

    def add_tag(self):
        tag = self.input1.get()
        db.tag_add(tag)
        self.input1.delete(0, tk.END)

    def remove_tag(self):
        tag = self.input1.get()
        db.tag_remove(tag)
        self.input1.delete(0, tk.END)

