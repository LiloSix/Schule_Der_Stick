from window_tags import *
from autocomplete_combo import *
import backend as be
import fileutils as fi
from constants import *


class WindowMain:
    def __init__(self, master):
        self.master = master
        self.master.config(bg=BG_COL)
        self.master.iconbitmap("images/search-16.ico")
        self.completion_list = db.tag_hint("")

        master.columnconfigure([0, 1, 2], minsize=10, weight=1)
        master.rowconfigure([0, 1, 2], minsize=10, weight=1)

        fr_main = tk.Frame(master, bg=BG_COL, highlightbackground=HL_COL, highlightthickness=1)

        fr_main.grid(column=1, row=1, sticky="news")

        fr_main.columnconfigure([0, 1, 2, 3, 4, 5], minsize=10)
        fr_main.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=10)

        self.file_list = list()
        self.choice_list = list()

        # ------------ Mainframe Widgets ------------

        lbl_title = tk.Label(fr_main, text="Der Schtick", font=FT_LBL_TITLE, fg=FG_LBL_COL, bg=BG_COL)
        lbl_descr = tk.Label(fr_main, text="Unterrichtsvorbereitung", font=FT_LBL_DESCR, fg=FG_LBL_COL, bg=BG_COL)
        lbl_search = tk.Label(fr_main, text="Suche", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)
        lbl_results = tk.Label(fr_main, text="Ergebnisse", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)
        self.lbl_results_monitor = tk.Label(fr_main, text="Bitte geben Sie ein Stichwort im Suchfeld ein."
                                                          "\nOder mehrere Stichworte mit Komma getrennt.",
                                            font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL,
                                            justify="left")

        btn_tags = tk.Button(fr_main, text="Stichworte\nbearbeiten", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL,
                             bg=BG_BTN_COL,
                             command=self.open_popup)
        btn_search = tk.Button(fr_main, text="Suche", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL,
                               command=self.result_list)
        btn_save = tk.Button(fr_main, text="Unterrichtseinheit\nspeichern", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL,
                             bg=BG_BTN_COL, command=self.save_selection)

        self.search_combo = AutocompleteCombobox(fr_main)
        self.search_combo.set_completion_list(self.completion_list)

        self.search_combo.config(width=WD_TEXTBOXES, postcommand=self.combobox_update)
        self.search_combo.bind('<Return>', self.handler)
        self.search_combo.bind('<<ComboboxSelected>>', )

        # -------------Frame Results -----------

        fr_choice_results = tk.Frame(fr_main, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL)

        self.lbx_results = tk.Listbox(fr_choice_results, width=WD_TEXTBOXES, height=HT_TEXTBOXES, relief="flat",
                                      selectmode="extended")
        scroll_results = tk.Scrollbar(fr_choice_results)
        self.lbx_results.config(yscrollcommand=scroll_results.set)
        scroll_results.config(command=self.lbx_results.yview)

        # ----------Frame Choice Buttons ----------

        fr_choice_btns = tk.Frame(fr_main, height=HT_TEXTBOXES, bg=BG_COL)

        btn_add_files = tk.Button(fr_choice_btns, text="Hinzuf??gen ->", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                                  bg=BG_BTN_COL, command=self.results_to_choice)
        btn_remove_files = tk.Button(fr_choice_btns, text="<- Entfernen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                                     bg=BG_BTN_COL, command=self.remove_from_choice)
        btn_empty_results = tk.Button(fr_choice_btns, text="<- Ergebnisse\nleeren", width=10, font=FT_BTN_NORM,
                                      fg=FG_BTN_COL, bg=BG_BTN_COL, command=self.empty_results)

        # --------------Frame Choice -------------

        fr_choice = tk.Frame(fr_main, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL)

        self.lbx_choice = tk.Listbox(fr_choice, width=WD_TEXTBOXES, height=HT_TEXTBOXES, relief="flat", selectmode="extended")
        scroll_choice = tk.Scrollbar(fr_choice, highlightthickness=1, highlightbackground=HL_COL)
        self.lbx_choice.config(yscrollcommand=scroll_choice.set)
        scroll_choice.config(command=self.lbx_choice.yview)

        # ------Frame Checkbox Do not empty -------

        fr_do_not_empty = tk.Frame(fr_main, bg=BG_COL)
        self.check_delete = tk.IntVar()

        lbl_do_not_empty = tk.Label(fr_do_not_empty, text="Ordner vorher leeren", font=FT_LBL_NORM, fg=FG_LBL_COL,
                                    bg=BG_COL)
        chk_do_not_empty = tk.Checkbutton(fr_do_not_empty, variable=self.check_delete, bg=BG_COL, highlightthickness=1,
                                          highlightbackground=HL_COL,
                                          relief="flat", onvalue=1, offvalue=0)

        # ------------- Layout --------------

        lbl_title.grid(row=1, column=1, columnspan=2, sticky="w")
        lbl_descr.grid(row=2, column=1, columnspan=3, sticky="w")
        lbl_search.grid(row=3, column=1, sticky="nw")
        lbl_results.grid(row=4, column=1, sticky="nw")
        self.lbl_results_monitor.grid(row=5, column=2, rowspan=2, columnspan=2, sticky="wn", pady=(5, 0))

        self.search_combo.grid(row=3, column=2, sticky="w")

        btn_tags.grid(row=1, column=4, sticky="e")
        btn_search.grid(row=3, column=3, pady=5)
        btn_save.grid(row=6, column=4, sticky="e")

        fr_choice_results.grid(row=4, column=2, sticky="nw")
        self.lbx_results.grid(row=0, column=0, sticky="news")
        scroll_results.grid(row=0, column=1, sticky="nes")

        fr_choice_btns.grid(row=4, column=3, sticky="ns", padx=5)
        btn_add_files.pack(side=tk.TOP)
        btn_remove_files.pack(side=tk.TOP)
        btn_empty_results.pack(side=tk.BOTTOM)

        fr_choice.grid(row=4, column=4, sticky="nw")
        self.lbx_choice.grid(row=0, column=0, sticky="news")
        scroll_choice.grid(row=0, column=1, sticky="nes")

        fr_do_not_empty.grid(row=5, column=3, columnspan=2, sticky="e")
        lbl_do_not_empty.grid(row=0, column=1, sticky="w")
        chk_do_not_empty.grid(row=0, column=0, sticky="e")

        # ------------ METHODS -------------

    def open_popup(self):
        popup = tk.Tk()
        popup.title("Stichworte bearbeiten")
        WindowTags(popup)

    def result_list(self):
        self.lbx_results.delete(0, tk.END)
        queries = [i.strip() for i in self.search_combo.get().split(",")]
        self.file_list = be.search(queries)
        counter = 1

        for value in self.file_list:
            filename = f"{counter}: {value.view_name_ui()}"
            counter += 1
            self.lbx_results.insert(tk.END, filename)

        self.update_result_monitor(self.search_combo.get(), len(self.file_list))

    def update_result_monitor(self, search_entry, result_amt):
        self.lbl_results_monitor.config(text=f"Ihre Suche nach '{search_entry} '\nbrachte {result_amt} Ergebnisse")

    def handler(self, e):
        self.result_list()

    def combobox_update(self):
        updted_list = db.tag_hint("")
        self.search_combo['values'] = updted_list

    def results_to_choice(self):
        res_selection = self.lbx_results.curselection()

        for i in res_selection:
            if i not in self.choice_list:
                self.choice_list.append(self.file_list[i])

        self.lbx_choice.delete(0, tk.END)

        for obj in self.choice_list:
            self.lbx_choice.insert(tk.END, f"{obj.id}: {obj.view_name_ui()}")

    def remove_from_choice(self):
        cho_selection = list(self.lbx_choice.curselection())
        cho_selection.reverse()

        while len(cho_selection) > 0:
            self.lbx_choice.delete(cho_selection[0])
            self.choice_list.pop(cho_selection[0])
            cho_selection = list(self.lbx_choice.curselection())

    def empty_results(self):
        self.lbx_results.delete(0, tk.END)

    def save_selection(self):

        id_list = list()

        for obj in self.choice_list:
            id_list.append(obj.id)

        chkbx = self.is_checked()

        self.lbx_results.delete(0, tk.END)
        self.lbx_choice.delete(0, tk.END)
        self.check_delete.set(0)
        self.search_combo.delete(0, tk.END)
        self.lbl_results_monitor.config(text="Bitte geben Sie ein Stichwort im Suchfeld ein."
                                             "\nOder mehrere Stichworte mit Komma getrennt.")

        self.choice_list.clear()
        print(id_list, chkbx)
        be.get_documents(id_list, chkbx)

    def is_checked(self):
        if self.check_delete.get() == 1:
            return True
        else:
            return False
