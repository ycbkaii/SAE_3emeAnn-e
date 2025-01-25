from elasticsearch import Elasticsearch
import pandas as pd

client = Elasticsearch("http://localhost:9200")

vectDescBooks = pd.read_feather("./vectDesc1024")
print(vectDescBooks)
vectDescBooks = vectDescBooks.to_numpy()


index_name_desc = "embeddings-books"


def recreateIndexDesc(vectDescBooks, index_name):
    mappings = {
        "properties": {"description_vector": {"type": "dense_vector", "dims": 1024}}
    }
    client.indices.delete(index=index_name)

    client.indices.create(index=index_name, mappings=mappings)

    for i in range(len(vectDescBooks)):
        doc = {"description_vector": vectDescBooks[i]}
        resp = client.index(index=index_name, id=i, document=doc)
        print(resp["result"], i)


def recreareIndexGenre(vectGenreBooks, index_name):
    mappings = {
       "properties": {"genre_vector": {"type": "dense_vector", "dims": 1024}}
    }
    try :
      client.indices.delete(index=index_name)
    except Exception as e :
      print(e)
    
    client.indices.create(index=index_name, mappings=mappings)

    for i in range(len(vectGenreBooks)):
        doc = {"genre_vector": vectGenreBooks[i]}
        resp = client.index(index=index_name, id=i, document=doc)
        print(resp["result"], i)


# recreateIndex(vectDescBooks, index_name)
def getvectBooks(idBook: int):
    return client.get(index=index_name_desc, id=idBook)
