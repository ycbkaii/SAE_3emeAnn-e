import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")

variables = ['id','publisher']

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]
data_cleaned = data.dropna(subset=['publisher'])


print(data_cleaned)

# On peut commencer la création du csv
publisher_data=[]

for index, row in data_cleaned.iterrows():
    book_id = row['id']
    publisher = row['publisher']
    publisher_data.append({'publisher': publisher,'id': book_id})

# Convertir la liste en DataFrame
publisher_df = pd.DataFrame(publisher_data)

# Sauvegarder le csv des personnages
publisher_df.to_csv("csv/publisher_avec_id_livre.csv", index=True)
