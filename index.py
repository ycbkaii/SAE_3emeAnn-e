from typing import Tuple
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PCA import acpReco
from embeddings.embeddingsController import book_sim_by_id
from get_saga import getSagaById
from inputData_outputCluster import acmReco
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query

from deps import SessionDep
from models import User, _livre
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


 
@app.get("/livres/similaire/{book_id}")
def get_recommended_genres(book_id):
     recommended = get_reco_books(book_id)
     return recommended

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