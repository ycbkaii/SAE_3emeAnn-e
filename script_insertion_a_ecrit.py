
import pandas as pd

# Charger les deux fichiers CSV d'origine
books_df = pd.read_csv("bigboss_book(1).csv")  # Contient la colonne 'id' pour 'id_livre'
authors_df = pd.read_csv("Big_boss_authors.csv")  # Contient la colonne 'author_id' pour 'id_auteur'

# Sélectionner uniquement les colonnes nécessaires
books_df = books_df[['id']]  # Renommer 'id' en 'id_livre'
authors_df = authors_df[['author_id']]  # Renommer 'author_id' en 'id_auteur'

# Créer un produit cartésien des deux colonnes pour obtenir toutes les combinaisons possibles
a_ecrit_df = pd.DataFrame(columns=['id_livre', 'id_auteur'])
a_ecrit_df['id_livre'] = books_df['id']
a_ecrit_df['id_auteur'] = authors_df['author_id']


# Sauvegarder le DataFrame résultant dans un nouveau fichier CSV
a_ecrit_df.to_csv("a_ecrit.csv", index=False)

print("Le fichier a_ecrit.csv a été généré avec succès.")
