import csv

class Entite:
    def __init__(self, code, ville, addr, nature):
        self.code = code
        self.ville = ville
        self.addr = addr
        self.nature = nature

class Orga:
    def __init__(self, left, right, niveau, entite, parent):
        self.left = left
        self.right = right
        self.niveau = niveau
        self.entite = entite
        self.parent = parent
        self.enfants = []

    def add_child(self, child):
        self.enfants.append(child)

class User:
    def __init__(self, code, entite, nom, prenom, mail):
        self.code = code
        self.entite = entite
        self.nom = nom
        self.prenom = prenom
        self.mail = mail

class Organisation:
    def __init__(self):
        self.entites = {}
        self.orgas = {}
        self.users = {}

    def load_entites_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = Entite(row['entite_code'], row['entite_ville'], row['entite_addr'], row['entite_nature'])
                self.entites[entite.code] = entite

    def load_orgas_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = self.entites.get(row['entite_code'])
                parent = self.orgas.get(row['entite_pere_code'])
                orga = Orga(int(row['orga_left']), int(row['orga_right']), int(row['orga_niveau']), entite, parent)
                if parent:
                    parent.add_child(orga)
                self.orgas[entite.code] = orga

    def load_users_from_csv(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = self.entites.get(row['user_entite'])
                user = User(row['user_code'], entite, row['user_nom'], row['user_prenom'], row['user_mail'])
                self.users[user.code] = user

    def get_hierarchy(self):
        hierarchy = []
        for orga in self.orgas.values():
            if orga.parent is None:
                hierarchy.append(self.build_hierarchy(orga, 0))
        return hierarchy

    def build_hierarchy(self, orga, depth):
        result = "  " * depth + f"{orga.entite.code} - {orga.entite.ville} - {orga.niveau}\n"
        for child in orga.enfants:
            result += self.build_hierarchy(child, depth + 1)
        return result

# Interface Graphique
import tkinter as tk
from tkinter import ttk

class Application(tk.Tk):
    def __init__(self, organisation):
        super().__init__()
        self.title("Organisation Viewer")
        self.geometry("800x600")
        self.organisation = organisation

        # Interface components
        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = tk.Label(self, text="Organisation Structure")
        self.lbl_title.pack()

        self.txt_hierarchy = tk.Text(self, wrap=tk.NONE)
        self.txt_hierarchy.pack(fill=tk.BOTH, expand=True)

        btn_refresh = tk.Button(self, text="Afficher la hiérarchie", command=self.display_hierarchy)
        btn_refresh.pack()

    def display_hierarchy(self):
        hierarchy = self.organisation.get_hierarchy()
        self.txt_hierarchy.delete(1.0, tk.END)
        self.txt_hierarchy.insert(tk.END, "".join(hierarchy))

if __name__ == "__main__":
    org = Organisation()
    org.load_entites_from_csv('entites.csv')
    org.load_orgas_from_csv('orgas.csv')
    org.load_users_from_csv('users.csv')

    app = Application(org)
    app.mainloop()
