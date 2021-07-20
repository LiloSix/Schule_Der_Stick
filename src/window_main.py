
from window_tags import *
import backend as be
import database as db


class WindowMain:
    def __init__(self, master):
        self.master = master
        self.master.config(bg="#EBF2F5")
        self.master.iconbitmap("images/search-16.ico")

        master.columnconfigure([0, 1, 2], minsize=10, weight=1)
        master.rowconfigure([0, 1, 2], minsize=10, weight=1)

        fr_main = tk.Frame(master, bg=BG_COL, highlightbackground=HL_COL, highlightthickness=1)

        fr_main.grid(column=1, row=1, sticky="news")

        fr_main.columnconfigure([0, 1, 2, 3, 4, 5], minsize=10)
        fr_main.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], minsize=10)

        # ------------ Mainframe Widgets ------------

        lbl_title = tk.Label(fr_main, text="Der Schtick", font=FT_LBL_TITLE, fg=FG_LBL_COL, bg=BG_COL)
        lbl_descr = tk.Label(fr_main, text="Unterrichtsvorbereitung", font=FT_LBL_DESCR, fg=FG_LBL_COL, bg=BG_COL)
        lbl_search = tk.Label(fr_main, text="Suche", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)
        lbl_results = tk.Label(fr_main, text="Ergebnisse", font=FT_LBL_NORM, fg=FG_LBL_COL, bg=BG_COL)

        btn_tags = tk.Button(fr_main, text="Stichworte\nbearbeiten", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL,
                             bg=BG_BTN_COL,
                             command=self.open_popup)
        btn_search = tk.Button(fr_main, text="Suche", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL, bg=BG_BTN_COL,
                               command=self.result_list)
        btn_save = tk.Button(fr_main, text="Unterrichtseinheit\nspeichern", width=15, font=FT_BTN_NORM, fg=FG_BTN_COL,
                             bg=BG_BTN_COL, command=self.save_selection)

        self.ent_search = tk.Entry(fr_main, highlightthickness=1, highlightbackground=HL_COL, relief="flat")

        # -------------Frame Results -----------

        fr_choice_results = tk.Frame(fr_main, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL)

        self.lbx_results = tk.Listbox(fr_choice_results, width=WD_TEXTBOXES, height=HT_LISTBOXES, relief="flat",
                                      selectmode="extended")
        scroll_results = tk.Scrollbar(fr_choice_results)
        self.lbx_results.config(yscrollcommand=scroll_results.set)
        scroll_results.config(command=self.lbx_results.yview)

        # ----------Frame Choice Buttons ----------

        fr_choice_btns = tk.Frame(fr_main, bg=BG_COL)

        btn_add_files = tk.Button(fr_choice_btns, text="Hinzufügen ->", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                                  bg=BG_BTN_COL, command=self.results_to_choice)
        btn_remove_files = tk.Button(fr_choice_btns, text="<- Entfernen", width=10, font=FT_BTN_NORM, fg=FG_BTN_COL,
                                     bg=BG_BTN_COL, command=self.remove_from_choice)

        # --------------Frame Choice -------------

        fr_choice = tk.Frame(fr_main, bg=BG_COL, highlightthickness=1, highlightbackground=HL_COL)

        self.lbx_choice = tk.Listbox(fr_choice, width=WD_TEXTBOXES, height=HT_LISTBOXES, relief="flat", selectmode="extended")
        scroll_choice = tk.Scrollbar(fr_choice, highlightthickness=1, highlightbackground=HL_COL)
        self.lbx_choice.config(yscrollcommand=scroll_choice.set)
        scroll_choice.config(command=self.lbx_choice.yview)

        # ------Frame Checkbox Do not empty -------

        fr_do_not_empty = tk.Frame(fr_main, bg=BG_COL)
        self.check_delete = tk.IntVar()

        lbl_do_not_empty = tk.Label(fr_do_not_empty, text="Ordner vorher nicht leeren", font=FT_LBL_NORM, fg=FG_LBL_COL,
                                    bg=BG_COL)
        chk_do_not_empty = tk.Checkbutton(fr_do_not_empty, variable=self.check_delete, bg=BG_COL, highlightthickness=1,
                                          highlightbackground=HL_COL,
                                          relief="flat", onvalue=1, offvalue=0)

        # ------------- Layout --------------

        lbl_title.grid(row=1, column=1, columnspan=2, sticky="w")
        lbl_descr.grid(row=2, column=1, columnspan=3, sticky="w")
        lbl_search.grid(row=3, column=1, sticky="nw")
        lbl_results.grid(row=4, column=1, sticky="nw")

        self.ent_search.grid(row=3, column=2, sticky="ew")

        btn_tags.grid(row=1, column=4, sticky="e")
        btn_search.grid(row=3, column=3, pady=5)
        btn_save.grid(row=6, column=4, sticky="e")

        fr_choice_results.grid(row=4, column=2, sticky="n")
        self.lbx_results.grid(row=0, column=0, sticky="news")
        scroll_results.grid(row=0, column=1, sticky="nes")

        fr_choice_btns.grid(row=4, column=3, sticky="n", padx=5, pady=5)
        btn_add_files.grid(row=0, column=0)
        btn_remove_files.grid(row=1, column=0)

        fr_choice.grid(row=4, column=4, sticky="n")
        self.lbx_choice.grid(row=0, column=0, sticky="news")
        scroll_choice.grid(row=0, column=1, sticky="nes")

        fr_do_not_empty.grid(row=5, column=3, columnspan=2, sticky="e")
        lbl_do_not_empty.grid(row=0, column=1, sticky="w")
        chk_do_not_empty.grid(row=0, column=0, sticky="e")

        # -----------ATTRIBUTES ------------
    queries = list()
    query_choice = list()

        # ------------ METHODS -------------

    def open_popup(self):
        popup = tk.Tk()
        popup.title("Stichworte bearbeiten")
        window_2 = WindowTags(popup)

    def result_list(self):

        queries = [i.strip() for i in self.ent_search.get().split(",")]
        results = be.search(queries)

        for value in results:
            self.lbx_results.insert(tk.END, value.view_name_ui())

            print(value.id)

    def results_to_choice(self):
        #list_result_choices = list()
        selection = self.lbx_results.curselection()

        for i in selection:
            entry = self.lbx_results.get(i)
            print(i)
            for j in self.queries:
                print(j)
                if entry == j.view_name_ui():
                    self.query_choice.append(j)

        for ii in self.query_choice:
            self.lbx_choice.insert(tk.END, ii.view_name_ui())
            print(ii)

    def remove_from_choice(self):
        val_selection = self.lbx_choice.curselection()

        print(val_selection)

        while len(val_selection) > 0:
            self.lbx_choice.delete(val_selection[0])
            val_selection = self.lbx_choice.curselection()

    def save_selection(self):
        values = self.lbx_choice.get(0, tk.END)
        chkbx = self.is_checked()
        self.lbx_results.delete(0, tk.END)
        self.lbx_choice.delete(0, tk.END)
        self.check_delete.set(0)

        print(f"Values ={values}, Checked: {chkbx}")

    def is_checked(self):
        if self.check_delete.get() == 1:
            return "true"
        else:
            return "false"
