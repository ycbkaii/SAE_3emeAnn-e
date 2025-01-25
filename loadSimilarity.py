from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


cosSimGenreBooks = cosine_similarity(
    pd.read_csv("./vectGenre.csv", index_col="id_genre").to_numpy()
)

vectDescBooks = pd.read_feather("./vectDesc1024")
print(vectDescBooks)
vectDescBooks = vectDescBooks.to_numpy()

client = Elasticsearch("http://localhost:9200")
index_name = "embeddings-books"

print(client.info())

def calcSim2Books(id_books1, id_books2):
    livre1 = client.get(index=index_name, id=id_books1)["_source"]["description_vector"]
    livre2 = client.get(index=index_name, id=id_books2)["_source"]["description_vector"]
    # return cosine_similarity(
    #     np.array(livre1).reshape(1, -1), vectDescBooks
    # )
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


print(kNNUser(1))
