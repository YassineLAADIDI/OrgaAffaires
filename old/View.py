import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Authentification")
        self.geometry("300x150")

        tk.Label(self, text="Login:").pack(pady=5)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        tk.Label(self, text="Mot de passe:").pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Se connecter", command=self.controller.check_login)
        self.login_button.pack(pady=10)

        self.center_window(self, 300, 150)

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

class ApplicationView(tk.Tk):
    def __init__(self, controller, organisation):
        super().__init__()
        self.controller = controller
        self.organisation = organisation
        self.title("Réseau des sites et points de vente")
        self.geometry("800x600")
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

        self.tree.bind("<Button-3>", self.controller.on_right_click)

        btn_refresh = tk.Button(self, text="Rafraîchir", command=self.controller.refresh_tree)
        btn_refresh.pack(side=tk.LEFT, padx=5,pady=2)

        btn_logout = tk.Button(self, text="Déconnexion", command=self.controller.logout)
        btn_logout.pack(side=tk.RIGHT, padx=5,pady=2)
    
        btn_ajouter = tk.Button(self, text="Ajouter une entité", command=self.controller.ajouter_entite)
        btn_ajouter.pack(side=tk.LEFT, padx=5,pady=2)

        btn_ajouter_user = tk.Button(self, text="Ajouter un utilisateur", command=self.controller.ajouter_utilisateur)
        btn_ajouter_user.pack(side=tk.LEFT, padx=5,pady=2)

        btn_list_users = tk.Button(self, text="Lister les utilisateurs", command=self.controller.lister_utilisateurs)
        btn_list_users.pack(side=tk.LEFT, padx=5, pady=2)

        btn_exporter = tk.Button(self, text="Exporter", command=self.controller.exporter_hierarchie)
        btn_exporter.pack(side=tk.LEFT, padx=5, pady=2)

        self.display_hierarchy()

    def display_hierarchy(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for orga in self.organisation.orgas.values():
            if orga.parent is None:
                self.controller.insert_node("", orga)
