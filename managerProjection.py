from fastapi import APIRouter, HTTPException
import pandas as pd
from collections import Counter
from sqlalchemy import create_engine
from PCA import acpReco
from inputData_outputCluster import acmReco
from recommandation_aleatoire import recommend_genres
from embeddings.embeddingsController import book_sim_by_id
import psycopg2

manager_router = APIRouter(prefix="/manager")

def get_db_connection():
    """Retourne une connexion à la base de données"""
    return psycopg2.connect(
        dbname="masterbook", 
        user="admin", 
        password="root", 
        host="localhost", 
        port="5433"
    )

@manager_router.get("/getRecommendedBooks")
def get_recommended_books():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT id_livre, title, author, isbn, occurrences FROM masterbook.recommended_books"
        cursor.execute(query)
        books = cursor.fetchall()

        # Formater les résultats
        recommended_books = [{"id_livre": book[0], "title": book[1], "author": book[2], "isbn": book[3], "occurrences": book[4]} for book in books]

        cursor.close()
        conn.close()
        return recommended_books

    except Exception as e:
        print(f"Erreur lors de la récupération des livres recommandés : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des livres recommandés")

def check_if_recommended_books_table_is_empty():
    """Vérifie si la table recommended_books est vide"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM masterbook.recommended_books")
        count = cursor.fetchone()[0]
        return count == 0
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification de la table : {e}")
    finally:
        cursor.close()
        conn.close()

def get_books_recom_all_users():
    # Connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer tous les utilisateurs
    query = "SELECT id_user FROM masterbook._utilisateur"
    try:
        cursor.execute(query)
        users = cursor.fetchall()  # Récupérer tous les résultats
        users = [user[0] for user in users]  # Extraire seulement les ids des utilisateurs
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des utilisateurs : {e}")

    # Initialisation d'un dictionnaire pour accumuler les scores des livres
    livres_scores = Counter()

    # Exécuter les fonctions de recommandation pour chaque utilisateur
    for user_id in users[:5]:  # Limite à 5 utilisateurs pour la démo
        try:
            # Exécuter les différentes fonctions de recommandation
            livres_acp = acpReco(user_id)
            livres_acm = acmReco(user_id)
            livres_genres = recommend_genres(user_id)
            livres_sim = book_sim_by_id(user_id)
            
            # Ajouter les livres recommandés aux scores cumulés
            for livre in livres_acp + livres_acm + livres_genres + livres_sim:
                livre_id = livre[5]  # ID du livre
                livres_scores[livre_id] += 1  # Ajouter le score au livre
            
        except Exception as e:
            print(f"Erreur lors de la récupération des livres pour l'utilisateur {user_id}: {e}")
            continue  # Passer à l'utilisateur suivant en cas d'erreur
    
    # Trier les livres par score et prendre les 100 premiers
    top_livres = livres_scores.most_common(100)

    # Créer une liste de dictionnaires avec toutes les informations nécessaires
    top_livres_info = []
    for livre in top_livres:
        livre_id = livre[0]  # ID du livre
        for livre_source in livres_acp + livres_acm + livres_genres + livres_sim:
            if livre_source[5] == livre_id:  # Trouver le livre dans les sources de recommandations
                # Ajouter le livre même s'il manque certaines informations
                top_livres_info.append({
                    "id_livre": livre_source[5],
                    "title": livre_source[0] if len(livre_source) > 0 else None,
                    "author": livre_source[6] if len(livre_source) > 6 else None,  # Valeur par défaut si l'auteur est manquant
                    "isbn": livre_source[3] if len(livre_source) > 3 else None,  # Valeur par défaut si l'ISBN est manquant
                    "image_url": livre_source[4] if len(livre_source) > 4 else None,  # Valeur par défaut si l'image est manquante
                    "occurrences": livre[1]
                })
                break

    # Fermer la connexion et le curseur
    cursor.close()
    conn.close()
    
    # Retourner les informations des 100 livres les plus recommandés
    return {"top_livres_info": top_livres_info}


def store_recommended_books_in_db(recommended_books):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Vérifier si la table est vide
        cursor.execute("SELECT COUNT(*) FROM masterbook.recommended_books")
        count = cursor.fetchone()[0]

        if count == 0:
            # La table est vide, insérer les livres recommandés
            for book in recommended_books:
                cursor.execute("""
                    INSERT INTO masterbook.recommended_books (id_livre, title, author, isbn, occurrences)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id_livre) DO UPDATE
                    SET occurrences = excluded.occurrences
                """, (book['id_livre'], book['title'], book['author'], book['isbn'], book['occurrences']))

            conn.commit()
            print("Table peuplée avec les livres recommandés")
        else:
            print("La table est déjà peuplée, aucune insertion n'a été effectuée.")

    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table: {e}")
    finally:
        cursor.close()
        conn.close()

# Vérification avant d'exécuter les calculs
if check_if_recommended_books_table_is_empty():
    recommended_books = get_books_recom_all_users()
    store_recommended_books_in_db(recommended_books['top_livres_info'])
else:
    print("La table 'recommended_books' est déjà peuplée, aucun calcul effectué.")
