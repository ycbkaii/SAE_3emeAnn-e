from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from urllib.parse import unquote
import psycopg2

router = APIRouter()

templates = Jinja2Templates(directory="Site")  # Dossier contenant index.html

# Connexion à la base de données
def get_db_connection():
    return psycopg2.connect(
        database="masterbook",
        port="5433",
        user="root",
        host="localhost",
        password="root"
    )

@router.post("/search", response_class=HTMLResponse)
def search_books(query: str = Form(...)):
    """Recherche de livres, auteurs et sagas et affichage sur index.html"""
    results = {"books": [], "authors": [], "sagas": []}

    # On decode l'uriComponent
    query = unquote(query)
    
    conn = get_db_connection()
    cur = conn.cursor()

    
    # Recherche des livres
    cur.execute("""
                SELECT _livre.id_livre, title, description, cover_link, nom_de_la_saga, numéro_opus, _a_ecrit.id_auteur FROM masterbook._livre FULL OUTER JOIN masterbook._a_ecrit ON _livre.id_livre = _a_ecrit.id_livre FULL OUTER JOIN masterbook._auteur ON _auteur.id_auteur = _a_ecrit.id_auteur WHERE title ILIKE %s OR _auteur.nom_complet ILIKE %s OR nom_de_la_saga ILIKE %s
                
                """, (f"%{query}%",f"%{query}%", f"%{query}%"))
    books = cur.fetchall()
    results["books"] = [{"id": b[0], "title": b[1] ,"description": b[2] or "Pas de description", "cover": b[3] or "", "saga" : b[4], "num_opus" : b[5], "id_auteur" : b[6]} for b in books]

    # Recherche des auteurs
    cur.execute("SELECT id_auteur, nom_complet, review_count, average_rating FROM masterbook._auteur WHERE nom_complet ILIKE %s", (f"%{query}%",))
    authors = cur.fetchall()
    results["authors"] = [{"id": a[0], "name": a[1], 'reviews' : a[2], 'avg_rating' : a[3]} for a in authors]

    # Recherche des sagas
    cur.execute("SELECT nom_de_la_saga FROM masterbook._saga WHERE nom_de_la_saga ILIKE %s", (f"%{query}%",))
    sagas = cur.fetchall()
    results["sagas"] = [{"name": s[0]} for s in sagas]

    cur.close()
    conn.close()

    return results