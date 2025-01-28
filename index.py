from fastapi import FastAPI
from embeddings.loadSimilarity import kNNBooks, checkClient, kNNUser

app = FastAPI()

@app.get("/")
def read_root():
    """La route par def"""
    return {"Hello": "World"}

@app.get("/es_info")
def elastic_search_info() :
    """Renvoie les infos du clients ElasticSearch"""
    return checkClient()


@app.get("/books/{books_id}")
def get_reco_books_id(books_id : int) :
    """ Renvoie les recommandations item_base pour le livre d'id {books_id} """
    return kNNBooks(books_id)

@app.get("/user/{user_id}")
def get_user_similar_id(user_id : int) :
    """Renvoie les usr similaire """
    return kNNUser(user_id)