import numpy as np
from elasticsearch import Elasticsearch
import pandas as pd

ES_URL = "http://my-es-sae:9200"

try:
    client = Elasticsearch(ES_URL)
except Exception as e:
    raise RuntimeError("Can't connect to ES : " + str(e))

index_name_desc = "embeddings-books"


def add_books(vect_desc, id_books):
    doc = {
        "id": id_books,
        "description_vector": vect_desc,
    }
    client.index(index=index_name_desc, document=doc)


def recreate_index_desc(index_name=index_name_desc):
    mappings = {
        "properties": {
            "id": {"type": "keyword"},
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
    df = pd.read_csv("vectDesc1024.csv",index_col="id_livre")
    for index, row in df.iterrows() :
        add_books(id_books=index,vect_desc=row)



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


# recreate_index_user()

if not client.indices.exists(index=index_name_desc) :
    recreate_index_desc()
