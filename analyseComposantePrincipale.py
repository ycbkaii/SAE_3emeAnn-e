import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")


# On récupere les colonnes quantitatives
variables = ['rating_count', 'review_count', 'average_rating', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages']

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

print(data)

# On peut commencer l'analyse en composante principale

# On remplace les virgules ',' en '.' pour qu'ils soient considérés comme des floats
data = data.replace(",", ".", regex=True) 



 


