import tkinter as tk
from tkinter import ttk, messagebox
from Modele import *

# Classe pour instancier la fenêtre de connexion
class Connexion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.geometry("300x150")

        tk.Label(self, text="Login:").pack(pady=5)
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()

        tk.Label(self, text="Mot de passe:").pack(pady=5)
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Se connecter", command=self.checkLogin)
        self.login_button.pack(pady=10)

    # Valider login et mot de passe
    def checkLogin(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        if login == "aa" and password == "aa":
            self.chargerApp()
        else:
            messagebox.showerror("Erreur", "Login ou mot de passe incorrect")

    # Fermer la fenêtre de connexion, instancier le réseau et charger les 3 CSV pour lancer la fenêtre principale avec la structure de l'organisation passée en paramètre
    def chargerApp(self):
        self.destroy()
        org = ReseauOrga()
        org.chargerEntitesCSV('entites.csv')
        org.chargerOrgaCSV('orgas.csv')
        org.chargerUsersCSV('users.csv')
        app = Application(org)
        app.mainloop()

    def centrerFenetre(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")


# Classe d'application principale avec la structure de l'organisation passée en paramètre
class Application(tk.Tk):
    def __init__(self, ReseauOrga):
        super().__init__()
        self.title("ReseauOrga Viewer")
        self.geometry("800x600")
        self.ReseauOrga = ReseauOrga
        self.createWidgets()

    # Crée les widgets de l'interface, y compris le Treeview pour afficher la hiérarchie et les boutons.
    def createWidgets(self):
        self.lbl_title = tk.Label(self, text="ReseauOrga Structure")
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

        self.tree.bind("<Button-3>", self.cliquerDroite)

        self.afficherHierarchie()

        btn_refresh = tk.Button(self, text="Rafraîchir", command=self.actualiser)
        btn_refresh.pack(side=tk.LEFT, padx=5, pady=2)

        # Bouton de déconnexion
        btn_sortir = tk.Button(self, text="Déconnexion", command=self.sortir)
        btn_sortir.pack(side=tk.RIGHT, padx=5, pady=2)

        # Bouton "Ajouter une entité"
        btn_ajouter = tk.Button(self, text="Ajouter une entité", command=self.ajouterEntite)
        btn_ajouter.pack(side=tk.LEFT, padx=5, pady=2)

        # Nouveau bouton "Ajouter un utilisateur"
        btn_ajouter_user = tk.Button(self, text="Ajouter un utilisateur", command=self.ajouterUser)
        btn_ajouter_user.pack(side=tk.LEFT, padx=5, pady=2)

        # Bouton pour lister les utilisateurs
        btn_list_users = tk.Button(self, text="Lister les utilisateurs", command=self.listerUtilisateurs)
        btn_list_users.pack(side=tk.LEFT, padx=5, pady=2)

        # Bouton pour exporter la hiérarchie
        btn_exporter = tk.Button(self, text="Exporter", command=self.exporterHierarchie)
        btn_exporter.pack(side=tk.LEFT, padx=5, pady=2)

    def exporterHierarchie(self):
        try:
            self.ReseauOrga.exportOrgaCSV()
            messagebox.showinfo("Succès", "Hiérarchie exportée avec succès dans 'resultat.csv'")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {str(e)}")

    def listerUtilisateurs(self):
        # Créer une nouvelle fenêtre pour afficher la liste des utilisateurs
        list_window = tk.Toplevel(self)
        list_window.title("Liste des utilisateurs")
        list_window.geometry("600x400")

        # Créer le widget Treeview pour afficher les utilisateurs sous forme de tableau
        tree_users = ttk.Treeview(list_window)
        tree_users.pack(fill=tk.BOTH, expand=True)

        # Définir les colonnes
        tree_users['columns'] = ("Nom", "Prénom", "Email", "Entité")

        # Configurer les colonnes
        tree_users.column("#0", width=0, stretch=tk.NO)  # On cache la première colonne implicite
        tree_users.column("Nom", anchor=tk.W, width=150)
        tree_users.column("Prénom", anchor=tk.W, width=150)
        tree_users.column("Email", anchor=tk.W, width=200)
        tree_users.column("Entité", anchor=tk.W, width=100)

        # Définir les en-têtes de colonnes
        tree_users.heading("#0", text="", anchor=tk.W)
        tree_users.heading("Nom", text="Nom", anchor=tk.W)
        tree_users.heading("Prénom", text="Prénom", anchor=tk.W)
        tree_users.heading("Email", text="Email", anchor=tk.W)
        tree_users.heading("Entité", text="Entité", anchor=tk.W)

        # Insérer les données des utilisateurs dans le tableau
        for user in self.ReseauOrga.users.values():
            entite_code = user.getEntite().getCode() if user.getEntite() else "Aucune entité"
            tree_users.insert("", "end", values=(user.getNom(), user.getPrenom(), user.getMail(), entite_code))

        # Centrer la fenêtre sur l'écran
        self.centrerFenetre(list_window, 600, 400)

    def ajouterUser(self):
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

        entite_dropdown = ttk.Combobox(self.user_window, textvariable=entite_var, values=list(self.ReseauOrga.entites.keys()))
        entite_dropdown.grid(row=4, column=1)

        def sauvegarderUser():
            code = code_var.get()
            nom = nom_var.get()
            prenom = prenom_var.get()
            mail = mail_var.get()
            entite_code = entite_var.get()

            if code and nom and prenom and mail and entite_code:
                entite = self.ReseauOrga.entites.get(entite_code)
                if entite:
                    user = User(code, entite, nom, prenom, mail)
                    self.ReseauOrga.users[code] = user

                    self.user_window.destroy()
                else:
                    messagebox.showerror("Erreur", "L'entité sélectionnée n'existe pas.")
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

        tk.Button(self.user_window, text="Ajouter", command=sauvegarderUser).grid(row=5, column=1)
        self.centrerFenetre(self.user_window, 400, 300)

    def ajouterEntite(self):
        self.ajout_window = tk.Toplevel(self)
        self.ajout_window.title("Ajouter une nouvelle entité")
        self.ajout_window.geometry("400x300")

        tk.Label(self.ajout_window, text="Code").grid(row=0, column=0)
        tk.Label(self.ajout_window, text="Ville").grid(row=1, column=0)
        tk.Label(self.ajout_window, text="Adresse").grid(row=2, column=0)
        tk.Label(self.ajout_window, text="Nature").grid(row=3, column=0)
        tk.Label(self.ajout_window, text="Code du parent").grid(row=4, column=0)

        code_var = tk.StringVar()
        ville_var = tk.StringVar()
        addr_var = tk.StringVar()
        nature_var = tk.StringVar()
        parent_var = tk.StringVar()

        tk.Entry(self.ajout_window, textvariable=code_var).grid(row=0, column=1)
        tk.Entry(self.ajout_window, textvariable=ville_var).grid(row=1, column=1)
        tk.Entry(self.ajout_window, textvariable=addr_var).grid(row=2, column=1)
        tk.Entry(self.ajout_window, textvariable=nature_var).grid(row=3, column=1)
        tk.Entry(self.ajout_window, textvariable=parent_var).grid(row=4, column=1)

        def sauvegarderEntite():
            code = code_var.get()
            ville = ville_var.get()
            addr = addr_var.get()
            nature = nature_var.get()
            parent_code = parent_var.get()

            if code and ville and addr and nature:
                entite = Entite(code, ville, addr, nature)
                parent_orga = self.ReseauOrga.orgas.get(parent_code)
                niveau = parent_orga.niveau + 1 if parent_orga else 0
                orga = Orga(left=0, right=0, niveau=niveau, entite=entite, parent=parent_orga)

                if parent_orga:
                    parent_orga.ajouterEnfant(orga)
                self.ReseauOrga.entites[code] = entite
                self.ReseauOrga.orgas[code] = orga

                self.actualiser()
                self.ajout_window.destroy()
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

        tk.Button(self.ajout_window, text="Ajouter", command=sauvegarderEntite).grid(row=5, column=1)
        self.centrerFenetre(self.ajout_window, 400, 300)

    def afficherHierarchie(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for orga in self.ReseauOrga.orgas.values():
            if orga.parent is None:
                self.insererElement("", orga)

    def insererElement(self, parent, orga):
        node_id = self.tree.insert(parent, "end", text=orga.entite.getCode(),
                                   values=(orga.entite.getVille(), orga.niveau))
        self.tree.item(node_id, tags=(orga.entite.getCode(),))
        for child in orga.enfants:
            self.insererElement(node_id, child)

    def cliquerDroite(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Afficher", command=self.afficherDetails)
            menu.add_command(label="Modifier", command=self.modifierElement)
            menu.add_command(label="Supprimer", command=self.supprimerElement)
            menu.post(event.x_root, event.y_root)

    def afficherDetails(self):
        selected_item = self.tree.selection()[0]
        orga = self.getOrgaByElement(selected_item)
        details = f"Code: {orga.entite.getCode()}\nVille: {orga.entite.getVille()}\nAdresse: {orga.entite.getAddr()}\nNature: {orga.entite.getNature()}"
        user = self.getUserByEntite(orga.entite.getCode())
        if user:
            details += f"\n\nResponsable: {user.getNom()} {user.getPrenom()}\nEmail: {user.getMail()}"

        detail_window = tk.Toplevel(self)
        detail_window.title("Détails de l'entité")
        label = tk.Label(detail_window, text=details, justify=tk.LEFT)
        label.pack(padx=20, pady=20)
        self.centrerFenetre(detail_window, 300, 200)

    def modifierElement(self):
        selected_item = self.tree.selection()[0]
        orga = self.getOrgaByElement(selected_item)

        self.mod_window = tk.Toplevel(self)
        self.mod_window.title("Modifier l'entité")
        self.mod_window.geometry("400x300")

        tk.Label(self.mod_window, text="Code").grid(row=0, column=0)
        tk.Label(self.mod_window, text="Ville").grid(row=1, column=0)
        tk.Label(self.mod_window, text="Adresse").grid(row=2, column=0)
        tk.Label(self.mod_window, text="Nature").grid(row=3, column=0)

        code_var = tk.StringVar(value=orga.entite.getCode())
        ville_var = tk.StringVar(value=orga.entite.getVille())
        addr_var = tk.StringVar(value=orga.entite.getAddr())
        nature_var = tk.StringVar(value=orga.entite.getNature())

        tk.Entry(self.mod_window, textvariable=code_var).grid(row=0, column=1)
        tk.Entry(self.mod_window, textvariable=ville_var).grid(row=1, column=1)
        tk.Entry(self.mod_window, textvariable=addr_var).grid(row=2, column=1)
        tk.Entry(self.mod_window, textvariable=nature_var).grid(row=3, column=1)

        def sauvegarderModifs():
            old_code = orga.entite.getCode()
            orga.entite.setCode(code_var.get())
            orga.entite.setVille(ville_var.get())
            orga.entite.setAddr(addr_var.get())
            orga.entite.setNature(nature_var.get())

            if old_code != orga.entite.getCode():
                self.ReseauOrga.orgas[orga.entite.getCode()] = self.ReseauOrga.orgas.pop(old_code)

            self.actualiser()
            self.mod_window.destroy()

        tk.Button(self.mod_window, text="Sauvegarder", command=sauvegarderModifs).grid(row=4, column=1)
        self.centrerFenetre(self.mod_window, 400, 300)

    def supprimerElement(self):
        selected_item = self.tree.selection()[0]
        orga = self.getOrgaByElement(selected_item)
        if orga.parent:
            orga.parent.enfants.remove(orga)
        else:
            del self.ReseauOrga.orgas[orga.entite.getCode()]
        self.actualiser()

    def getOrgaByElement(self, item):
        code = self.tree.item(item, "text")
        return self.ReseauOrga.orgas.get(code)

    def getUserByEntite(self, entite_code):
        for user in self.ReseauOrga.users.values():
            if user.getEntite().getCode() == entite_code:
                return user
        return None

    def actualiser(self):
        self.afficherHierarchie()

    def sortir(self):
        self.destroy()  # Ferme la fenêtre principale
        login_window = Connexion()
        login_window.mainloop()

    def centrerFenetre(self, window, width, height):
        window.update_idletasks()
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
