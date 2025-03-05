from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
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
def search_books(request: Request, query: str = Form(...)):
    """Recherche de livres, auteurs et sagas et affichage sur index.html"""
    results = {"books": [], "authors": [], "sagas": []}

    conn = get_db_connection()
    cur = conn.cursor()

    # Recherche des livres
    cur.execute("SELECT id_livre, title, description, cover_link FROM _livre WHERE title ILIKE %s", (f"%{query}%",))
    books = cur.fetchall()
    results["books"] = [{"id": b[0], "title": b[1], "description": b[2] or "Pas de description", "cover": b[3] or ""} for b in books]

    # Recherche des auteurs
    cur.execute("SELECT id_auteur, nom_complet FROM _auteur WHERE nom_complet ILIKE %s", (f"%{query}%",))
    authors = cur.fetchall()
    results["authors"] = [{"id": a[0], "name": a[1]} for a in authors]

    # Recherche des sagas
    cur.execute("SELECT nom_de_la_saga FROM _saga WHERE nom_de_la_saga ILIKE %s", (f"%{query}%",))
    sagas = cur.fetchall()
    results["sagas"] = [{"name": s[0]} for s in sagas]

    cur.close()
    conn.close()

    return templates.TemplateResponse("index.html", {"request": request, "query": query, "results": results})
