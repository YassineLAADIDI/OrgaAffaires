import csv

# Classes de Modèle

# Classe représentant une entité (site ou point de vente) avec ses attributs
class Entite:
    def __init__(self, code, ville, addr, nature):
        self.code = code
        self.ville = ville
        self.addr = addr
        self.nature = nature

# Classe représentant l'organisation (arbre) avec la position hiérarchique, le niveau; l'element parent et les élements dépendants
class Orga:
    def __init__(self, left, right, niveau, entite, parent):
        self.left = left
        self.right = right
        self.niveau = niveau
        self.entite = entite
        self.parent = parent
        self.enfants = []
    # Ajouter un enfant 
    def ajouterEnfant(self, child):
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
class ReseauOrga:
    def __init__(self):
        self.entites = {}
        self.orgas = {}
        self.users = {}

    # charger les entites
    def chargerEntitesCSV(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = Entite(row['entite_code'], row['entite_ville'], row['entite_addr'], row['entite_nature'])
                self.entites[entite.code] = entite # clé est le code  /valeur est l'instance

    # charger l'organisation des entites
    def chargerOrgaCSV(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = self.entites.get(row['entite_code'])
                parent = self.orgas.get(row['entite_pere_code'])
                orga = Orga(int(row['orga_left']), int(row['orga_right']), int(row['orga_niveau']), entite, parent)
                if parent:
                    parent.ajouterEnfant(orga)
                self.orgas[entite.code] = orga # clé est le code  /valeur est l'instance

    # charger les utilisateurs
    def chargerUsersCSV(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = self.entites.get(row['user_entite'])
                user = User(row['user_code'], entite, row['user_nom'], row['user_prenom'], row['user_mail'])
                self.users[user.code] = user # clé est le code  /valeur est l'instance

    # Construit une représentation textuelle de l'arborescence à partir d'une organisation donnée, en ajoutant des indentations selon le niveau 
    def buildOrga(self, orga, niv):
        result = "  " * niv + f"{orga.entite.code} - {orga.entite.ville} - {orga.niveau}\n"
        for e in orga.enfants:
            result += self.buildOrga(e, niv + 1)
        return result
    
    # Renvois arborescence complete de l'organisation
    def getOrgaArb(self):
        orgaArb = []
        for orga in self.orgas.values():
            if orga.parent is None:
                orgaArb.append(self.buildOrga(orga, 0))
        return orgaArb
    # Exporte la hiérarchie actuelle dans un fichier CSV avec les détails de chaque organisation
    def exportOrgaCSV(self, filename='resultat.csv'):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Code', 'Ville', 'Adresse', 'Nature', 'Niveau', 'Parent'])
            for orga in self.orgas.values():
                parent_code = orga.parent.entite.code if orga.parent else 'Aucun'
                writer.writerow([orga.entite.code, orga.entite.ville, orga.entite.addr, orga.entite.nature, orga.niveau, parent_code])
