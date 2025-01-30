from elasticsearch import Elasticsearch

try : 
    client = Elasticsearch("http://localhost:9200")
except Exception as e :
    client = None
    print("Erreur ElasticSearch : ",e)

index_name = "embeddings-books"

def checkClient() :
    if client is not None :
        return client.info()
    else :
        return {"Status" : "Es is not running"}

def kNNBooks(id_books1):
    livre1 = client.get(index=index_name, id=id_books1)["_source"]["description_vector"]
    query_string = {
        "field": "description_vector",
        "query_vector": livre1,
        "k": 6,
        "num_candidates": 10000
    }
    return client.search(index=index_name, knn=query_string)

def kNNUser(user : int) :
    index_name="hoe-users"
    usr = client.get(index=index_name, id=user)["_source"]["user_vector"]
    query_string = {
        "field": "user_vector",
        "query_vector": usr,
        "k": 6,
        "num_candidates": 300
    }
    return client.search(index=index_name, knn=query_string)