from elasticsearch import Elasticsearch
import pandas as pd

client = Elasticsearch("http://localhost:9200")


index_name_desc = "embeddings-books"


def addBooks(desc, vect_desc, title, genre_principal, id):
    doc = {
        "id": id,
        "description": desc,
        "title": title,
        "genre_principal": genre_principal,
        "description_vector": vect_desc,
    }
    client.create(index=index_name_desc, document=doc)


def recreateIndexDesc(index_name):
    vectDescBooks = pd.read_feather("./vectDesc1024")
    vectDescBooks = vectDescBooks.to_numpy()
    mappings = {
        "properties": {
            "id": {"type": "keyword"},
            "description": {"type": "text"},
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


def addUser(id, vector):
    doc = {"id": id, "user_vector": vector}
    client.create(index="hoe-users", document=doc)


def recreateIndexUser(index_name="hoe-users"):
    vectUser = pd.read_csv("userVectorize.csv", index_col="id_user").to_numpy()
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


def getvectBooks(idBook: int):
    """Sert a rien parceque la recherche renvoie déja ça"""
    query = {"term": {"id": idBook}}
    return client.search(
        index=index_name_desc,
        query=query,
    )

def searchBooks(title: str):
    """Sert a rien parceque la recherche renvoie déja ça"""
    query = {"match": {"title": title}}
    return client.search(
        index=index_name_desc,
        query=query,
    )


# recreateIndexDesc(index_name_desc)
# recreateIndexUser()
