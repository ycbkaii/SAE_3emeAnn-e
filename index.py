from typing import Tuple
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PCA import acpReco
from embeddings.embeddingsController import book_sim_by_id
from get_saga import getSagaById
from inputData_outputCluster import acmReco
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
import psycopg2
from pydantic import BaseModel
from deps import SessionDep
from models import User, _livre
from typing import Optional
from user import user_router
from admin import admin_router
# from inputData_outputCluster import acmReco
from embeddings.embeddingsController import (
    get_reco_books
)
from utilities import getBooksById,getBooksInfosById, get_books_by_author, getBooksInfosallById, search_books_deux, get_search_suggestions_deux
from recherche import search_books
from recommandation_aleatoire import recommend_genres
from fastapi import Form
from fastapi.templating import Jinja2Templates




description = """
# Comment installer l'api

## Prerequis :

- docker
- python3

Dans le dossier /docker et dans le dossier /bdd_docker, executer la commande :
`docker compose up -d --build`

L'initialisation du système peut prendre plusieurs minutes la premier fois, donc soyez patient

Ensuite dans la raçine (ou il y a index.py) executer les commande :

Uniquement première fois :
  `python -m pip install -r requirements.txt`

`fastapi dev index.py`
"""

app = FastAPI(description=description)


# On mentionne les cors
origins = [
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5174",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="masterbook", 
        user="admin", 
        password="root", 
        host="localhost", 
        port="5433"
    )
    return conn

# Charger le CSS et le JS dans les pages
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="Site")


@app.get("/", response_class=HTMLResponse)
def read_root():
    """La route par def"""
    file_path = "Site/index.html"
    return FileResponse(file_path)

@app.get("/contact", response_class=HTMLResponse)
def get_contact():
    file_path = "Site/contacts.html"
    return FileResponse(file_path)


@app.get("/livres/acm_recom/{user_id}")
def get_books_recom_acm(user_id : int) :
    """Cela renvoie les la liste des livres de recommandation"""
    return acmReco(user_id)

@app.get("/livres/acp_recom/{user_id}")
def get_books_recom_acp(user_id : int) :
    """Cela renvoie les la liste des livres de recommandation en ACP"""
    return acpReco(user_id)

@app.get("/livres/genres/{user_id}")
def get_recommended_genres(user_id):
    recommended = recommend_genres(user_id)
    return recommended

@app.get("/livres/sim/{user_id}")
def get_sim_recom(user_id : int) :
    return book_sim_by_id(user_id)


#@app.get("/livres/genres/{user_id}")
#def get_recommended_genres(user_id):
 #   recommended = recommend_genres(user_id)
  #  return recommended


app.include_router(admin_router)
app.include_router(user_router)

@app.get("/book", response_class=HTMLResponse)
def get_book():
    file_path = "Site/book.html"
    return FileResponse(file_path)

@app.get("/books_list/{books_id}")
def retourne_book(books_id : int) :
    """ Renvoie les recommandations item_base pour le livre d'id {books_id} """
    return getBooksById([books_id])

@app.get("/books_infos_list/{books_id}")
def retourne_book2(books_id : int) :
    return getBooksInfosById([books_id])[0]

@app.get("/books_infos_all_list/{books_id}")
def retourne_book3(books_id : int) :
    return getBooksInfosallById([books_id]) 


@app.get("/books_saga/{sagaName}")
def retourne_saga(sagaName : str) :
    return getSagaById(sagaName)


@app.post("/search", response_class=HTMLResponse)
def search(request : Request,query: str = Form(...)):
    """Route qui redirige vers la recherche"""
    
    return templates.TemplateResponse("recherche.html", {"request": request, "query": query})

@app.get("/api/search_deux")
def search_books_deux_route(query: str = Query(..., min_length=1), type: str = Query("title")):
    """Route API pour la recherche améliorée"""
    return search_books_deux(query, type)

@app.get("/api/search_deux/suggestions")
def get_search_suggestions_deux_route(query: str = Query(..., min_length=1), type: str = Query("title")):
    """Route API pour les suggestions de recherche en temps réel"""
    return get_search_suggestions_deux(query, type)

@app.get("/api/author_books")
def get_books_by_author_route(author_id: int = Query(..., description="ID de l'auteur")):
    """Route API pour récupérer tous les livres écrits par un auteur donné"""
    return get_books_by_author(author_id)

@app.get("/api/moods")
def get_moods():
    """Retourne les moods disponibles"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_selection, nom_humeur FROM masterbook._mood_selection")
    moods = cur.fetchall()
    conn.close()
    return [{"id_selection": mood[0], "nom_humeur": mood[1]} for mood in moods]


@app.get("/api/reading-speeds")
def get_reading_speeds():
    """Retourne les vitesses de lecture disponibles"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_vitesse_lecture, nom_categorie FROM masterbook._vitesse_de_lecture")
    speeds = cur.fetchall()
    conn.close()
    return [{"id_vitesse_lecture": speed[0], "nom_categorie": speed[1]} for speed in speeds]


@app.get("/api/sectors")
def get_sectors():
    """Retourne les secteurs d'activité disponibles"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_secteur, nom_secteur FROM masterbook._secteur_de_travail")
    sectors = cur.fetchall()
    conn.close()
    return [{"id_secteur": sector[0], "nom_secteur": sector[1]} for sector in sectors]


@app.get("/api/genres")
def get_genres():
    """Retourne les genres disponibles"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_genre, nom_genre FROM masterbook._genre")
    genres = cur.fetchall()
    conn.close()
    return [{"id_genre": genre[0], "nom_genre": genre[1]} for genre in genres]


@app.get("/api/book-criteria")
def get_book_criteria():
    """Retourne les critères pour choisir des livres"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_critere, critere FROM masterbook._critere_pour_choisir_livre")
    criteria = cur.fetchall()
    conn.close()
    return [{"id_critere": criterion[0], "critere": criterion[1]} for criterion in criteria]


@app.get("/api/authors")
def get_authors():
    """Retourne les auteurs favoris disponibles"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_auteur, nom_complet FROM masterbook._auteur")
    authors = cur.fetchall()
    conn.close()
    return [{"id_auteur": author[0], "nom_complet": author[1]} for author in authors]

@app.get("/api/preferences")
def get_preferences():
    """Retourne les préférences de lecture disponibles"""
    conn = get_db_connection()
    cur = conn.cursor()

    # Exécution de la requête pour récupérer les préférences de lecture
    cur.execute("SELECT id_preference, preference FROM masterbook._preference_lecture")
    preferences = cur.fetchall()
    
    conn.close()

    # Retourne les préférences sous forme de dictionnaire
    return [{"id_preference": preference[0], "preference": preference[1]} for preference in preferences]

class WishlistRequest(BaseModel):
    id_user: int
    id_livre: int

@app.post("/wishlist/add")
def add_to_wishlist(request: WishlistRequest):
    """Ajouter un livre à la wishlist d'un utilisateur"""

    id_user = request.id_user
    id_livre = request.id_livre
    
    # Connexion à la base de données
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Requête pour ajouter l'enregistrement à la wishlist
    query = """
        INSERT INTO masterbook._est_dans_wishlist (id_user, id_livre)
        VALUES (%s, %s)
        ON CONFLICT (id_user, id_livre) DO NOTHING;  -- Ne rien faire si l'entrée existe déjà
    """
    
    try:
        # Exécution de la requête d'insertion
        cur.execute(query, (id_user, id_livre))
        conn.commit()  # Valider la transaction
        return {"message": "Livre ajouté à la wishlist avec succès"}
    
    except psycopg2.Error as e:
        conn.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=400, detail=f"Erreur SQL : {e.pgcode} - {e.pgerror}")
    
    finally:
        # Fermer les ressources
        cur.close()
        conn.close()

@app.delete("/wishlist/remove")
def remove_from_wishlist(request: WishlistRequest):
    """Supprimer un livre de la wishlist d'un utilisateur"""

    id_user = request.id_user
    id_livre = request.id_livre
    
    # Connexion à la base de données
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Requête pour supprimer l'enregistrement de la wishlist
    query = """
        DELETE FROM masterbook._est_dans_wishlist 
        WHERE id_user = %s AND id_livre = %s;
    """
    
    try:
        # Exécution de la requête de suppression
        cur.execute(query, (id_user, id_livre))
        conn.commit()  # Valider la transaction
        
        # Vérifier si une ligne a été supprimée
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Livre non trouvé dans la wishlist")
        
        return {"message": "Livre supprimé de la wishlist avec succès"}
    
    except psycopg2.Error as e:
        conn.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=400, detail=f"Erreur SQL : {e.pgcode} - {e.pgerror}")
    
    finally:
        # Fermer les ressources
        cur.close()
        conn.close()

@app.get("/wishlist/{id_user}")
def get_wishlist(id_user: int):
    """Récupérer tous les livres dans la wishlist d'un utilisateur"""
    
    # Connexion à la base de données
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Requête pour récupérer les livres de la wishlist
    query = """
        SELECT _livre.id_livre
        FROM masterbook._est_dans_wishlist
        JOIN masterbook._livre ON _livre.id_livre = _est_dans_wishlist.id_livre
        WHERE _est_dans_wishlist.id_user = %s;
    """
    
    try:
        # Exécution de la requête
        cur.execute(query, (id_user,))
        books = cur.fetchall()  # Récupérer tous les résultats
        
        # Vérifier si des livres ont été trouvés
        if not books:
            raise HTTPException(status_code=404, detail="Aucun livre trouvé dans la wishlist")
        
        # Retourner les livres récupérés
        return {"wishlist": [{"id_livre": book[0]} for book in books]}
    
    except psycopg2.Error as e:
        conn.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=400, detail=f"Erreur SQL : {e.pgcode} - {e.pgerror}")
    
    finally:
        # Fermer les ressources
        cur.close()
        conn.close()



class AddBookRequest(BaseModel):
    user_id: int
    book_id: int
    genre_id: int

@app.post("/a_lu/add")
def add_book_to_read(request: AddBookRequest):
    """
    Ajoute un livre à la table _a_lu_livre_vote_genre_pour_livre sans note ni avis.
    """
    try:
        query = """
            INSERT INTO masterbook._a_lu_livre_vote_genre_pour_livre (id_user, id_livre, id_genre)
            VALUES (%s, %s, %s);
        """
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (request.user_id, request.book_id, request.genre_id))
        conn.commit()
        cur.close()
        conn.close()
        return {"message": "Livre ajouté avec succès sans avis."}
    except Exception as e:
        return {"error": f"Erreur lors de l'ajout du livre : {str(e)}"}
    
from pydantic import BaseModel

# Modèle pour la suppression du livre
class RemoveBookRequest(BaseModel):
    user_id: int
    book_id: int
    genre_id: int

@app.delete("/a_lu/remove")
def remove_book_from_read(request: RemoveBookRequest):
    """
    Supprime un livre de la liste '_a_lu_livre_vote_genre_pour_livre' sans modifier la note ni l'avis.
    """
    try:
        query = """
            DELETE FROM masterbook._a_lu_livre_vote_genre_pour_livre
            WHERE id_user = %s AND id_livre = %s AND id_genre = %s;
        """
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, (request.user_id, request.book_id, request.genre_id))
        conn.commit()

        # Vérifier si la suppression a affecté des lignes
        if cur.rowcount == 0:
            return {"error": "Aucun livre trouvé à supprimer."}

        cur.close()
        conn.close()
        return {"message": "Livre supprimé avec succès."}

    except Exception as e:
        return {"error": f"Erreur lors de la suppression du livre : {str(e)}"}

    
class UpdateBookRatingRequest(BaseModel):
    id_user: int
    id_livre: int
    id_genre: int
    note_livre: int
    review: Optional[str] = None  # review est optionnel

@app.post("/a_lu/update-note")
def update_book_rating(request: UpdateBookRatingRequest):
    """Mettre à jour la note et l'avis d'un livre dans la table _a_lu_livre_vote_genre_pour_livre"""
    
    # Validation de la note
    if not (1 <= request.note_livre <= 5):
        raise HTTPException(status_code=400, detail="La note doit être comprise entre 1 et 5")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Requête pour mettre à jour la note et l'avis d'un livre
    query = """
        UPDATE masterbook._a_lu_livre_vote_genre_pour_livre
        SET note_livre = %s, review = %s
        WHERE id_user = %s AND id_livre = %s AND id_genre = %s;
    """
    
    try:
        cur.execute(query, (request.note_livre, request.review, request.id_user, request.id_livre, request.id_genre))
        conn.commit()  # Valider la transaction
        
        # Vérifier si une ligne a été mise à jour
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Livre non trouvé dans la liste de lecture de l'utilisateur")
        
        return {"message": "Note et avis mis à jour avec succès"}
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur de mise à jour : {str(e)}")
    
    finally:
        cur.close()
        conn.close()
        
@app.get("/a_lu/{id_user}")
def get_books_to_read(id_user: int):
    """Récupérer tous les livres de la liste 'a_lu' d'un utilisateur"""
    
    # Connexion à la base de données
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Requête pour récupérer les livres de la liste 'a_lu'
    query = """
        SELECT _livre.id_livre
        FROM masterbook._a_lu_livre_vote_genre_pour_livre
        JOIN masterbook._livre ON _livre.id_livre = _a_lu_livre_vote_genre_pour_livre.id_livre
        WHERE _a_lu_livre_vote_genre_pour_livre.id_user = %s;
    """
    
    try:
        # Exécution de la requête
        cur.execute(query, (id_user,))
        books = cur.fetchall()  # Récupérer tous les résultats
        
        # Vérifier si des livres ont été trouvés
        if not books:
            raise HTTPException(status_code=404, detail="Aucun livre trouvé dans la liste 'a_lu'.")
        
        # Retourner les livres récupérés
        return {"a_lu": [{"id_livre": book[0]} for book in books]}
    
    except psycopg2.Error as e:
        conn.rollback()  # Annuler la transaction en cas d'erreur
        raise HTTPException(status_code=400, detail=f"Erreur SQL : {e.pgcode} - {e.pgerror}")
    
    finally:
        # Fermer les ressources
        cur.close()
        conn.close()