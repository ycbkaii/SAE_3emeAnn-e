import pandas as pd

# Lire le fichier CSV source
raw_csv = pd.read_csv("csv/bigboss_book.csv")

# Extraire les colonnes "id" et "genre_and_votes"
data_extract = raw_csv[["id", "genre_and_votes"]]

# Supprimer les lignes où il n'y a pas de genres (les valeurs manquantes)
data_extract = data_extract.dropna()


# Fonction pour décomposer le genre et les votes de chaque livre
def split_genres(row):
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
        df_list.append({"id_livre": new_id, "genre": new_genre, "votes": new_votes})
    return pd.DataFrame(df_list)


# Appliquer la fonction à toutes les lignes et concaténer les résultats
genre_du_livre = pd.concat(
    [split_genres(row) for index, row in data_extract.iterrows()], ignore_index=True
)

# Enregistrer le DataFrame des genres dans un fichier CSV
genre_du_livre.to_csv("csv/peuplement_genre_du_livre.csv", index=False)

# Extraire les genres uniques, les trier par ordres, les réindexer et enregistrer dans un autre fichier CSV
genre_unique = (
    genre_du_livre["genre"].drop_duplicates().sort_values().reset_index(drop=True)
)
genre_unique.to_csv("csv/peuplement_genre_livre.csv", index_label="id")
