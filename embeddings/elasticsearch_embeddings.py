import numpy as np
from elasticsearch import Elasticsearch
import pandas as pd

ES_URL = "http://localhost:9200"

try:
    client = Elasticsearch(ES_URL)
except Exception as e:
    raise RuntimeError("Can't connect to ES : " + str(e))

index_name_desc = "embeddings-books"


def add_books(desc, vect_desc, title, genre_principal, id_books):
    doc = {
        "id": id_books,
        "description": desc,
        "title": title,
        "genre_principal": genre_principal,
        "description_vector": vect_desc,
    }
    client.index(index=index_name_desc, document=doc)


def recreate_index_desc(index_name=index_name_desc):
    mappings = {
        "properties": {
            "id": {"type": "keyword"},
            "description": {"type": "text", "index": "false"},
            "title": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
            "genre_principal": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}},
            },
            "description_vector": {
                "type": "dense_vector",
                "dims": 1024,
                "index": "true",
                "similarity": "cosine",
                "index_options": {"type": "int8_hnsw"},
            },
        }
    }
    try:
        client.indices.delete(index=index_name)
    except Exception as e:
        print(e)
    client.indices.create(index=index_name, mappings=mappings)
    tab = pd.read_feather("vectDesc1024").to_numpy()
    for i in range(len(tab)):
        add_books(desc="", genre_principal="", id_books=i, title="", vect_desc=tab[i])


def recreateIndexGenre(index_name):
    vectGenreBooks = []
    mappings = {"properties": {"genre_vector": {"type": "dense_vector", "dims": 1024}}}
    try:
        client.indices.delete(index=index_name)
    except Exception as e:
        print(e)
    client.indices.create(index=index_name, mappings=mappings)
    for i in range(len(vectGenreBooks)):
        doc = {"genre_vector": vectGenreBooks[i]}
        resp = client.index(index=index_name, id=i, document=doc)
        print(resp["result"], i)


def add_user(id_usr, vector):
    doc = {"id": id_usr, "user_vector": vector}
    client.index(index="hoe-users", document=doc)


def recreate_index_user(index_name="hoe-users"):
    vectUser = pd.read_csv("./userVectorize.csv", index_col="id_user").to_numpy()
    mappings = {
        "properties": {
            "id": {"type": "keyword"},
            "user_vector": {
                "type": "dense_vector",
                "index": "true",
                "similarity": "cosine",
                "index_options": {"type": "hnsw"},
            },
        }
    }
    try:
        client.indices.delete(index=index_name)
    except Exception as e:
        print(e)
    client.indices.create(index=index_name, mappings=mappings)
    for i in range(len(vectUser)):
        add_user(i, vectUser[i])


def search_books_by_title(title: str):
    """Recherche par titre des livres"""
    query = {"match": {"title": title}}
    return client.search(
        index=index_name_desc,
        query=query,
    )


def fill_index_desc(books_array: np.array, index_name=index_name_desc):
    for book in books_array:
        add_books(
            book["desc"], book["vect_desc"], book["title"], book["genre"], book["id"]
        )


# recreate_index_user()
# recreate_index_desc()
