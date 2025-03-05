from fastapi import APIRouter, Form
import psycopg2

router = APIRouter()

# Connexion à la base de données
def get_db_connection():
    return psycopg2.connect(
        database="masterbook",
        port="5433",
        user="root",
        host="localhost",
        password="root"
    )

@router.post("/search")
def search_books(query: str = Form(...)):
    """Recherche de livres, auteurs et sagas dans la base de données"""
    results = {"books": [], "authors": [], "sagas": []}

    conn = get_db_connection()
    cur = conn.cursor()

    # Recherche des livres
    cur.execute("SELECT id_livre, title, description, cover_link FROM _livre WHERE title ILIKE %s", (f"%{query}%",))
    results["books"] = cur.fetchall()

    # Recherche des auteurs
    cur.execute("SELECT id_auteur, nom_complet FROM _auteur WHERE nom_complet ILIKE %s", (f"%{query}%",))
    results["authors"] = cur.fetchall()

    # Recherche des sagas
    cur.execute("SELECT nom_de_la_saga FROM _saga WHERE nom_de_la_saga ILIKE %s", (f"%{query}%",))
    results["sagas"] = cur.fetchall()

    cur.close()
    conn.close()

    return results
