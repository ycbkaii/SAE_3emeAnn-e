import pandas as pd

# Lire le fichier CSV source
raw_csv = pd.read_csv("csv/bigboss_book.csv")

# Extraire les colonnes "id" et "genre_and_votes"
data_extract = raw_csv[["id", "genre_and_votes"]]

# Supprimer les lignes où il n'y a pas de genres (les valeurs manquantes)
data_extract = data_extract.dropna()

# Dictionnaire pour la recherche de l'id du genre
dico_genre = {}

def split_genres_livres(row):
    genres = row['genre_and_votes'].split(', ')
    df_list = []
    for genre in genres:
        parts = genre.split()
        new_genre = ' '.join(parts[:-1])
        df_list.append({'genre': new_genre})
    return pd.DataFrame(df_list)

# Apply the function to all rows and concatenate results
all_genres = pd.concat([split_genres_livres(row) for index, row in data_extract.iterrows()], ignore_index=True)
all_different_genre = all_genres.drop_duplicates().sort_values(by="genre").reset_index(drop = True)

# On remplie notre dictionnaire de recherche
for index, row in all_different_genre.iterrows() :
    dico_genre.update({row["genre"] : index})

# Fonction pour décomposer le genre et les votes de chaque livre
def split_genres_du_livres(row):
    # Séparer les genres en utilisant la virgule comme séparateur
    genres = row["genre_and_votes"].split(", ")
    df_list = []
    for genre in genres:
        parts = (
            genre.split()
        )  # Décomposer le texte du genre en mots (le dernier mot = le nombre de votes)
        new_id = row["id"]  # Récupérer l'ID du livre possédent le genre
        new_genre = " ".join(parts[:-1])  # Joindre tous les mots sauf le dernier pour obtenir le genre
        new_votes = (
            1 if parts[-1] == "1user" else int(parts[-1])
        )  # Convertir le nombre de votes en entier
        id_genre = dico_genre.get(new_genre) # On recupére l'id du genre
        df_list.append({"id_livre": new_id,"id_genre" : id_genre, "votes": new_votes})
    return pd.DataFrame(df_list)


# Appliquer la fonction à toutes les lignes et concaténer les résultats
genre_du_livre = pd.concat(
    [split_genres_du_livres(row) for index, row in data_extract.iterrows()], ignore_index=True
)

# Enregistrer les DataFrames dans des fichier CSV
genre_du_livre.to_csv("csv/peuplement_genre_du_livre.csv", index=False)

all_different_genre.to_csv("csv/peuplement_genre_livre.csv")

