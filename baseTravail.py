import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib
# matplotlib.use('Agg')  # Utiliser le backend Agg



# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("../csv/bigboss_book.csv")

variables = ['author', 'rating_count', 'review_count', 'average_rating','genre_and_votes', 'series', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages', 'publisher', 'date_published']


# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

data = data.drop_duplicates()
# data = data.head(1000)

# Fonction pour extraire le genre le plus voté
# Cela ne prends pas en compte des livres avec moins de votes
def splitFunction (genre) :
    # genre = str(genre).split(",")[0]
    try :   
        genre = str(genre).split(",")
        top_genre_tab = []
        for i in range(len(genre)) :
                
            # print(genre[i])
            # print(genre.split()[-1])
            # print(isinstance(genre.split()[-1], int))        

            if (int(genre[i].split()[-1]) > 4000) :
                top_genre = genre[i].split()
                top_genre.pop(-1)
                top_genre_str = ''
                for i in range (len(top_genre)) :
                    top_genre_str = '_'+top_genre[i]
                # top_genre = top_genre.split("-")[0].strip()
                top_genre_tab.append(top_genre_str)
        # print(top_genre_tab)
        return top_genre_tab
    except:
        return 'Peu_de_critique'
    

# Appliquer la fonction à la colonne 'genre_and_votes'
# On isole le genre le plus voté pour chaque livre
# data['top_genre'] = data["genre_and_votes"].str.split(",", expand=True)[0]
data['top_genre'] = data["genre_and_votes"].apply(splitFunction)

# Utiliser explode() pour étendre la liste des genres dans une nouvelle ligne pour chaque genre
data = data.explode('top_genre')


# print(data['genre'])
# Renommer la colonne pour clarifier
# data_exploded.rename(columns={'top_genre': 'genre'}, inplace=True)

# Supprimer les lignes où la colonne 'top_genre' contient des valeurs NaN
data = data.dropna(subset=['top_genre'])

# On sépare la catégorie du nombre de vote


# data['top_genre'] = data['top_genre'].str.split("[0-9]", expand=True, regex=True)[0]

data.to_html('../data.html')

# FAUT REGROUPER LES CATEGORIE

# data['top_genre'] = data['top_genre'].groupby(0).size().reset_index(name="count")

# data['top_genre'] = data['top_genre'].str.split("-", expand=True)[0].str.strip()
# Appliquer la fonction à la colonne 'genre_and_votes'
# print(data['top_genre'])

# Pour le graphique des individus on va récupérer une variable qualitative 'date_published'

# On créé une fonction pour qualitativiser la variable
def datePublished(date) :
    dateRetenu = date.split()[-1]
    if dateRetenu == None or dateRetenu == 'nan' : 
        return 'Date Inconnu'

    if int(dateRetenu) >= 2010 :
        return 'Livre Très Récent'
    elif int(dateRetenu) < 2010 and int(dateRetenu) >= 2000 : 
        return 'Livre Récent'
    else :
        return 'Ancien Livre'

data['date_published'] = data['date_published'].astype(str).apply(datePublished)

# data = random.choice(data)


# On peut commencer les analyses
from mca import MCA 
# import dask.dataframe as dd
# data_cat = dd.from_pandas(data[['top_genre', 'author', 'date_published']], npartitions=10)
# data_cat = data_cat.categorize()
# dc = dd.get_dummies(data_cat)
data_cat = data[['top_genre', 'date_published']]
dc = pd.get_dummies(data_cat)
print(dc.head())

mca = MCA(dc)

plt.ioff()  # Désactiver le mode interactif

plt.scatter(mca.fs_c()[:, 0], mca.fs_c()[:, 1], s=20, alpha=0.7, edgecolors='none')

for i, var in enumerate(dc.columns):
    plt.annotate(var, (mca.fs_c()[i, 0], mca.fs_c()[i, 1]))    

plt.title("Projection des variables - ACM")
plt.show()


# /CHOICE 

