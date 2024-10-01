#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 09:37:21 2024

@author: yoalebris
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Lecture du fichier CSV avec low_memory=False pour éviter les avertissements sur les types de colonnes mélangés
data = pd.read_csv('bigboss_book.csv', low_memory=False)

# Conversion de 'average_rating' en float avec gestion des erreurs
data['average_rating_float'] = pd.to_numeric(data['average_rating'].str.replace(',', '.'), errors='coerce')

# Fonction pour segmenter genre_and_votes et garder ceux avec plus de 50 votes
def segment_genre_votes(genre_and_votes):
    if not isinstance(genre_and_votes, str):
        # Si ce n'est pas une chaîne de caractères (ex. NaN), retourner une liste vide
        return []
    
    # Séparer chaque couple genre-vote par une virgule
    genres_votes = genre_and_votes.split(',')
    
    # Filtrer et extraire seulement les genres avec plus de 50 votes
    filtered_genres = []
    for genre_vote in genres_votes:
        # Utiliser une expression régulière pour capturer les genres avec tirets, espaces, et les votes
        match = re.match(r'#?([\w\s\-]+)\s(\d+)', genre_vote.strip())
        if match:
            genre = match.group(1).strip()
            votes = int(match.group(2))
            if votes > 50:
                filtered_genres.append(genre)
    
    # Retourner une liste des genres avec plus de 50 votes
    return filtered_genres

# Appliquer la fonction à la colonne 'genre_and_votes' pour obtenir une nouvelle colonne 'filtered_genres'
data['filtered_genres'] = data['genre_and_votes'].apply(segment_genre_votes)
print(data['genre_and_votes'])
print(data['filtered_genres'])
# Exploser la colonne 'filtered_genres' pour qu'il y ait une ligne par genre
data_exploded = data.explode('filtered_genres')

# Supprimer les lignes avec des valeurs NaN dans 'filtered_genres' après explosion
data_exploded = data_exploded.dropna(subset=['filtered_genres'])

# Groupement par genre filtré et calcul de la moyenne des notes
datamean = data_exploded.groupby('filtered_genres').mean(numeric_only=True)

# Sélectionner les colonnes d'analyse
dataanalise = ['average_rating_float']
datamean = datamean[dataanalise]

# Affichage des moyennes
print(datamean)

# Données pour les barres
x = np.arange(len(datamean))  # Indices pour les genres filtrés

# Largeur des barres et décalage
width = 0.1  # Largeur des barres légèrement augmentée pour plus de lisibilité
dist = 0.1    # Distance entre les barres

# Taille du graphique ajustée pour correspondre à la quantité de données
plt.figure(figsize=(1*len(datamean), 10))  # Largeur proportionnelle au nombre de genres

# Création du graphique à barres
colors = ['cyan', 'orange', 'green']  # Correspondre au nombre de variables analysées
for i, var in enumerate(dataanalise):
    plt.bar(x + (i - 1) * dist, datamean[var], width, color=colors[i], label=var.capitalize())

# Ajout des labels et légendes
plt.xticks(x, datamean.index, rotation=45, ha="right")
plt.xlabel('Genres filtrés')
plt.ylabel('Moyennes des variables')
plt.title('Moyennes des notes par genre filtré')

# Déplacer la légende à l'extérieur du graphique
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Affichage du graphique
plt.tight_layout()  # Ajustement pour éviter les chevauchements
plt.grid(True)
plt.show()
