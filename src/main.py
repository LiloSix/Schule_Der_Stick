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
        lbx_results.insert(tk.END, f"val: {values}")


def results_to_choice():
    list_result_choices = list()
    selection = lbx_results.curselection()

    for i in selection:
        entry = lbx_results.get(i)
        list_result_choices.append(entry)

    for j in list_result_choices:
        lbx_choice.insert(tk.END, j)


def remove_from_choice():
    val_selection = lbx_choice.curselection()

    print(val_selection)

    while len(val_selection) > 0:
        lbx_choice.delete(val_selection[0])
        val_selection = lbx_choice.curselection()


def save_selection():
    values = lbx_choice.get(0, tk.END)
    chkbx = is_checked()
    lbx_results.delete(0, tk.END)
    lbx_choice.delete(0, tk.END)
    check_delete.set(0)

    print(f"Values ={values}, {chkbx}")


def is_checked():
    if check_delete.get() == 1:
        return "true"
    else:
        return "false"


# -------------Pop-Up---------------
def popup_bonus():
    win = tk.Toplevel()
    win.minsize(200, 150)
    win.wm_title("Stichworte/Tags bearbeiten")

    win.columnconfigure([0, 1, 2], minsize=5, weight=1)
    win.rowconfigure([0, 1, 2], minsize=5, weight=1)


    header = tk.Label(win, text="Stichwort/Tags bearbeiten", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)
    header.grid(row=0, column=0, columnspan=3, sticky="w", padx=3)

    input1 = tk.Entry(win, width=31, highlightthickness=1, highlightbackground=HL_COL, relief="flat")
    input1.grid(row=1, column=0, columnspan=3, sticky="w", padx=5)

    remove = tk.Button(win, text="entfernen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)
    remove.grid(row=2, column=0, sticky="w", padx=5)

    add_tags = tk.Button(win, text="Tag hinzufügen",width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)
    add_tags.grid(row=2, column=1, sticky="e", padx=5)

    update = tk.Button(win, text="Index aktualisieren", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)
    update.grid(row=3, column=0, sticky="w", padx=5, pady=10)

    b = tk.Button(win, text="Schließen", command=win.destroy, width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL)
    b.grid(row=3, column=1, sticky="e", padx=5, pady=10)


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
btn_search = tk.Button(fr_main, text="Suche", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL,
                       command=testing_list)
btn_save = tk.Button(fr_main, text="Unterrichtseinheit\nspeichern", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL,
                     bg=BG_BTN_COL, command=save_selection)

ent_search = tk.Entry(fr_main, highlightthickness=1, highlightbackground=HL_COL, relief="flat")


# -------------Frame Results -----------

fr_choice_results = tk.Frame(fr_main, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL)

lbx_results = tk.Listbox(fr_choice_results, width=WD_TEXTBOXES, height=8, relief="flat", selectmode="multiple")
scroll_results = tk.Scrollbar(fr_choice_results)
lbx_results.config(yscrollcommand=scroll_results.set)
scroll_results.config(command=lbx_results.yview)

# ----------Frame Choice Buttons ----------

fr_choice_btns = tk.Frame(fr_main, bg=BG_COL)

btn_add_files = tk.Button(fr_choice_btns, text="Hinzufügen ->", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                          bg=BG_BTN_COL, command=results_to_choice)
btn_remove_files = tk.Button(fr_choice_btns, text="<- Entfernen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                             bg=BG_BTN_COL, command=remove_from_choice)

# --------------Frame Choice -------------

fr_choice = tk.Frame(fr_main, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL)

lbx_choice = tk.Listbox(fr_choice, width=WD_TEXTBOXES, height=8, relief="flat", selectmode="multiple")
scroll_choice = tk.Scrollbar(fr_choice, highlightthickness=1, highlightbackground=HL_COL)
lbx_choice.config(yscrollcommand=scroll_choice.set)
scroll_choice.config(command=lbx_choice.yview)

# ------Frame Checkbox Do not empty -------

fr_do_not_empty = tk.Frame(fr_main, bg=BG_COL)
check_delete = tk.IntVar()

lbl_do_not_empty = tk.Label(fr_do_not_empty, text="Ordner vorher nicht leeren", font=FT_LBL_NORM, fg=FG_LBL_COL,
                            bg=BG_COL)
chk_do_not_empty = tk.Checkbutton(fr_do_not_empty, variable=check_delete, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL,
                                  relief="flat", onvalue=1, offvalue=0)


# ------------- Layout --------------

lbl_title.grid(row=1, column=1, columnspan=2, sticky="w")
lbl_descr.grid(row=2, column=1, columnspan=3, sticky="w")
lbl_search.grid(row=3, column=1, sticky="nw")
lbl_results.grid(row=4, column=1, sticky="nw")

ent_search.grid(row=3, column=2, sticky="ew")

btn_tags.grid(row=1, column=4, sticky="e")
btn_search.grid(row=3, column=3, pady=5)
btn_save.grid(row=6, column=4, sticky="e")

fr_choice_results.grid(row=4, column=2, sticky="n")
lbx_results.grid(row=0, column=0, sticky="news")
scroll_results.grid(row=0, column=1, sticky="nes")

fr_choice_btns.grid(row=4, column=3, sticky="n", padx=5, pady=5)
btn_add_files.grid(row=0, column=0)
btn_remove_files.grid(row=1, column=0)

fr_choice.grid(row=4, column=4, sticky="n")
lbx_choice.grid(row=0, column=0, sticky="news")
scroll_choice.grid(row=0, column=1, sticky="nes")

fr_do_not_empty.grid(row=5, column=3, columnspan=2, sticky="e")
lbl_do_not_empty.grid(row=0, column=1, sticky="w")
chk_do_not_empty.grid(row=0, column=0, sticky="e")

window.mainloop()