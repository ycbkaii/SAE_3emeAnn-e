import psycopg2
from fastapi import HTTPException


def getBooksById(listIdBooks):
    # Ouverture connexion bdd
    conn = psycopg2.connect(
        database="masterbook",
        port="5432",
        user="root",
        # host="localhost",
        host="postgres-sae",
        password="root",
    )
    cursor = conn.cursor()

    tuples = []

    for id in listIdBooks:
        # On vérifie que l'id est un tuple ou non
        if isinstance(id, tuple):
            id = id[0]
        
        queryToSelectBooks = f"SELECT DISTINCT(title), average_rating, nom_genre, isbn, cover_link, _livre.id_livre FROM masterbook._livre NATURAL JOIN masterbook._genres_du_livre NATURAL JOIN masterbook._genre WHERE id_livre = {id};"
        
        cursor.execute(queryToSelectBooks)

        try :
            tuples.append(cursor.fetchall()[0])
        except Exception as e:
            print(id)
            print(e)

    return tuples

def getBooksInfosById(listIdBooks) :
    
    # Ouverture connexion bdd
    conn = psycopg2.connect(database="masterbook",
                        port="5432",
                        user="root",
                        host="postgres-sae",
                        password="root"
                        )
    cursor = conn.cursor()
    
    tuples = []
    
    for id in listIdBooks : 
        
        # On vérifie que l'id est un tuple ou non
        if isinstance(id, tuple) :
            id = id[0]
        
        queryToSelectBooks = f"SELECT nom_genre FROM masterbook._livre NATURAL JOIN masterbook._genres_du_livre NATURAL JOIN masterbook._genre WHERE _livre.id_livre = {id};"
        
        cursor.execute(queryToSelectBooks)

        tuples.append(cursor.fetchall())
        
    
    return tuples



def getBooksInfosallById(listIdBooks):
    try:
        # Ouverture connexion bdd avec gestion sécurisée
        with psycopg2.connect(database="masterbook", port="5432", user="root", host="postgres-sae", password="root") as conn:
            with conn.cursor() as cursor:
                tuples = []
                for id in listIdBooks:
                    if isinstance(id, tuple):
                        id = id[0]
                    
                    queryToSelectAllBooks = """
SELECT 
    l.id_livre,
    l.title,
    l.description,
    l.number_of_page,
    l.isbn,
    l.nom_de_la_saga,
    l.numéro_opus,
    l.review_count,
    l.rating_count,
    l.average_rating,
    l.cover_link,
    s.nom_de_la_saga,
    STRING_AGG(DISTINCT p.nom_personnage, ', ') AS personnages,
    STRING_AGG(DISTINCT aw.nom_awards, ', ') AS recompenses,
    STRING_AGG(DISTINCT pub.nom_complet, ', ') AS publishers
FROM 
    masterbook._livre l
LEFT JOIN masterbook._saga s ON l.nom_de_la_saga = s.nom_de_la_saga
LEFT JOIN masterbook._possede_personnage pp ON l.id_livre = pp.id_books
LEFT JOIN masterbook._personnage p ON pp.id_personnage = p.id_personnage
LEFT JOIN masterbook._recompense_en vl ON l.id_livre = vl.id_livre
LEFT JOIN masterbook._awards aw ON vl.id_awards = aw.id_awards
LEFT JOIN masterbook._a_publie ap ON l.id_livre = ap.id_book
LEFT JOIN masterbook._publisher pub ON ap.id_publisher = pub.id_publisher
WHERE l.id_livre = %s
GROUP BY 
    l.id_livre,
    l.title,
    l.description,
    l.number_of_page,
    l.isbn,
    l.nom_de_la_saga,
    l.numéro_opus,
    l.review_count,
    l.rating_count,
    l.average_rating,
    l.cover_link,
    s.nom_de_la_saga
"""
                    cursor.execute(queryToSelectAllBooks, (id,))
                    tuples.append(cursor.fetchall())
                return tuples
    except psycopg2.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
