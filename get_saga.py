from urllib.parse import unquote
import psycopg2

from utilities import getBooksById


# Connexion à la base de données
def get_db_connection():
    return psycopg2.connect(
        database="masterbook",
        port="5433",
        user="root",
        host="localhost",
        password="root"
    )

def getSagaById(sagaName : str):
    """ Récupération des livres de la même saga que le livre en entrée"""
    sagaName = unquote(sagaName)

    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Recherche des livres
    cur.execute("SELECT _livre.id_livre FROM masterbook._livre WHERE _livre.nom_de_la_saga = %s", (sagaName,))
    books = cur.fetchall()

    cur.close()
    conn.close()

    print(books)

    return getBooksById(books)