import psycopg2
from fastapi import HTTPException
import requests
import re


def get_cover_from_google_books(isbn: str) -> str:
    """
    Récupère l'URL de la couverture d'un livre à partir de l'API Google Books.
    Si aucune couverture n'est trouvée, renvoie l'image de remplacement noCover.
    :param isbn: L'ISBN du livre.
    :return: L'URL de la couverture ou l'URL de l'image noCover.
    """
    no_cover_url = "http://localhost:5173/public/images/noCover.png"  # À adapter selon l'URL de votre image par défaut

    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            cover_url = data["items"][0]["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            # Renvoie l'image par défaut si aucune cover n'est trouvée
            return cover_url if cover_url else no_cover_url
        else:
            # Renvoie l'image par défaut si aucune donnée de livre n'est trouvée
            return "noExist"
    else:
        # En cas d'erreur d'API, on renvoie aussi l'image par défaut
        return no_cover_url





def get_book_data_from_google_books(isbn: str) -> dict:
    """
    Récupère les données d'un livre à partir de l'API Google Books via son ISBN.
    :param isbn: L'ISBN du livre.
    :return: Un dictionnaire contenant les données du livre si trouvé, sinon None.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]  # Retourne le premier résultat trouvé
    return None

def check_book_exists(isbn: str) -> dict:
    """
    Vérifie si un livre existe déjà dans la base de données et s'il est déjà associé à un auteur.
    Si le livre n'existe pas dans la base de données, vérifie son existence via l'API Google Books.
    :param isbn: L'ISBN du livre.
    :return: Un dictionnaire contenant les informations sur l'existence du livre et son état.
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="root",
            host="localhost",
            password="root"
        )
        cursor = conn.cursor()

        # Vérifier si le livre existe dans la table _livre
        query_livre = """
        SELECT id_livre FROM masterbook._livre
        WHERE isbn = %s;
        """
        cursor.execute(query_livre, (isbn,))
        result_livre = cursor.fetchone()

        if result_livre:
            id_livre = result_livre[0]

            # Vérifier si le livre est déjà associé à un auteur dans la table _a_ecrit
            query_relation = """
            SELECT COUNT(*) FROM masterbook._a_ecrit
            WHERE id_livre = %s;
            """
            cursor.execute(query_relation, (id_livre,))
            relation_count = cursor.fetchone()[0]

            return {
                "exists": True,
                "on_site": relation_count > 0,  # True si une relation existe
                "id_livre": id_livre,
                "google_books_data": None  # Pas besoin d'interroger Google Books si le livre est déjà en base
            }

        # Si le livre n'existe pas dans la base de données, vérifier dans Google Books
        google_books_data = get_book_data_from_google_books(isbn)

        return {
            "exists": False,
            "on_site": False,
            "id_livre": None,
            "google_books_data": google_books_data  # Contient les données retournées par Google Books ou None
        }

    except psycopg2.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification du livre : {str(e)}")

    finally:
        cursor.close()
        conn.close()

def check_author_book_relation(author_id: int, isbn: str) -> bool:
    """
    Vérifie si une relation entre un auteur et un livre existe déjà dans la table _a_ecrit.
    :param author_id: L'ID de l'auteur.
    :param isbn: L'ISBN du livre.
    :return: True si la relation existe, False sinon.
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="root",
            host="localhost",
            password="root"
        )
        cursor = conn.cursor()

        # Vérifier si la relation auteur-livre existe
        query = """
        SELECT COUNT(*)
        FROM masterbook._a_ecrit
        INNER JOIN masterbook._livre ON _a_ecrit.id_livre = _livre.id_livre
        WHERE _a_ecrit.id_auteur = %s AND _livre.isbn = %s;
        """
        cursor.execute(query, (author_id, isbn))
        count = cursor.fetchone()[0]

        return count > 0

    except psycopg2.DatabaseError as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification de la relation auteur-livre : {str(e)}")

    finally:
        cursor.close()
        conn.close()

def check_author_exists(author_name: str) -> int:
    """
    Vérifie si un auteur existe déjà dans la base de données.
    :param author_name: Le nom de l'auteur.
    :return: L'ID de l'auteur s'il existe, sinon None.
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="root",
            host="localhost",
            password="root"
        )
        cursor = conn.cursor()

        query = """
        SELECT id_auteur FROM masterbook._auteur
        WHERE LOWER(nom_complet) = LOWER(%s);
        """
        cursor.execute(query, (author_name,))
        result = cursor.fetchone()

        return result[0] if result else None

    except psycopg2.DatabaseError as e:
        print("Erreur SQL :", e.pgerror)
        print("Code d'erreur :", e.pgcode)
        print("Message complet :", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification de l'auteur : {str(e)}")
    finally:
        cursor.close()
        conn.close()

def get_next_author_id() -> int:
    """
    Récupère l'ID maximum dans la table _auteur et retourne le prochain ID disponible.
    :return: Le prochain ID disponible pour un auteur.
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="root",
            host="localhost",
            password="root"
        )
        cursor = conn.cursor()

        query = "SELECT COALESCE(MAX(id_auteur), 0) + 1 FROM masterbook._auteur;"
        cursor.execute(query)
        next_id = cursor.fetchone()[0]

        return next_id

    except psycopg2.DatabaseError as e:
        print("Erreur SQL :", e.pgerror)
        print("Code d'erreur :", e.pgcode)
        print("Message complet :", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l'ID de l'auteur : {str(e)}")

    finally:
        cursor.close()
        conn.close()


def create_author(author_name: str) -> int:
    """
    Crée un nouvel auteur dans la base de données.
    :param author_name: Le nom complet de l'auteur.
    :return: L'ID de l'auteur créé.
    """
    try:
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="root",
            host="localhost",
            password="root"
        )
        cursor = conn.cursor()

        # Récupérer le prochain ID disponible
        author_id = get_next_author_id()

        # Insérer le nouvel auteur
        query = """
        INSERT INTO masterbook._auteur (id_auteur, nom_complet,id_genre_sex)
        VALUES (%s, %s,2);
        """
        cursor.execute(query, (author_id, author_name))

        # Valider la transaction
        conn.commit()

        return author_id

    except psycopg2.DatabaseError as e:
        print("Erreur SQL :", e.pgerror)
        print("Code d'erreur :", e.pgcode)
        print("Message complet :", str(e))
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création de l'auteur : {str(e)}")

    finally:
        cursor.close()
        conn.close()

def clearValueString(value: str) -> str:
    """
    Nettoie une chaîne de caractères en remplaçant les caractères problématiques.
    :param value: La chaîne à nettoyer.
    :return: La chaîne nettoyée.
    """
    if value:
        # Remplacer les guillemets courbes par des guillemets standards
        value = value.replace("“", '').replace("”", '')
        # Remplacer les apostrophes courbes par des apostrophes standards
        value = value.replace("‘", '').replace("’", '')
        value = value.replace('',"")
        # Supprimer les caractères non imprimables ou spéciaux
        value = ''.join(c for c in value if c.isprintable())
       
        # Supprimer les espaces inutiles au début et à la fin
        value = value.strip()
    return value
def normalize_date(date_str: str):
    if not date_str:
        return None

    # Format YYYY
    if re.match(r'^\d{4}$', date_str):
        return f"{date_str}-01-01"

    # Format YYYY-MM
    if re.match(r'^\d{4}-\d{2}$', date_str):
        return f"{date_str}-01"

    # Format YYYY-MM-DD (on ne gère pas d'autres spécificités)
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str

    # Sinon, on renvoie None
    return None
def createBook(livre: dict):
    """
    Insère un nouveau livre dans la base de données.
    :param livre: Un dictionnaire contenant les informations minimales du livre (isbn, genre_id).
    :return: L'ID du livre inséré.
    
    """
    conn = None
    cursor = None
    try:
        # Vérifier si le livre existe déjà
        if check_book_exists(livre["isbn"])["exists"]:
            raise HTTPException(status_code=400, detail="Le livre existe déjà dans la base de données.")

        # Récupérer les données depuis Google Books si nécessaire
        google_books_data = get_book_data_from_google_books(livre["isbn"])
        if google_books_data:
            transformed_data = transform_google_books_data(google_books_data)
            for key, value in transformed_data.items():
                if key not in livre or (livre[key] is None and value is not None):
                    livre[key] = value

        # Nettoyer toutes les chaînes dans le dictionnaire
        for key, value in livre.items():
            if isinstance(value, str):
                livre[key] = clearValueString(value)

        # Si aucune couverture n'est fournie, utiliser une couverture par défaut
        if not livre.get("cover_link"):
            livre["cover_link"] = get_cover_from_google_books(livre["isbn"])

        # Si aucun ISBN-13 ou ISBN-10 n'est trouvé, définir un ISBN vide
        if not livre.get("isbn"):
            livre["isbn"] = ""

        # Connexion à la base de données
        conn = psycopg2.connect(
            database="masterbook",
            port="5433",
            user="root",
            host="localhost",
            password="root"
        )
        cursor = conn.cursor()

        # Calculer le prochain ID du livre
        query_next_id = "SELECT COALESCE(MAX(id_livre), 0) + 1 FROM masterbook._livre;"
        cursor.execute(query_next_id)
        next_id = cursor.fetchone()[0]

        # Insérer le livre dans la table _livre
        query_livre = """
            INSERT INTO masterbook._livre (
                id_livre, title, description, number_of_page, date_published, isbn,
                nom_de_la_saga, numéro_opus, review_count, rating_count,
                average_rating, five_star_ratings, four_star_ratings,
                three_star_ratings, two_star_ratings, one_star_ratings, cover_link
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, 0, 0, 0.0, 0, 0, 0, 0, 0, %s
            )
        """
        rawDate = normalize_date(livre.get("date_published",""))
        # Préparer les valeurs pour l'insertion
        values = [
            next_id,
            livre.get("title", "Titre inconnu"),
            livre.get("description", ""),
            livre.get("number_of_page", 0),
            rawDate,
            livre.get("isbn", ""),
            livre.get("nom_de_la_saga", None),
            livre.get("numéro_opus", None),
            livre.get("cover_link", "")
        ]

    

        cursor.execute(query_livre, values)
        # Vérifier si l'ISBN est déjà présent dans la base de données
        

        # Commit des modifications
        conn.commit()
        print("Livre inséré avec succès avec l'ID :", next_id)
        
        # Associer le genre au livre si un genre_id est fourni
        if "genre_id" in livre and livre["genre_id"] is not None:
            print("genre id "+str(livre['genre_id']))
            query_genre = """
            INSERT INTO masterbook._genres_du_livre (id_livre, id_genre,nombre_votes_utilisateur)
            VALUES (%s, %s,0);
            """
            valueGenre = [
                next_id,
                livre["genre_id"]
            ]
            cursor.execute(query_genre, valueGenre)

        # Gérer les auteurs (si présents dans les données Google Books)
        authors = livre.get("authors", [])
        
        for author_name in authors:
            author_id = check_author_exists(author_name)
            if not author_id:
                author_id = create_author(author_name)
            print("author id : "+str(author_id))
            query_a_ecrit = """
            INSERT INTO masterbook._a_ecrit (id_auteur, id_livre)
            VALUES (%s, %s);
            """
            valueAuteur = [
                author_id,
                next_id
            ]
            cursor.execute(query_a_ecrit, valueAuteur)

        conn.commit()
        return next_id

    except psycopg2.DatabaseError as e:
        conn.rollback()
        print("Erreur SQL :", e.pgerror)
        print("Code d'erreur :", e.pgcode)
        print("Message complet :", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur SQL : {e.pgerror}")

    finally:
        cursor.close()
        conn.close()

def transform_google_books_data(google_books_data: dict) -> dict:
    """
    Transforme les données de Google Books pour les adapter au modèle de la base de données.
    :param google_books_data: Les données retournées par l'API Google Books.
    :return: Un dictionnaire contenant les informations du livre.
    """
    volume_info = google_books_data.get("volumeInfo", {})
    return {
        "title": volume_info.get("title"),
        "description": volume_info.get("description"),
        "number_of_page": volume_info.get("pageCount"),
        "date_published": volume_info.get("publishedDate"),
        "isbn": next(
            (identifier["identifier"] for identifier in volume_info.get("industryIdentifiers", []) if identifier["type"] == "ISBN_13"),
            None
        ),
        "nom_de_la_saga": None,  # À compléter manuellement si nécessaire
        "numéro_opus": None,  # À compléter manuellement si nécessaire
        "review_count": 0,
        "rating_count": volume_info.get("ratingsCount", 0),
        "average_rating": volume_info.get("averageRating", 0),
        "five_star_ratings": 0,
        "four_star_ratings": 0,
        "three_star_ratings": 0,
        "two_star_ratings": 0,
        "one_star_ratings": 0,
        "cover_link": volume_info.get("imageLinks", {}).get("thumbnail"),
        "authors" :volume_info.get("authors", [])
    }
