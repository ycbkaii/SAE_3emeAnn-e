import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")

variables = ['author', 'rating_count', 'review_count', 'average_rating','genre_and_votes', 'series', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages', 'publisher', 'date_published']

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

print(data)

# On peut commencer les analyses 
