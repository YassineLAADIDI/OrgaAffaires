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

    def export_to_csv(self, filename='resultat.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Code', 'Ville', 'Adresse', 'Nature', 'Niveau', 'Parent'])
            for orga in self.orgas.values():
                parent_code = orga.parent.entite.code if orga.parent else 'Aucun'
                writer.writerow([orga.entite.code, orga.entite.ville, orga.entite.addr, orga.entite.nature, orga.niveau, parent_code])
