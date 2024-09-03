import csv

# Classes de Modèle

# Classe représentant une entité (site ou point de vente) avec ses attributs
class Entite:
    def __init__(self, code, ville, addr, nature):
        self.__code = code
        self.__ville = ville
        self.__addr = addr
        self.__nature = nature

    # Getter et Setter pour chaque attribut
    def getCode(self):
        return self.__code

    def setCode(self, code):
        self.__code = code

    def getVille(self):
        return self.__ville

    def setVille(self, ville):
        self.__ville = ville

    def getAddr(self):
        return self.__addr

    def setAddr(self, addr):
        self.__addr = addr

    def getNature(self):
        return self.__nature

    def setNature(self, nature):
        self.__nature = nature

# Classe représentant un utilisateur avec ses attributs
class User:
    def __init__(self, code, entite, nom, prenom, mail):
        self.__code = code
        self.__entite = entite 
        self.__nom = nom
        self.__prenom = prenom
        self.__mail = mail

    # Getter et Setter pour chaque attribut
    def getCode(self):
        return self.__code

    def setCode(self, code):
        self.__code = code

    def getEntite(self):
        return self.__entite

    def setEntite(self, entite):
        self.__entite = entite

    def getNom(self):
        return self.__nom

    def setNom(self, nom):
        self.__nom = nom

    def getPrenom(self):
        return self.__prenom

    def setPrenom(self, prenom):
        self.__prenom = prenom

    def getMail(self):
        return self.__mail

    def setMail(self, mail):
        self.__mail = mail



# Classe représentant l'organisation (arbre) avec la position hiérarchique, le niveau; l'élément parent et les éléments dépendants
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


        
# Classe représentant l'organisation globale contenant les entités et les utilisateurs
class ReseauOrga:
    def __init__(self):
        self.entites = {}
        self.orgas = {}
        self.users = {}

    # Charger les entités à partir d'un fichier CSV
    def chargerEntitesCSV(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = Entite(row['entite_code'], row['entite_ville'], row['entite_addr'], row['entite_nature'])
                self.entites[entite.getCode()] = entite  # Clé est le code / Valeur est l'instance

    # Charger l'organisation des entités à partir d'un fichier CSV
    def chargerOrgaCSV(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = self.entites.get(row['entite_code'])
                parent = self.orgas.get(row['entite_pere_code'])
                orga = Orga(int(row['orga_left']), int(row['orga_right']), int(row['orga_niveau']), entite, parent)
                if parent:
                    parent.ajouterEnfant(orga)
                self.orgas[entite.getCode()] = orga  # Clé est le code / Valeur est l'instance

    # Charger les utilisateurs à partir d'un fichier CSV
    def chargerUsersCSV(self, filename):
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                entite = self.entites.get(row['user_entite'])
                user = User(row['user_code'], entite, row['user_nom'], row['user_prenom'], row['user_mail'])
                self.users[user.getCode()] = user  # Clé est le code / Valeur est l'instance

    # Construit une représentation textuelle de l'arborescence à partir d'une organisation donnée, en ajoutant des indentations selon le niveau 
    def buildOrga(self, orga, niv):
        result = "  " * niv + f"{orga.entite.getCode()} - {orga.entite.getVille()} - {orga.niveau}\n"
        for e in orga.enfants:
            result += self.buildOrga(e, niv + 1)
        return result
    
    # Renvoie l'arborescence complète de l'organisation
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
                parent_code = orga.parent.entite.getCode() if orga.parent else 'Aucun'
                writer.writerow([orga.entite.getCode(), orga.entite.getVille(), orga.entite.getAddr(), orga.entite.getNature(), orga.niveau, parent_code])
