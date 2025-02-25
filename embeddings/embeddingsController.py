import numpy as np
from elastic_transport import ObjectApiResponse
import psycopg2

from .ollama_emb import embed_text, check_ollama
from .load_recommandation import knn_books, check_client_es, knn_user
from .elasticsearch_embeddings import (
    add_books,
    search_books_by_title,
    recreate_index_desc,
    fill_index_desc,
)
from typing import Any

def object_api_response_to_ids(object_api: ObjectApiResponse[Any]):
    """Permet de renvoyer les ids des livres de la réponse d'ES"""
    return object_api["hits"]["hits"]["_source"]["id"]

class Books:
    """La classe pour un livre"""

    id: int
    title: str
    desc: str
    genre: str


def initialize_elastic_search():
    """Fonction pour initializer ES"""
    recreate_index_desc()
    fill_index_desc(np.array([]))


def init_and_check_ollama():
    """Pour savoir si Ollama marche bien"""
    return {"status": check_ollama()}


def add_new_books(books: Books) -> bool:
    # TODO ajouter le livre au SQL
    embedding = embed_text(books.desc)["embeddings"][0]
    add_books(books.desc, embedding, books.title, books.genre, books.id)
    return True


def search_books(title: str):
    return object_api_response_to_ids(search_books_by_title(title=title))


def check_client():
    return check_client_es()


def get_reco_books(books_id: int):
    return object_api_response_to_ids(knn_books(books_id))


def getBooksByUser(id: int | str) -> list[tuple] | list:
    """
    Fonction pour avoir les livres aimé par les utilisateur
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5432",
            user="root",
            host="localhost",
            password="root",
        )
    except Exception as e:
        conn = None
        print("DATABASE ERROR :", e)
    if conn is not None:
        with conn.cursor() as cursor:
            requete = (
                "SELECT id_livre FROM masterbook._a_lu_livre_vote_genre_pour_livre WHERE note_livre>4 AND id_user="
                + str(id)
            )
            try:
                cursor.execute(requete)
                res = cursor.fetchall()
                return res
            except Exception as e:
                print(e)
                return ()
    else:
        return ()


def get_reco_user_based(id: int):
    listBooks = {}
    for elem in object_api_response_to_ids(knn_user(id)):
        id_usr = elem["_source"]["id"]
        if id_usr != id:
            listBooks[id_usr] = getBooksByUser(id_usr)
    return listBooks
