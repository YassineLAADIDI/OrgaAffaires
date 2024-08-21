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

    def export_to_csv(self, filename='resultat.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Code', 'Ville', 'Adresse', 'Nature', 'Niveau', 'Parent'])
            for orga in self.orgas.values():
                parent_code = orga.parent.entite.code if orga.parent else 'Aucun'
                writer.writerow([orga.entite.code, orga.entite.ville, orga.entite.addr, orga.entite.nature, orga.niveau, parent_code])

    
 
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
        self.title("Réseau des sites et points de vente")
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
        btn_refresh.pack(side=tk.LEFT, padx=5,pady=2)

        # Bouton de déconnexion
        btn_logout = tk.Button(self, text="Déconnexion", command=self.logout)
        btn_logout.pack(side=tk.RIGHT, padx=5,pady=2)
    
        # Bouton "Ajouter une entité"
        btn_ajouter = tk.Button(self, text="Ajouter une entité", command=self.ajouter_entite)
        btn_ajouter.pack(side=tk.LEFT, padx=5,pady=2)

        # Nouveau bouton "Ajouter un utilisateur"
        btn_ajouter_user = tk.Button(self, text="Ajouter un utilisateur", command=self.ajouter_utilisateur)
        btn_ajouter_user.pack(side=tk.LEFT, padx=5,pady=2)

        # Bouton pour lister les utilisateurs
        btn_list_users = tk.Button(self, text="Lister les utilisateurs", command=self.lister_utilisateurs)
        btn_list_users.pack(side=tk.LEFT, padx=5, pady=2)

        # Bouton pour exporter la hiérarchie
        btn_exporter = tk.Button(self, text="Exporter", command=self.exporter_hierarchie)
        btn_exporter.pack(side=tk.LEFT, padx=5, pady=2)

    def exporter_hierarchie(self):
        try:
            self.organisation.export_to_csv()
            messagebox.showinfo("Succès", "Hiérarchie exportée avec succès dans 'resultat.csv'")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation : {str(e)}")
    
    def lister_utilisateurs(self):
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
            for user in self.organisation.users.values():
                entite_code = user.entite.code if user.entite else "Aucune entité"
                tree_users.insert("", "end", values=(user.nom, user.prenom, user.mail, entite_code))

            # Centrer la fenêtre sur l'écran
            self.center_window(list_window, 600, 400)

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
        
    
    def ajouter_entite(self):
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

        def save_new_entity():
            code = code_var.get()
            ville = ville_var.get()
            addr = addr_var.get()
            nature = nature_var.get()
            parent_code = parent_var.get()

            if code and ville and addr and nature:
                entite = Entite(code, ville, addr, nature)
                parent_orga = self.organisation.orgas.get(parent_code)
                niveau = parent_orga.niveau + 1 if parent_orga else 0
                orga = Orga(left=0, right=0, niveau=niveau, entite=entite, parent=parent_orga)
                
                if parent_orga:
                    parent_orga.add_child(orga)
                self.organisation.entites[code] = entite
                self.organisation.orgas[code] = orga

                self.refresh_tree()
                self.ajout_window.destroy()
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

        tk.Button(self.ajout_window, text="Ajouter", command=save_new_entity).grid(row=5, column=1)
        self.center_window(self.ajout_window, 400, 300)

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
