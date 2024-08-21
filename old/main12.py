import tkinter as tk
from tkinter import ttk, messagebox

# Classe représentant une entité avec ses attributs
class Entite:
    def __init__(self, code, ville, addr, nature):
        self.code = code
        self.ville = ville
        self.addr = addr
        self.nature = nature

# Classe représentant une organisation avec ses relations hiérarchiques
class Orga:
    def __init__(self, left, right, niveau, entite, parent=None):
        self.left = left
        self.right = right
        self.niveau = niveau
        self.entite = entite
        self.enfants = []
        self.parent = parent

    # Ajouter un enfant à l'organisation actuelle
    def add_child(self, child):
        self.enfants.append(child)

# Classe représentant un utilisateur avec ses attributs
class User:
    def __init__(self, code, entite, nom, prenom, mail):
        self.code = code
        self.entite = entite
        self.nom = nom
        self.prenom = prenom
        self.mail = mail

# Classe représentant l'organisation globale contenant les entités et les utilisateurs
class Organisation:
    def __init__(self):
        self.entites = {}
        self.orgas = {}
        self.users = {}

    # Récupérer la hiérarchie complète des organisations
    def get_hierarchy(self):
        return [orga for orga in self.orgas.values() if orga.parent is None]

# Classe principale de l'application
class OrganisationApp(tk.Tk):
    def __init__(self, organisation):
        super().__init__()
        self.organisation = organisation
        self.title("Organisation")
        self.geometry("800x600")

        # Création du Treeview pour afficher la hiérarchie
        self.tree = ttk.Treeview(self, columns=("Ville", "Niveau"), show='tree headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.heading("#0", text="Code")
        self.tree.heading("Ville", text="Ville")
        self.tree.heading("Niveau", text="Niveau")

        # Boutons pour les actions
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Bouton pour rafraîchir la hiérarchie
        tk.Button(button_frame, text="Rafraîchir", command=self.refresh_tree).pack(side=tk.LEFT)

        # Bouton pour ajouter une entité
        tk.Button(button_frame, text="Ajouter Entité", command=self.ajouter_entite).pack(side=tk.LEFT)

        # Bouton pour ajouter un utilisateur
        tk.Button(button_frame, text="Ajouter Utilisateur", command=self.ajouter_utilisateur).pack(side=tk.LEFT)

        # Bouton pour afficher la liste des utilisateurs
        tk.Button(button_frame, text="Liste des Utilisateurs", command=self.liste_utilisateurs).pack(side=tk.LEFT)

        # Bouton pour déconnecter l'utilisateur
        tk.Button(button_frame, text="Déconnexion", command=self.logout).pack(side=tk.LEFT)

        # Affichage initial de la hiérarchie
        self.display_hierarchy()

        # Bind le clic droit pour afficher un menu contextuel
        self.tree.bind("<Button-3>", self.on_right_click)

    # Méthode pour afficher la liste des utilisateurs
    def liste_utilisateurs(self):
        list_window = tk.Toplevel(self)
        list_window.title("Liste des Utilisateurs")
        list_window.geometry("600x400")

        # Création d'un Treeview pour afficher les utilisateurs
        tree = ttk.Treeview(list_window, columns=("Entité", "Nom", "Prénom", "Email"), show='headings')
        tree.pack(fill=tk.BOTH, expand=True)
        tree.heading("Entité", text="Entité")
        tree.heading("Nom", text="Nom")
        tree.heading("Prénom", text="Prénom")
        tree.heading("Email", text="Email")

        # Ajouter chaque utilisateur dans le Treeview
        for user in self.organisation.users.values():
            tree.insert("", "end", values=(user.entite.code, user.nom, user.prenom, user.mail))

    # Rafraîchir l'arbre de l'organisation
    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())  # Supprimer les éléments actuels
        self.display_hierarchy()  # Réafficher la hiérarchie

    # Déconnexion de l'utilisateur
    def logout(self):
        self.destroy()  # Fermer l'application
        login_window = LoginWindow()  # Retour à la fenêtre de login
        login_window.mainloop()

    # Afficher la hiérarchie des organisations
    def display_hierarchy(self):
        for orga in self.organisation.get_hierarchy():
            self.insert_orga("", orga)

    # Méthode pour insérer les organisations dans le Treeview
    def insert_orga(self, parent, orga):
        node_id = self.tree.insert(parent, "end", text=orga.entite.code, values=(orga.entite.ville, orga.niveau))
        for child in orga.enfants:
            self.insert_orga(node_id, child)

    # Méthode pour le clic droit sur un élément
    def on_right_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Modifier", command=self.modifier_entite)
            menu.add_command(label="Supprimer", command=self.supprimer_entite)
            menu.post(event.x_root, event.y_root)

    # Méthode pour ajouter une entité
    def ajouter_entite(self):
        form_window = tk.Toplevel(self)
        form_window.title("Ajouter une nouvelle entité")
        form_window.geometry("400x300")

        # Champs pour les informations de l'entité
        tk.Label(form_window, text="Code:").pack(pady=5)
        code_entry = tk.Entry(form_window)
        code_entry.pack()

        tk.Label(form_window, text="Ville:").pack(pady=5)
        ville_entry = tk.Entry(form_window)
        ville_entry.pack()

        tk.Label(form_window, text="Adresse:").pack(pady=5)
        addr_entry = tk.Entry(form_window)
        addr_entry.pack()

        tk.Label(form_window, text="Nature:").pack(pady=5)
        nature_entry = tk.Entry(form_window)
        nature_entry.pack()

        tk.Label(form_window, text="Code Entité Parent:").pack(pady=5)
        parent_entry = tk.Entry(form_window)
        parent_entry.pack()

        # Bouton pour soumettre le formulaire
        tk.Button(form_window, text="Ajouter", command=lambda: self.soumettre_nouvelle_entite(form_window, code_entry.get(), ville_entry.get(), addr_entry.get(), nature_entry.get(), parent_entry.get())).pack(pady=10)

        # Centrer la fenêtre sur l'écran
        self.center_window(form_window, 400, 300)

    # Soumettre une nouvelle entité et la rajouter à l'organisation
    def soumettre_nouvelle_entite(self, form_window, code, ville, addr, nature, parent_code):
        if code and ville and addr and nature:
            if code not in self.organisation.entites:
                new_entite = Entite(code, ville, addr, nature)
                self.organisation.entites[code] = new_entite

                # Créer la nouvelle organisation et l'ajouter à l'arbre
                parent = self.organisation.orgas.get(parent_code)
                niveau = parent.niveau + 1 if parent else 0
                new_orga = Orga(left=0, right=0, niveau=niveau, entite=new_entite, parent=parent)

                if parent:
                    parent.add_child(new_orga)

                self.organisation.orgas[code] = new_orga
                self.refresh_tree()  # Rafraîchir l'affichage de l'arbre
                form_window.destroy()  # Fermer la fenêtre de formulaire
            else:
                messagebox.showerror("Erreur", "Le code d'entité existe déjà.")
        else:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")

    # Méthode pour modifier une entité existante
    def modifier_entite(self):
        selected_item = self.tree.selection()[0]
        entite_code = self.tree.item(selected_item, "text")
        entite = self.organisation.entites[entite_code]

        form_window = tk.Toplevel(self)
        form_window.title("Modifier l'entité")
        form_window.geometry("400x300")

        # Champs de formulaire pré-remplis avec les informations actuelles
        tk.Label(form_window, text="Code:").pack(pady=5)
        code_entry = tk.Entry(form_window)
        code_entry.insert(0, entite.code)
        code_entry.pack()

        tk.Label(form_window, text="Ville:").pack(pady=5)
        ville_entry = tk.Entry(form_window)
        ville_entry.insert(0, entite.ville)
        ville_entry.pack()

        tk.Label(form_window, text="Adresse:").pack(pady=5)
        addr_entry = tk.Entry(form_window)
        addr_entry.insert(0, entite.addr)
        addr_entry.pack()

        tk.Label(form_window, text="Nature:").pack(pady=5)
        nature_entry = tk.Entry(form_window)
        nature_entry.insert(0, entite.nature)
        nature_entry.pack()

        # Bouton pour soumettre les modifications
        tk.Button(form_window, text="Modifier", command=lambda: self.soumettre_modifications_entite(form_window, entite, code_entry.get(), ville_entry.get(), addr_entry.get(), nature_entry.get())).pack(pady=10)

        # Centrer la fenêtre sur l'écran
        self.center_window(form_window, 400, 300)

    # Méthode pour soumettre les modifications de l'entité
    def soumettre_modifications_entite(self, form_window, entite, new_code, new_ville, new_addr, new_nature):
        if new_code and new_ville and new_addr and new_nature:
            if new_code == entite.code or new_code not in self.organisation.entites:
                entite.code = new_code
                entite.ville = new_ville
                entite.addr = new_addr
                entite.nature = new_nature
                self.refresh_tree()  # Rafraîchir l'affichage de l'arbre
                form_window.destroy()  # Fermer la fenêtre de formulaire
            else:
                messagebox.showerror("Erreur", "Le code d'entité existe déjà.")
        else:
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")

    # Méthode pour centrer une fenêtre sur l'écran
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

# Classe pour gérer la fenêtre de login
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        # Champs pour le login
        tk.Label(self, text="Nom d'utilisateur:").pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Mot de passe:").pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Bouton pour soumettre le login
        tk.Button(self, text="Se connecter", command=self.login).pack(pady=20)

    # Méthode pour le login
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Vérification des informations de login (exemple simple)
        if username == "aa" and password == "aa":
            self.destroy()  # Fermer la fenêtre de login
            main_window = OrganisationApp(Organisation())  # Ouvrir la fenêtre principale
            main_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

if __name__ == "__main__":
    # Démarrer l'application avec la fenêtre de login
    app = LoginWindow()
    app.mainloop()
