from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select

from deps import SessionDep
from models import _utilisateur
from user import user_router
from admin import admin_router
# from inputData_outputCluster import acmReco
# from embeddings.embeddingsController import (
#     get_reco_books,
#     get_reco_user_based,
# )

app = FastAPI()

# On mentionne les cors
origins = [
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8080",
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


@app.get("/", response_class=HTMLResponse)
def read_root():
    """La route par def"""
    file_path = "Site/index.html"
    return FileResponse(file_path)

@app.get("/test")
def test(session : SessionDep) :
    statement = select(_utilisateur).where(_utilisateur.id_user == 1)
    session_user = session.exec(statement).first()
    return session_user


# @app.get("/ollama_info")
# def ollama_info():
#     return init_and_check_ollama()


# @app.get("/es_info")
# def elastic_search_info():
#     """Renvoie les infos du clients ElasticSearch"""
#     return check_client_es()


# @app.get("/init_es")
# def init_es():
#     return initialize_elastic_search()


# @app.get("/books/{books_id}")
# def get_reco_books_id(books_id: int):
#     """Renvoie les recommandations item_base pour le livre d'id {books_id}"""
#     return get_reco_books(books_id)


# @app.get("/user/{user_id}")
# def get_user_similar_id(user_id: int):
#     """Renvoie les reco user similaires"""
#     return get_reco_user_based(user_id)


# @app.get("/livres/acm_recom/{user_id}")
# def get_books_recom_acm(user_id : int) :
#     """Cela renvoie les la liste des livres de recommandation"""
#     return acmReco(user_id)


# @app.get("/init")
# def init_ia() :
#     """Route pour init les algorithmes"""

app.include_router(admin_router)
app.include_router(user_router)
