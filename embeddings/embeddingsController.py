from elastic_transport import ObjectApiResponse
from loadSimilarity import kNNBooks,checkClient
from ollama_emb import embedText
from elasticsearchEmbeddings import addBooks,searchBooks
from typing import Any

def object_api_response_to_ids(object_api: ObjectApiResponse[Any]) :
    """ Permet de renvoyer les ids des livres de la réponse d'ES """
    return object_api["hits"]["hits"]

class Books:
    """La classe pour un livre"""
    id : int
    title : str
    desc : str
    genre : str

def add_new_books(books : Books) -> bool :
    # TODO ajouter le livre au SQL
    embedding = embedText(books.desc)["embeddings"][0]
    addBooks(books.desc,embedding,books.title,books.genre,books.id)
    return True

def search_books(title : str) :
    return object_api_response_to_ids(searchBooks(title=title))

def check_client() :
    return checkClient()

def get_reco_books(books_id : int) :
    return object_api_response_to_ids(kNNBooks(books_id))

print(get_reco_books(100))