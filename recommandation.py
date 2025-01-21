import pandas as pd
import numpy as np
from connection_to_db import conn
from sklearn.metrics.pairwise import cosine_similarity

csv_path = "./userVectorize.csv"


matriceUser = cosine_similarity(pd.read_csv(csv_path))

def getBooksByUser(id : int | str) :
    """
    Fonction pour avoir les livres aimé par les utilisateur
    """
    if conn is not None :
        with conn.cursor() as cursor :
            requete = "SELECT id_livre FROM _a_lu_livre_vote_genre_pour_livre WHERE note_livre>4 AND id_user="+id 
            try :
                cursor.execute(requete)
            except Exception as e :
                print(e)


def getSimilarity(id_user1 : int, id_user2 : int) :
    """
    Renvoie la sim entre user1 et user2
    """
    return matriceUser[id_user1][id_user2]

def getAllSimilarity(id_user : int) :
    """
    Renvoie les sim pour user1
    """
    return matriceUser[id_user]

def findMaxSim(similarity : np.ndarray) :
    trie = sorted(similarity,reverse=True)
    valMax = trie[1:6]
    for e in valMax :
        print(np.where(similarity == e)[0][0])    


findMaxSim(getAllSimilarity(1))