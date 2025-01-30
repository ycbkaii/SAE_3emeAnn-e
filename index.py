from fastapi import FastAPI
from embeddings.loadSimilarity import kNNBooks, checkClient, kNNUser
from inputData_outputCluster import acmReco
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# On mentionne les cors
origins = [
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/livres/acm_recom/{user_id}")
def get_books_recom_acm(user_id : int) :
    """Cela renvoie les la liste des livres de recommandation"""
    return acmReco(user_id)