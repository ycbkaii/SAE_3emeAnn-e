import psycopg2


def getBooksById(listIdBooks) :
    
    # Ouverture connexion bdd
    conn = psycopg2.connect(database="masterbook",
                        port="5433",
                        user="root",
                        host="localhost",
                        password="root"
                        )
    cursor = conn.cursor()
    
    tuples = []
    
    for id in listIdBooks : 
        
        # On vérifie que l'id est un tuple ou non
        if isinstance(id, tuple) :
            id = id[0]
        
        queryToSelectBooks = f"SELECT DISTINCT(title), average_rating, nom_genre, isbn, cover_link, _livre.id_livre FROM masterbook._livre NATURAL JOIN masterbook._genres_du_livre NATURAL JOIN masterbook._genre WHERE id_livre = {id};"
        
        cursor.execute(queryToSelectBooks)

        tuples.append(cursor.fetchall()[0])
        
    
    return tuples