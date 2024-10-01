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


# Sélection des colonnes de notation
ratings_columns = ['five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings']

# Calcul des moyennes et des écarts-types des notations par catégorie d'étoiles
mean_values = data[ratings_columns].mean()
std_values = data[ratings_columns].std()

# Taille de la population (ici, on suppose n = nombre de livres dans chaque catégorie)
n = len(data)

# Calcul de l'intervalle de confiance à 95 %
ci = 1.96 * std_values / np.sqrt(n)

# Création du graphique
plt.figure()
x = np.array([5, 4, 3, 2, 1])  # Les catégories d'étoiles
y = mean_values.values

plt.plot(x, y, marker='o', linestyle='-', color='b', label='Moyenne des notes')
plt.fill_between(x, (y - ci), (y + ci), color='b', alpha=0.1, label='Intervalle de confiance à 95%')

# Personnalisation du graphique
plt.xlabel('Nombre d\'étoiles')
plt.ylabel('Nombre moyen de notes')
plt.title('Nombre moyen de notes par étoiles avec intervalle de confiance à 95%')
plt.xticks([5, 4, 3, 2, 1], ['5 étoiles', '4 étoiles', '3 étoiles', '2 étoiles', '1 étoile'])
plt.legend()
plt.grid(True)

# Affichage du graphique
plt.show()