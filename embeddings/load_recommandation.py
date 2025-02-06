from elasticsearch import Elasticsearch

from elasticsearch_embeddings import ES_URL

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
    try :
        return client.info()
    except Exception :
        return {"status": "Es is not running"}


def knn_books(id_books1):
    livre1 = client.get(index=index_name, id=id_books1)["_source"]["description_vector"]
    query_string = {
        "field": "description_vector",
        "query_vector": livre1,
        "k": 6,
        "num_candidates": 10000,
    }
    return client.search(index=index_name, knn=query_string, source=False)


def knn_user(user: int):
    index_name_usr = "hoe-users"
    usr = client.get(index=index_name_usr, id=str(user))["_source"]["user_vector"]
    query_string = {
        "field": "user_vector",
        "query_vector": usr,
        "k": 6,
        "num_candidates": 300,
    }
    return client.search(index=index_name_usr, knn=query_string, source=False)
