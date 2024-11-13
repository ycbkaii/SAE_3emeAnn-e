import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")

variables = ['id','characters']

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]
data_cleaned = data.dropna(subset=['characters'])


print(data_cleaned)

# On peut commencer la création du csv
characters_data=[]

for index, row in data_cleaned.iterrows():
    book_id = row['id']
    characters_list = row['characters'].split(', ')  
    for character in characters_list:
        characters_data.append({'character': character,'id': book_id})

# Convertir la liste en DataFrame
characters_df = pd.DataFrame(characters_data)

# Sauvegarder le csv des personnages
characters_df.to_csv("csv/personnages_avec_id_livre.csv", index=False)
