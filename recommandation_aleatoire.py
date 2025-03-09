import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import random
import psycopg2
import random as rd

# Charger le fichier CSV
#file_path = "questionnaire_traite.csv"
#df = pd.read_csv(file_path)

# INIT BDD
conn = psycopg2.connect(database="masterbook",
                    port="5433",
                    user="root",
                    host="localhost",
                    password="root"
                    )
cursor = conn.cursor()

# Étape 1 : Extraire et nettoyer les genres uniques
def convert_to_list(x):
    try:
        return ast.literal_eval(x)
    except:
        return []

# df['all_genres'] = df['all_genres'].apply(convert_to_list)
# genres_flat = [genre.strip().lower() for sublist in df['all_genres'] for genre in sublist if genre != '-1']
# unique_genres = list(set(genres_flat))  # Genres uniques


# On retrieve tous les genres
tousLesGenres = f"""
SELECT nom_genre FROM masterbook._genre;
"""

cursor.execute(tousLesGenres)

listeGenres = []
tupleGenres = cursor.fetchall() 
for i in tupleGenres :
    listeGenres.append(i[0])
listeGenres = list(set(listeGenres))






# Étape 2 : Vectorisation des genres avec TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(listeGenres)

# Étape 3 : Calculer la similarité cosinus entre genres
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=listeGenres, columns=listeGenres)

# Étape 4 : Fonction pour recommander des genres proches mais différents
def recommend_genres(user_id, similarity_matrix=cosine_sim_df, num_recommendations=1, shuffle_results=True):

    

    # faire script SQL pour récuperer les genres que l'utilisateur
    queryRetrieveGenres = f"""
    SELECT _genre.nom_genre FROM masterbook._genre 
    NATURAL JOIN masterbook._genre_aime
    WHERE id_user = {user_id} 
    ;

    """
    cursor.execute(queryRetrieveGenres)

    tuplesGenres = cursor.fetchall()

    num_aleatoire = rd.randint(0,len(tuplesGenres)-1)
    
    preferred_genre = tuplesGenres[num_aleatoire][0]



    if preferred_genre not in similarity_matrix.index:
        return []
    
    # Récupérer les similarités
    similarities = similarity_matrix.loc[preferred_genre]
    
    
    
    # Trier les genres par similarité
    recommended_genres = similarities.sort_values(ascending=False).iloc[1:]  # Exclure le genre préféré

    # On retire les similarités en dessous de 50%
    listeGenresRecommended = []
    for i in recommended_genres.index :
        if recommended_genres[i] >= 0.5 :
            listeGenresRecommended.append(i)
        else : 
            break
    recommended_genres = listeGenresRecommended
    #recommended_genres = list(recommended_genres.index)
    
    
    # Mélanger légèrement les genres si shuffle_results est activé
    if shuffle_results:
        top_half = recommended_genres[:len(recommended_genres)//2]
        random.shuffle(top_half)
        recommended_genres = top_half + recommended_genres[len(recommended_genres)//2:]
    
    # Retourner les genres recommandés jusqu'à num_recommendations
    genre_retrieved = recommended_genres[:num_recommendations]
    

    queryRecupLivres = f"""
    SELECT * FROM (
        SELECT DISTINCT title, average_rating, nom_genre, isbn, cover_link, _livre.id_livre
        FROM masterbook._livre
        NATURAL JOIN masterbook._genres_du_livre
        NATURAL JOIN masterbook._genre
        WHERE nom_genre = '{genre_retrieved[0].replace("''","'")}'
        AND average_rating > 4.0 AND rating_count >= 300
    ) AS subquery
    ORDER BY RANDOM()
    LIMIT 10;

    """

    cursor.execute(queryRecupLivres)

    return cursor.fetchall()
