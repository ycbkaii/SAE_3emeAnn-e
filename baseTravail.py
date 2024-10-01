import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib
# matplotlib.use('Agg')  # Utiliser le backend Agg



# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")

variables = ['author', 'rating_count', 'review_count', 'average_rating','genre_and_votes', 'series', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages', 'publisher', 'date_published']


# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]
# Fonction pour extraire le genre le plus voté

# Appliquer la fonction à la colonne 'genre_and_votes'
# On isole le genre le plus voté pour chaque livre
data['top_genre'] = data["genre_and_votes"].str.split(",", expand=True)[0]

# On sépare la catégorie du nombre de vote
data['top_genre'] = data['top_genre'].str.split("[0-9]", expand=True, regex=True)[0]

print(data['top_genre'])


# FAUT REGROUPER LES CATEGORIE

# data['top_genre'] = data['top_genre'].groupby(0).size().reset_index(name="count")

data['top_genre'] = data['top_genre'].str.split("-", expand=True)[0].str.strip()
# Appliquer la fonction à la colonne 'genre_and_votes'
# print(data['top_genre'])

# data = random.choice(data)

data = data.head(1000)
data = data.drop_duplicates()

# On peut commencer les analyses
from mca import MCA 
# import dask.dataframe as dd
# data_cat = dd.from_pandas(data[['top_genre', 'author', 'date_published']], npartitions=10)
# data_cat = data_cat.categorize()
# dc = dd.get_dummies(data_cat)
data_cat = data[['author', 'top_genre']]
dc = pd.get_dummies(data_cat)
print(dc.head())

mca = MCA(dc)

plt.ioff()  # Désactiver le mode interactif

plt.scatter(mca.fs_c()[:, 0], mca.fs_c()[:, 1], s=10, alpha=0.7, edgecolors='none')

for i, var in enumerate(dc.columns):
    plt.annotate(var, (mca.fs_c()[i, 0], mca.fs_c()[i, 1]))    

plt.title("Projection des variables - ACM")
plt.show()


# /CHOICE 

