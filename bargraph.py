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

# Lecture du fichier CSV
data = pd.read_csv('bigboss_book.csv', low_memory=False)

# Conversion de 'average_rating' en float
data['average_rating_float'] = pd.to_numeric(data['average_rating'].str.replace(',', '.'), errors='coerce')

# Fonction pour filtrer les genres ayant plus de 50 votes
def segment_genre_votes(genre_and_votes):
    if not isinstance(genre_and_votes, str):
        return []
    
    genres_votes = genre_and_votes.split(',')
    filtered_genres = []
    
    for genre_vote in genres_votes:
        match = re.match(r'#?([\w\s\-]+)\s(\d+)', genre_vote.strip())
        if match:
            genre = match.group(1).strip()
            votes = int(match.group(2))
            if votes > 50:  # Garde les genres avec plus de 50 votes
                filtered_genres.append(genre)
    
    return filtered_genres

# Appliquer la fonction pour créer une nouvelle colonne avec les genres filtrés
data['filtered_genres'] = data['genre_and_votes'].apply(segment_genre_votes)

# Diviser la colonne pour avoir une ligne par genre
data_exploded = data.explode('filtered_genres')

# Supprimer les lignes sans genre après explosion
data_exploded = data_exploded.dropna(subset=['filtered_genres'])

# Calculer la moyenne des notes par genre
datamean = data_exploded.groupby('filtered_genres').mean(numeric_only=True)

# Sélectionner les colonnes d'analyse (ici, le nombre de pages)
dataanalise = ['number_of_pages']
datamean = datamean[dataanalise]

# Nombre de genres à afficher
n_genres_to_display = 1000

# Limiter les données aux 'n_genres_to_display' premiers genres
datamean = datamean.head(n_genres_to_display)

# Afficher les moyennes
print(datamean)

# Indices pour les genres filtrés
x = np.arange(len(datamean))

# Largeur des barres
width = 0.7

# Ajuster la taille du graphique
plt.figure(figsize=(0.5 * len(datamean), 8))

# Créer le graphique à barres
colors = ['black']
for i, var in enumerate(dataanalise):
    plt.bar(x, datamean[var], width, color=colors[i], label=var.capitalize())

# Ajouter des labels
plt.xticks(x, datamean.index, rotation=45, ha="right")
plt.xlabel('Genres filtrés')
plt.ylabel('Moyennes des variables')
plt.title(f'Moyennes des notes par genre filtré (top {n_genres_to_display} genres)')

# Ajuster les limites des axes
plt.xlim(-0.5, len(datamean) - 0.5)

# Positionner la légende
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Afficher le graphique
plt.tight_layout()
plt.grid(True)
plt.show()
