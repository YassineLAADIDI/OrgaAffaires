import csv
import tkinter as tk
from tkinter import ttk, messagebox

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

        # Create a Treeview widget
        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add columns
        self.tree['columns'] = ("Ville", "Niveau")
        self.tree.column("#0", width=150, minwidth=150)
        self.tree.column("Ville", width=100, minwidth=100)
        self.tree.column("Niveau", width=50, minwidth=50)

        # Define headings
        self.tree.heading("#0", text="Entité", anchor=tk.W)
        self.tree.heading("Ville", text="Dept", anchor=tk.W)
        self.tree.heading("Niveau", text="Niveau", anchor=tk.W)

        self.display_hierarchy()

        # Bind right-click to show details
        self.tree.bind("<Button-3>", self.on_right_click)

    def display_hierarchy(self):
        # Clear the tree first
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Build hierarchy
        for orga in self.organisation.orgas.values():
            if orga.parent is None:
                self.insert_node("", orga)

    def insert_node(self, parent, orga):
        # Insert node into the tree
        node_id = self.tree.insert(parent, "end", text=orga.entite.code,
                                   values=(orga.entite.ville, orga.niveau))

        # Recursively insert children
        for child in orga.enfants:
            self.insert_node(node_id, child)

    def on_right_click(self, event):
        # Get the selected item
        item_id = self.tree.identify_row(event.y)
        if item_id:
            entite_code = self.tree.item(item_id, "text")
            orga = self.organisation.orgas.get(entite_code)
            if orga:
                entite_info = f"Code: {orga.entite.code}\nVille: {orga.entite.ville}\nAdresse: {orga.entite.addr}\nNature: {orga.entite.nature}"
                user = next((u for u in self.organisation.users.values() if u.entite == orga.entite), None)
                if user:
                    user_info = f"User:\nNom: {user.nom}\nPrénom: {user.prenom}\nEmail: {user.mail}"
                    entite_info += f"\n\n{user_info}"
                messagebox.showinfo("Détails de l'entité", entite_info)

if __name__ == "__main__":
    org = Organisation()
    org.load_entites_from_csv('entites.csv')
    org.load_orgas_from_csv('orgas.csv')
    org.load_users_from_csv('users.csv')

    app = Application(org)
    app.mainloop()
