import mysql.connector
import bcrypt

conn = mysql.connector.connect(
    host="localhost",
    user="app",          
    password="app", 
    database="app"
)
cursor = conn.cursor()

# Ajouter un utilisateur avec mot de passe crypté
def ajouter_utilisateur(login, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, hashed_password))
    conn.commit()

# Ajouter un utilisateur pour les tests
ajouter_utilisateur("cc", "cc")

cursor.close()
conn.close()