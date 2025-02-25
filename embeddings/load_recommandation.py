from elasticsearch import Elasticsearch

from .elasticsearch_embeddings import ES_URL

try:
    client = Elasticsearch(ES_URL)
except Exception as e:
    client = None
    print("Erreur ElasticSearch : ", e)

index_name = "embeddings-books"


def search_books(title: str):
    """Sert a rien parceque la recherche renvoie déja ça"""
    query = {"match": {"title": title}}
    return client.search(
        index=index_name,
        query=query,
    )


def check_client_es():
    try:
        return client.info()
    except Exception:
        return {"status": "Es is not running"}


def get_vect_books(id_book: int):
    """Pour trouver le vecteur à chercher"""
    query = {"term": {"id": id_book}}
    return client.search(
        index=index_name,
        query=query,
    )


def get_vect_user(id_user: int):
    """Pour trouver le vecteur à chercher"""
    query = {"term": {"id": id_user}}
    return client.search(
        index="hoe-users",
        query=query,
    )


def knn_books(id_books1):
    livre1 = get_vect_books(id_book=id_books1)["hits"]["hits"][0]["_source"][
        "description_vector"
    ]
    query_string = {
        "field": "description_vector",
        "query_vector": livre1,
        "k": 6,
        "num_candidates": 10000,
    }
    return client.search(index=index_name, knn=query_string, source_includes="id")


def knn_user(user: int):
    index_name_usr = "hoe-users"
    usr = get_vect_user(user)["hits"]["hits"][0]["_source"]["user_vector"]
    query_string = {
        "field": "user_vector",
        "query_vector": usr,
        "k": 6,
        "num_candidates": 300,
    }
    return client.search(index=index_name_usr, knn=query_string)
