from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


cosSimGenreBooks =  cosine_similarity(pd.read_csv("./vectGenre.csv",index_col="id_genre").to_numpy())
# print("---------------------------------------------------------------")

client = Elasticsearch("http://localhost:9200")
index_name = "embeddings-books"
def calcSim2Books(id_books1,id_books2 ) :
    livre1 = client.get(index=index_name,id=id_books1)["_source"]["description_vector"]
    livre2  = client.get(index=index_name,id=id_books2)["_source"]["description_vector"]
    return cosine_similarity(np.array(livre1).reshape(1,-1), np.array(livre2).reshape(1,-1))

print(calcSim2Books(42708,43277))