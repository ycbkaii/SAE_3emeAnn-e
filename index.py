from fastapi import FastAPI, Path
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
<<<<<<< Updated upstream
=======
from PCA import acpReco
from get_saga import getSagaById
>>>>>>> Stashed changes
from inputData_outputCluster import acmReco
from PCA import acpReco
from fastapi.middleware.cors import CORSMiddleware
from utilities import getBooksById
from recommandation_aleatoire import recommend_genres
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

# Charger le CSS et le JS dans les pages
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    """La route par def"""
    file_path = "Site/index.html"
    return FileResponse(file_path)

@app.get("/contact", response_class=HTMLResponse)
def get_contact():
    file_path = "Site/contacts.html"
    return FileResponse(file_path)


@app.get("/livres/acm_recom/{user_id}")
def get_books_recom_acm(user_id : int) :
    """Cela renvoie les la liste des livres de recommandation"""
    return acmReco(user_id)

@app.get("/livres/acp_recom/{user_id}")
def get_books_recom_acp(user_id : int) :
    """Cela renvoie les la liste des livres de recommandation en ACP"""
    return acpReco(user_id)

@app.get("/livres/genres/{user_id}")
def get_recommended_genres(user_id):
    recommended = recommend_genres(user_id)
    return recommended


@app.get("/init")
def init_ia() :
    """Route pour init les algorithmes""" 
    
@app.get("/book", response_class=HTMLResponse)
def get_book():
    file_path = "Site/book.html"
    return FileResponse(file_path)

@app.get("/books_list/{books_id}")
def retourne_book(books_id : int) :
    """ Renvoie les recommandations item_base pour le livre d'id {books_id} """
<<<<<<< Updated upstream
    return getBooksById([books_id])
=======
    return getBooksById([books_id])

@app.get("/books_infos_list/{books_id}")
def retourne_book2(books_id : int) :
    return getBooksInfosById([books_id])[0]

@app.get("/books_infos_all_list/{books_id}")
def retourne_book3(books_id : int) :
    return getBooksInfosallById([books_id]) 

@app.get("/books_saga/{sagaName}")
def retourne_saga(sagaName : str) :
    return getSagaById(sagaName)


@app.post("/search", response_class=HTMLResponse)
def search(request : Request,query: str = Form(...)):
    """Route qui redirige vers la recherche"""
    
    return templates.TemplateResponse("recherche.html", {"request": request, "query": query})

@app.get("/retrievedata/{query}")
def retrieveDataLivresSagaAuteurs(query : str) :
    return search_books(query)
>>>>>>> Stashed changes
