from elasticsearch import Elasticsearch
import pandas as pd

client = Elasticsearch("http://localhost:9200")

client.info()

vectDescBooks =  pd.read_feather("./vectDesc1024")
print(vectDescBooks)
vectDescBooks = vectDescBooks.to_numpy()

mappings = {
      "properties": {
        "description_vector": {
          "type": "dense_vector",
          "dims" : 1024
        }
      }
    }

index_name = "embeddings-books"

def recreateIndex( vectDescBooks, index_name):
    client.indices.delete(index=index_name)

    client.indices.create(index=index_name,mappings=mappings)

    for i in range(len(vectDescBooks)) :
        doc = {
        "description_vector" : vectDescBooks[i]
    }
        resp = client.index(index=index_name, id=i, document=doc)
        print(resp['result'],i)

# recreateIndex(vectDescBooks, index_name)
def getvectBooks(idBook : int ) :
    return client.get(index=index_name, id=idBook)

