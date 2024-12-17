import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mca import MCA



# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("questionnaire_traite.csv")

# variables = ['genre_humain', 'age', 'secteur', 'familie_lecture', 'prefere_lire', 'duree_livre_200', 'genre']
variables = ['genre_humain', 'age', 'duree_livre_200', 'familie_lecture', 'genre']

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]
data = data[data['genre_humain'] != "-1"]

# Générer des colonnes pour chaque âge
age_dummies = pd.get_dummies(data["age"], prefix="age")

# Ajouter les colonnes générées au DataFrame original
data = pd.concat([data, age_dummies], axis=1)

# Supprimer la colonne d'origine si souhaité
data.drop(columns=["age"], inplace=True)





x = pd.concat([data],axis=1)
dc=pd.DataFrame(pd.get_dummies(x))
dc.head()
# On affiche le tableau disjonctif
print(dc)

# On affiche le graphique
mcaFic = MCA(dc, benzecri=False)
plt.scatter(mcaFic.fs_c()[:, 0], mcaFic.fs_c()[:, 1])
for i, j, nom in zip(mcaFic.fs_c()[:, 0], mcaFic.fs_c()[:, 1],  dc.columns):
    plt.text(i, j, nom)
plt.show()



# On renseigne les résultats des coordonnées des individus
mca_result = mcaFic.fs_r()
ids_individus = dc.index



print(mca_result)