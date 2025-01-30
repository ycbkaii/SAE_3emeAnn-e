from ollama_emb import embedText
from elasticsearchEmbeddings import addBooks,searchBooks

def ObjectApiResponseToIds() :
    """ Permet de renvoyer les ids des livres de la réponse d'ES """

class Books() :
    """La classe pour un livre"""
    id : int
    title : str
    desc : str
    genre : str

def addNewBooks(books : Books) -> bool :
    # TODO ajouter le livre au SQL
    embedding = embedText(books.desc)["embeddings"][0]
    addBooks(books.desc,embedding,books.title,books.genre,books.id)
    return True

def recherchBooks(title : str) : 
    return searchBooks(title=title)