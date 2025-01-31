import numpy as np
from elastic_transport import ObjectApiResponse
from .ollama_emb import embed_text, check_ollama
from .load_recommandation import knn_books, check_client_es
from .elasticsearch_embeddings import (
    add_books,
    search_books_by_title,
    recreate_index_desc,
    fill_index_desc,
)
from typing import Any


def object_api_response_to_ids(object_api: ObjectApiResponse[Any]):
    """Permet de renvoyer les ids des livres de la réponse d'ES"""
    return object_api["hits"]["hits"]


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

def init_and_check_ollama() :
    """Pour savoir si Ollama marche bien """
    return {"status" : check_ollama()}

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
