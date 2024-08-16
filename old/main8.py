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
    
import csv
import tkinter as tk
from tkinter import ttk, messagebox

# Les classes Entite, Orga, User et Organisation restent les mêmes

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Authentification")
        self.geometry("300x150")

        tk.Label(self, text="Login:").pack(pady=5)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        tk.Label(self, text="Mot de passe:").pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Se connecter", command=self.check_login)
        self.login_button.pack(pady=10)

        self.center_window(self, 300, 150)

    def check_login(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login == "admin" and password == "admin":
            self.open_main_application()
        else:
            messagebox.showerror("Erreur", "Login ou mot de passe incorrect")

    def open_main_application(self):
        self.destroy()
        org = Organisation()
        org.load_entites_from_csv('entites.csv')
        org.load_orgas_from_csv('orgas.csv')
        org.load_users_from_csv('users.csv')
        app = Application(org)
        app.mainloop()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

class Application(tk.Tk):
    def __init__(self, organisation):
        super().__init__()
        self.title("Organisation Viewer")
        self.geometry("800x600")
        self.organisation = organisation
        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = tk.Label(self, text="Organisation Structure")
        self.lbl_title.pack()

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree['columns'] = ("Ville", "Niveau")
        self.tree.column("#0", width=150, minwidth=150)
        self.tree.column("Ville", width=100, minwidth=100)
        self.tree.column("Niveau", width=50, minwidth=50)
        self.tree.heading("#0", text="Entité", anchor=tk.W)
        self.tree.heading("Ville", text="Ville", anchor=tk.W)
        self.tree.heading("Niveau", text="Niveau", anchor=tk.W)

        self.tree.bind("<Button-3>", self.on_right_click)

        self.display_hierarchy()

        btn_refresh = tk.Button(self, text="Rafraîchir", command=self.refresh_tree)
        btn_refresh.pack()

        # Bouton de déconnexion
        btn_logout = tk.Button(self, text="Déconnexion", command=self.logout)
        btn_logout.pack(pady=10)

    def display_hierarchy(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for orga in self.organisation.orgas.values():
            if orga.parent is None:
                self.insert_node("", orga)

    def insert_node(self, parent, orga):
        node_id = self.tree.insert(parent, "end", text=orga.entite.code,
                                   values=(orga.entite.ville, orga.niveau))
        self.tree.item(node_id, tags=(orga.entite.code,))
        for child in orga.enfants:
            self.insert_node(node_id, child)

    def on_right_click(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Afficher", command=self.show_details)
            menu.add_command(label="Modifier", command=self.modify_node)
            menu.add_command(label="Supprimer", command=self.delete_node)
            menu.post(event.x_root, event.y_root)

    def show_details(self):
        selected_item = self.tree.selection()[0]
        orga = self.get_orga_by_tree_item(selected_item)
        details = f"Code: {orga.entite.code}\nVille: {orga.entite.ville}\nAdresse: {orga.entite.addr}\nNature: {orga.entite.nature}"
        user = self.get_user_by_entite(orga.entite.code)
        if user:
            details += f"\n\nResponsable: {user.nom} {user.prenom}\nEmail: {user.mail}"

        detail_window = tk.Toplevel(self)
        detail_window.title("Détails de l'entité")
        label = tk.Label(detail_window, text=details, justify=tk.LEFT)
        label.pack(padx=20, pady=20)
        self.center_window(detail_window, 300, 200)

    def modify_node(self):
        selected_item = self.tree.selection()[0]
        orga = self.get_orga_by_tree_item(selected_item)

        self.mod_window = tk.Toplevel(self)
        self.mod_window.title("Modifier l'entité")
        self.mod_window.geometry("400x300")

        tk.Label(self.mod_window, text="Code").grid(row=0, column=0)
        tk.Label(self.mod_window, text="Ville").grid(row=1, column=0)
        tk.Label(self.mod_window, text="Adresse").grid(row=2, column=0)
        tk.Label(self.mod_window, text="Nature").grid(row=3, column=0)

        code_var = tk.StringVar(value=orga.entite.code)
        ville_var = tk.StringVar(value=orga.entite.ville)
        addr_var = tk.StringVar(value=orga.entite.addr)
        nature_var = tk.StringVar(value=orga.entite.nature)

        tk.Entry(self.mod_window, textvariable=code_var).grid(row=0, column=1)
        tk.Entry(self.mod_window, textvariable=ville_var).grid(row=1, column=1)
        tk.Entry(self.mod_window, textvariable=addr_var).grid(row=2, column=1)
        tk.Entry(self.mod_window, textvariable=nature_var).grid(row=3, column=1)

        def save_changes():
            old_code = orga.entite.code
            orga.entite.code = code_var.get()
            orga.entite.ville = ville_var.get()
            orga.entite.addr = addr_var.get()
            orga.entite.nature = nature_var.get()

            if old_code != orga.entite.code:
                self.organisation.orgas[orga.entite.code] = self.organisation.orgas.pop(old_code)

            self.refresh_tree()
            self.mod_window.destroy()

        tk.Button(self.mod_window, text="Sauvegarder", command=save_changes).grid(row=4, column=1)
        self.center_window(self.mod_window, 400, 300)

    def delete_node(self):
        selected_item = self.tree.selection()[0]
        orga = self.get_orga_by_tree_item(selected_item)
        if orga.parent:
            orga.parent.enfants.remove(orga)
        else:
            del self.organisation.orgas[orga.entite.code]
        self.refresh_tree()

    def get_orga_by_tree_item(self, item):
        code = self.tree.item(item, "text")
        return self.organisation.orgas.get(code)

    def get_user_by_entite(self, entite_code):
        for user in self.organisation.users.values():
            if user.entite.code == entite_code:
                return user
        return None

    def refresh_tree(self):
        self.display_hierarchy()

    def logout(self):
        self.destroy()  # Ferme la fenêtre principale
        login_window = LoginWindow()
        login_window.mainloop()

    def center_window(self, window, width, height):
        window.update_idletasks()
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
