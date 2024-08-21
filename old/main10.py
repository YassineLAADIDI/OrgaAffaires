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

        if login == "aa" and password == "aa":
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

        btn_logout = tk.Button(self, text="Déconnexion", command=self.logout)
        btn_logout.pack(pady=10)
    
        btn_ajouter_entite = tk.Button(self, text="Ajouter une entité", command=self.ajouter_entite)
        btn_ajouter_entite.pack()

        # Nouveau bouton "Ajouter un utilisateur"
        btn_ajouter_user = tk.Button(self, text="Ajouter un utilisateur", command=self.ajouter_utilisateur)
        btn_ajouter_user.pack()

    def ajouter_utilisateur(self):
        self.user_window = tk.Toplevel(self)
        self.user_window.title("Ajouter un nouvel utilisateur")
        self.user_window.geometry("400x300")

        tk.Label(self.user_window, text="Code utilisateur").grid(row=0, column=0)
        tk.Label(self.user_window, text="Nom").grid(row=1, column=0)
        tk.Label(self.user_window, text="Prénom").grid(row=2, column=0)
        tk.Label(self.user_window, text="Email").grid(row=3, column=0)
        tk.Label(self.user_window, text="Entité").grid(row=4, column=0)

        code_var = tk.StringVar()
        nom_var = tk.StringVar()
        prenom_var = tk.StringVar()
        mail_var = tk.StringVar()
        entite_var = tk.StringVar()

        tk.Entry(self.user_window, textvariable=code_var).grid(row=0, column=1)
        tk.Entry(self.user_window, textvariable=nom_var).grid(row=1, column=1)
        tk.Entry(self.user_window, textvariable=prenom_var).grid(row=2, column=1)
        tk.Entry(self.user_window, textvariable=mail_var).grid(row=3, column=1)
        
        entite_dropdown = ttk.Combobox(self.user_window, textvariable=entite_var, values=list(self.organisation.entites.keys()))
        entite_dropdown.grid(row=4, column=1)

        def save_new_user():
            code = code_var.get()
            nom = nom_var.get()
            prenom = prenom_var.get()
            mail = mail_var.get()
            entite_code = entite_var.get()

            if code and nom and prenom and mail and entite_code:
                entite = self.organisation.entites.get(entite_code)
                if entite:
                    user = User(code, entite, nom, prenom, mail)
                    self.organisation.users[code] = user

                    self.user_window.destroy()
                else:
                    messagebox.showerror("Erreur", "L'entité sélectionnée n'existe pas.")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

        tk.Button(self.user_window, text="Ajouter", command=save_new_user).grid(row=5, column=1)
        self.center_window(self.user_window, 400, 300)

if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.mainloop()
