import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mca import MCA



# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("questionnaire_traite.csv")

variables = ['genre_humain', 'age', 'secteur', 'familie_lecture', 'prefere_lire', 'duree_livre_200', 'genre']


# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]
data = data[data['genre_humain'] != "-1"]





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


# # On peut commencer les analyses
# from mca import MCA 

# data_cat = data
# dc = pd.get_dummies(data_cat)
# print(dc.head())


# mca = MCA(dc)
# # print(mca.fs_c().shape)


# plt.figure(figsize=(10, 8))
# # plt.ioff()  # Désactiver le mode interactif

# plt.scatter(mca.fs_c()[:, 0], mca.fs_c()[:, 1], s=5, alpha=0.7, edgecolors='none')

# # Affichage du texte pour le points (ajout de paramêtre pour que ce soit plus lisible)
# for i, var in enumerate(dc.columns):
#     plt.annotate(var,
#                  (mca.fs_c()[i, 0], mca.fs_c()[i, 1]),
#                  textcoords="offset points",  # Utiliser des coordonnées relatives au point
#                  xytext=(5, 5),  # Décalage de 5 points 
#                  ha='center',    # Alignement horizontal
#                  fontsize=6) 
    
# plt.title("Projection des variables - ACM")
# plt.show()

