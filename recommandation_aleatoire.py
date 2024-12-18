import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
import random

# Charger le fichier CSV
file_path = "questionnaire_traite.csv"
df = pd.read_csv(file_path)

# Étape 1 : Extraire et nettoyer les genres uniques
def convert_to_list(x):
    try:
        return ast.literal_eval(x)
    except:
        return []

df['all_genres'] = df['all_genres'].apply(convert_to_list)
genres_flat = [genre.strip().lower() for sublist in df['all_genres'] for genre in sublist if genre != '-1']
unique_genres = list(set(genres_flat))  # Genres uniques

# Étape 2 : Vectorisation des genres avec TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(unique_genres)

# Étape 3 : Calculer la similarité cosinus entre genres
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=unique_genres, columns=unique_genres)

# Étape 4 : Fonction pour recommander des genres proches mais différents
def recommend_genres(preferred_genre, similarity_matrix, num_recommendations=3, shuffle_results=True):
    if preferred_genre not in similarity_matrix.index:
        return []
    
    # Récupérer les similarités
    similarities = similarity_matrix.loc[preferred_genre]
    
    # Trier les genres par similarité
    recommended_genres = similarities.sort_values(ascending=False).iloc[1:]  # Exclure le genre préféré
    recommended_genres = list(recommended_genres.index)
    
    # Mélanger légèrement les genres si shuffle_results est activé
    if shuffle_results:
        top_half = recommended_genres[:len(recommended_genres)//2]
        random.shuffle(top_half)
        recommended_genres = top_half + recommended_genres[len(recommended_genres)//2:]
    
    # Retourner les genres recommandés jusqu'à num_recommendations
    return recommended_genres[:num_recommendations]

# Exemple d'utilisation : Utilisateur avec un genre préféré
user_liked_genre = 'fantaisie'  # Exemple d'un genre aimé par un utilisateur

# Appel à la fonction pour obtenir 3 genres recommandés
recommended_genres = recommend_genres(user_liked_genre.lower(), cosine_sim_df, num_recommendations=3)

# Afficher les résultats
print(f"Genres recommandés pour le genre préféré '{user_liked_genre}':")
for i, genre in enumerate(recommended_genres, 1):
    print(f"{i}. {genre}")
