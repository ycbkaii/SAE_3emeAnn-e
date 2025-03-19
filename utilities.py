import psycopg2
from fastapi import HTTPException


def getBooksById(listIdBooks):
    # Ouverture connexion bdd
    conn = psycopg2.connect(
        database="masterbook",
        port="5433",
        user="utilisateur",
        # host="localhost",
        host="localhost",
        password="root",
    )
    cursor = conn.cursor()

    tuples = []

    for id in listIdBooks:
        # On vérifie que l'id est un tuple ou non
        if isinstance(id, tuple):
            id = id[0]
        
        queryToSelectBooks = f"SELECT DISTINCT _livre.title, _livre.average_rating, _genre.nom_genre, _livre.isbn, _livre.cover_link, _livre.id_livre, _auteur.nom_complet, _livre.description, _livre.id_livre FROM masterbook._livre INNER JOIN masterbook._genres_du_livre ON _livre.id_livre = _genres_du_livre.id_livre INNER JOIN masterbook._genre ON _genres_du_livre.id_genre = _genre.id_genre LEFT JOIN masterbook._a_ecrit ON _livre.id_livre = _a_ecrit.id_livre LEFT JOIN masterbook._auteur ON _a_ecrit.id_auteur = _auteur.id_auteur WHERE _livre.id_livre = {id};"
        
        cursor.execute(queryToSelectBooks)

        try :
            tuples.append(cursor.fetchall()[0])
        except Exception as e:
            print(id)
            print(e)

        # print(tuples, "test")

    return tuples

def getBooksInfosById(listIdBooks) :
    
    # Ouverture connexion bdd
    conn = psycopg2.connect(database="masterbook",
                        port="5433",
                        user="utilisateur",
                        host="localhost",
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
        with psycopg2.connect(database="masterbook", port="5433", user="utilisateur", host="localhost", password="root") as conn:
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
    STRING_AGG(DISTINCT pub.nom_complet, ', ') AS publishers,
    STRING_AGG(DISTINCT a.nom_complet, ', ') AS auteur
FROM 
    masterbook._livre l
LEFT JOIN masterbook._saga s ON l.nom_de_la_saga = s.nom_de_la_saga
LEFT JOIN masterbook._possede_personnage pp ON l.id_livre = pp.id_books
LEFT JOIN masterbook._personnage p ON pp.id_personnage = p.id_personnage
LEFT JOIN masterbook._recompense_en vl ON l.id_livre = vl.id_livre
LEFT JOIN masterbook._awards aw ON vl.id_awards = aw.id_awards
LEFT JOIN masterbook._a_publie ap ON l.id_livre = ap.id_book
LEFT JOIN masterbook._publisher pub ON ap.id_publisher = pub.id_publisher
LEFT JOIN masterbook._a_ecrit ae ON l.id_livre = ae.id_livre 
LEFT JOIN masterbook._auteur a ON ae.id_auteur = a.id_auteur
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
    s.nom_de_la_saga;
"""
                    cursor.execute(queryToSelectAllBooks, (id,))
                    tuples.append(cursor.fetchall())
                return tuples
    except psycopg2.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
def search_books_deux(query: str, search_type: str):
    """Recherche améliorée des livres, auteurs et sagas"""
    results = {"books": [], "authors": [], "sagas": []}
    
    try:
        conn = psycopg2.connect(database="masterbook",
                            port="5433",
                            user="utilisateur",
                            host="localhost",
                            password="root"
                            )
        cur = conn.cursor()

        if search_type == "title":
            cur.execute("""
                SELECT _livre.id_livre, title, description, cover_link, nom_de_la_saga, numéro_opus, _a_ecrit.id_auteur
                FROM masterbook._livre
                FULL OUTER JOIN masterbook._a_ecrit ON _livre.id_livre = _a_ecrit.id_livre
                FULL OUTER JOIN masterbook._auteur ON _auteur.id_auteur = _a_ecrit.id_auteur
                WHERE title ILIKE %s
            """, (f"%{query}%",))
            books = cur.fetchall()
            results["books"] = [
                {"id": b[0], "title": b[1].strip(), "description": (b[2] or "Pas de description").strip(),
                "cover": (b[3] or "").strip(), "saga": (b[4] or "").strip(),
                "num_opus": b[5], "id_auteur": b[6]}
                for b in books
            ]

        elif search_type == "author":
            cur.execute("""
                SELECT id_auteur, nom_complet, review_count, average_rating
                FROM masterbook._auteur
                WHERE nom_complet ILIKE %s
            """, (f"%{query}%",))
            authors = cur.fetchall()
            results["authors"] = [
                {"id": a[0], "name": a[1].strip(), 'reviews': a[2], 'avg_rating': a[3]}
                for a in authors
            ]

        elif search_type == "saga":
            cur.execute("SELECT nom_de_la_saga FROM masterbook._saga WHERE nom_de_la_saga ILIKE %s", (f"%{query}%",))
            sagas = cur.fetchall()
            results["sagas"] = [
                {"name": s[0].strip()} for s in sagas
]

        cur.close()
        conn.close()
    
    except psycopg2.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    return results

def get_search_suggestions_deux(query: str, search_type: str):
    """Récupère des suggestions en temps réel"""
    try:
        conn = psycopg2.connect(database="masterbook",
                            port="5433",
                            user="utilisateur",
                            host="localhost",
                            password="root"
                            )
        cur = conn.cursor()

        if search_type == "title":
            cur.execute("""
                SELECT DISTINCT id_livre, title 
                FROM masterbook._livre 
                WHERE title ILIKE %s 
            """, (f"%{query}%",))
        elif search_type == "author":
            cur.execute("""
                SELECT DISTINCT id_auteur, nom_complet 
                FROM masterbook._auteur 
                WHERE nom_complet ILIKE %s 
                LIMIT 10
            """, (f"%{query}%",))

        suggestions = cur.fetchall()
        cur.close()
        conn.close()

        # 🔥 On retourne maintenant un objet { id, name }
        return {"results": [{"id": s[0], "name": s[1].strip()} for s in suggestions]}



    
    except psycopg2.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
def get_books_by_author(author_id: int):
    """Récupère tous les livres écrits par un auteur donné"""
    
    conn = psycopg2.connect(database="masterbook",
                            port="5433",
                            user="utilisateur",
                            host="localhost",
                            password="root")
    cur = conn.cursor()
    
    cur.execute("""
        SELECT _livre.id_livre, _livre.title, _livre.cover_link, _auteur.nom_complet
        FROM masterbook._livre
        JOIN masterbook._a_ecrit ON _livre.id_livre = _a_ecrit.id_livre
        JOIN masterbook._auteur ON _a_ecrit.id_auteur = _auteur.id_auteur
        WHERE _auteur.id_auteur = %s
    """, (author_id,))
    
    books = cur.fetchall()
    cur.close()
    conn.close()

    print(books)
    
    return {"books": [{"id": b[0], "title": b[1], "cover": b[2], "author": b[3]} for b in books]}