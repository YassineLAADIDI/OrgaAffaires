import tkinter as tk
from tkinter import messagebox
import csv
from Model import Organisation
from View import LoginView, ApplicationView


class Controller:
    def __init__(self):
        self.organisation = Organisation()
        self.login_view = LoginView(self)
        self.login_view.mainloop()

    def check_login(self):
        login = self.login_view.login_entry.get()
        password = self.login_view.password_entry.get()

        if login == "aa" and password == "aa":
            self.open_main_application()
        else:
            messagebox.showerror("Erreur", "Login ou mot de passe incorrect")

    def open_main_application(self):
        self.login_view.destroy()
        self.organisation.load_entites_from_csv('entites.csv')
        self.organisation.load_orgas_from_csv('orgas.csv')
        self.organisation.load_users_from_csv('users.csv')
        self.application_view = ApplicationView(self, self.organisation)
        self.application_view.mainloop()

    def logout(self):
        self.application_view.destroy()
        self.__init__()

    def refresh_tree(self):
        self.application_view.display_hierarchy()

    def insert_node(self, parent, orga):
        node_id = self.application_view.tree.insert(parent, "end", text=orga.entite.code,
                                                     values=(orga.entite.ville, orga.niveau))
        self.application_view.tree.item(node_id, tags=(orga.entite.code,))
        for child in orga.enfants:
            self.insert_node(node_id, child)

    def on_right_click(self, event):
        item = self.application_view.tree.identify_row(event.y)
        if item:
            self.application_view.tree.selection_set(item)
            menu = tk.Menu(self.application_view)
