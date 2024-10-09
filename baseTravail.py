import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("../csv/bigboss_book.csv")

variables = ['author', 'rating_count', 'review_count', 'average_rating','genre_and_votes', 'series', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages', 'publisher', 'date_published']


# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

data = data.drop_duplicates()

# Fonction pour extraire le genre le plus voté
# Cela ne prends pas en compte des livres avec moins de votes
def splitFunction (genre) :
    # genre = str(genre).split(",")[0]
    try :   
        genre = str(genre).split(",")
        top_genre_tab = []
        for i in range(len(genre)) :

            if (int(genre[i].split()[-1]) > 4000) :
                top_genre = genre[i].split()
                top_genre.pop(-1)
                top_genre_str = ''
                for i in range (len(top_genre)) :
                    top_genre_str = '_'+top_genre[i]
                top_genre_tab.append(top_genre_str)
        return top_genre_tab
    except:
        return 'Peu_de_critique'
    

# Appliquer la fonction à la colonne 'genre_and_votes'
# On isole le genre le plus voté pour chaque livre
data['top_genre'] = data["genre_and_votes"].apply(splitFunction)

# Utiliser explode() pour étendre la liste des genres dans une nouvelle ligne pour chaque genre
data = data.explode('top_genre')

# Supprimer les lignes où la colonne 'top_genre' contient des valeurs NaN
data = data.dropna(subset=['top_genre'])


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

# On peut commencer les analyses
from mca import MCA 

data_cat = data[['top_genre', 'date_published']]
dc = pd.get_dummies(data_cat)
print(dc.head())

mca = MCA(dc)

plt.figure(figsize=(10, 8))
plt.ioff()  # Désactiver le mode interactif

plt.scatter(mca.fs_c()[:, 0], mca.fs_c()[:, 1], s=5, alpha=0.7, edgecolors='none')

# Affichage du texte pour le points (ajout de paramêtre pour que ce soit plus lisible)
for i, var in enumerate(dc.columns):
    plt.annotate(var,
                 (mca.fs_c()[i, 0], mca.fs_c()[i, 1]),
                 textcoords="offset points",  # Utiliser des coordonnées relatives au point
                 xytext=(5, 5),  # Décalage de 5 points 
                 ha='center',    # Alignement horizontal
                 fontsize=6) 
    
plt.title("Projection des variables - ACM")
plt.show()


