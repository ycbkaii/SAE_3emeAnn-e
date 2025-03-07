from fastapi import FastAPI, Path, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from PCA import acpReco
from inputData_outputCluster import acmReco
from fastapi.middleware.cors import CORSMiddleware
from recherche import search_books
from utilities import getBooksById
from recommandation_aleatoire import recommend_genres
from fastapi import Form
from fastapi.templating import Jinja2Templates
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
templates = Jinja2Templates(directory="Site")


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
    return getBooksById([books_id])


@app.post("/search", response_class=HTMLResponse)
def search(request : Request,query: str = Form(...)):
    """Route qui redirige vers la recherche"""
    
    return templates.TemplateResponse("recherche.html", {"request": request, "query": query})

@app.get("/retrievedata/{query}")
def retrieveDataLivresSagaAuteurs(query : str) :
    return search_books(query)
