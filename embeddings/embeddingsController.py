import numpy as np
from elastic_transport import ObjectApiResponse
import psycopg2

from utilities import getBooksById

from .load_recommandation import knn_books, check_client_es, knn_user
from .elasticsearch_embeddings import (
    search_books_by_title,
    recreate_index_desc,
)
from typing import Any

def object_api_response_to_ids(object_api: ObjectApiResponse[Any]):
    if "hits" in object_api and "hits" in object_api["hits"]:
        return object_api["hits"]["hits"]
    else:
        print("Structure inattendue dans la réponse Elasticsearch.")
        return []
class Books:
    """La classe pour un livre"""

    id: int
    title: str
    desc: str
    genre: str


def initialize_elastic_search():
    """Fonction pour initializer ES"""
    recreate_index_desc()



def search_books(title: str):
    return object_api_response_to_ids(search_books_by_title(title=title))


def check_client():
    return check_client_es()


def get_reco_books(books_id: int):
    response = knn_books(books_id)
    if response is not None:
        ids = object_api_response_to_ids(response)
        return ids
    else:
        return []


def getBooksByUser(id_user: int | str) -> list[tuple] | list:
    """
    Fonction pour avoir les livres aimé par les utilisateur
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="utilisateur",
            host="localhost",
            password="root",
        )
    except Exception as e:
        conn = None
        print("DATABASE ERROR :", e)
    if conn is not None:
        with conn.cursor() as cursor:
            requete = (
                "SELECT id_livre FROM masterbook._a_lu_livre_vote_genre_pour_livre WHERE id_user="
                + str(id_user)
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


def book_sim_by_id(id_user) :
    livre_aime = getBooksByUser(id_user)
    tuple_books = []
    for i in livre_aime :
        for e in get_reco_books(i[0]) :
            print(e)
            tuple_books.append(e["_source"]["id"])
    tuple_books = list(set(tuple_books))
    tuple_books = tuple_books[1:6]
    print(tuple_books)
    return getBooksById(tuple_books)

def book_sim_by_book(id_book) :
    tuple_books = []
    for e in get_reco_books(id_book) :
        tuple_books.append(e["_source"]["id"])
    tuple_books = list(set(tuple_books))
    tuple_books = tuple_books[1:6]
    return getBooksById(tuple_books)
