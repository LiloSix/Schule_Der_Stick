import tkinter as tk

# ----------- CONSTANTS ------------

BG_COL = "#EBF2F5"
FONT = "Arial"

FG_LBL_COL = "#0D1F2D"
FG_BTN_COL = "#0D1F2D"
BG_BTN_COL = "#9EA3B0"
HL_COL = "#9EA3B0"

FT_LBL_TITLE = (FONT, 24, "bold")
FT_LBL_DESCR = (FONT, 16, "normal")
FT_LBL_NORM = (FONT, 11, "normal")

FT_BTN_NORM = (FONT, 10, "normal")

WD_TEXTBOXES = 35

# ------------ METHODS -------------


def testing_list():
    for values in range(20):
        lbx_results.insert(tk.END, values)

# --------------- UI ---------------


window = tk.Tk()
window.title("Der Stick")
window.config(bg="#EBF2F5")
window.iconbitmap("images/search-16.ico")

window.columnconfigure([0, 1, 2], minsize=10, weight=1)
window.rowconfigure([0, 1, 2], minsize=10, weight=1)

fr_main = tk.Frame(window, bg=BG_COL, highlightbackground=HL_COL, highlightthickness=1)

fr_main.grid(column=1, row=1, sticky="news")

fr_main.columnconfigure([0, 1, 2, 3, 4, 5], minsize=10)
fr_main.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=10)

# ------------ Widgets ------------

lbl_title = tk.Label(fr_main, text="Der Stick", font=FT_LBL_TITLE, fg=FG_LBL_COL, bg=BG_COL)
lbl_descr = tk.Label(fr_main, text="Unterrichtsvorbereitung", font=FT_LBL_DESCR, fg=FG_LBL_COL, bg=BG_COL)
lbl_search = tk.Label(fr_main, text="Suche", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)
lbl_results = tk.Label(fr_main, text="Ergebnisse", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)

btn_tags = tk.Button(fr_main, text="Stichworte\nbearbeiten", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)
btn_search = tk.Button(fr_main, text="Suche", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL, command=testing_list)
btn_save = tk.Button(fr_main, text="Unterrichtseinheit\nspeichern", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)

ent_search = tk.Entry(fr_main, width=WD_TEXTBOXES, highlightthickness=1, highlightbackground=HL_COL, relief="flat")
lbx_results = tk.Listbox(fr_main, width=WD_TEXTBOXES, height=8, highlightthickness=1, highlightbackground=HL_COL, relief="flat")
lbx_choice = tk.Listbox(fr_main, width=WD_TEXTBOXES, height=8, highlightthickness=1, highlightbackground=HL_COL, relief="flat")

scroll_results = tk.Scrollbar(fr_main)
lbx_results.config(yscrollcommand=scroll_results.set)
scroll_results.config(command=lbx_results.yview)

scroll_choice = tk.Scrollbar(fr_main, highlightthickness=1, highlightbackground=HL_COL)
lbx_choice.config(yscrollcommand=scroll_choice.set)
scroll_choice.config(command=lbx_choice.yview)

fr_choice = tk.Frame(fr_main, bg=BG_COL)

btn_add_files = tk.Button(fr_choice, text="Hinzufügen ->", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)
btn_remove_files = tk.Button(fr_choice, text="<- Entfernen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)

fr_do_not_empty = tk.Frame(fr_main, bg=BG_COL)

lbl_do_not_empty = tk.Label(fr_do_not_empty, text="Ordner vorher nicht leeren", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)
chk_do_not_empty = tk.Checkbutton(fr_do_not_empty, bg= BG_COL, highlightthickness=1, highlightbackground=HL_COL, relief="flat")


# ------------- Layout --------------

lbl_title.grid(row=1, column=1, columnspan=2, sticky="w")
lbl_descr.grid(row=2, column=1, columnspan=3, sticky="w")
lbl_search.grid(row=3, column=1, sticky="nw")
lbl_results.grid(row=4, column=1, sticky="nw")

ent_search.grid(row=3, column=2)
lbx_results.grid(row=4, column=2, sticky="n")
lbx_choice.grid(row=4, column=4, sticky="n")

scroll_results.grid(row=4, column=2, sticky="nes")
scroll_choice.grid(row=4, column=4, sticky="nes")

btn_tags.grid(row=1, column=4, sticky="e")
btn_search.grid(row=3, column=3, pady=5)
btn_save.grid(row=6, column=4, sticky="e")

fr_choice.grid(row=4, column=3, sticky="n", padx=5, pady=5)
btn_add_files.grid(row=0, column=0)
btn_remove_files.grid(row=1, column=0)

fr_do_not_empty.grid(row=5, column=3, columnspan=2, sticky="e")
lbl_do_not_empty.grid(row=0, column=1, sticky="w")
chk_do_not_empty.grid(row=0, column=0, sticky="e")

window.mainloop()