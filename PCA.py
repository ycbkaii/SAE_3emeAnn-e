import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from biplot import biplot
import random as rd


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("questionnaire_traite.csv")
total_genre = pd.read_csv("peuplement_genre_livre.csv")


# On récupere les colonnes et on les transforme
variables = [
    "genre_humain",
    "age",
    "genre", 
    "id_secteur",
    "duree_livre_200",
    "familie_lecture",
    "id_prefere_lire"
]



# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

# print(data)


# On supprime les data qui possèdent -1
data = data[data['genre_humain'] != '-1']
# print(data)

# On transforme les genres humain en quantitatives
def transformGender(row) :
    if row == "Homme" :
        return 1
    elif row == "Femme" :
        return 2
    else :
        return 3
data['genre_humain'] = data['genre_humain'].apply(transformGender)


# Transformation duree_livre_200 qualitative => quantitative
def transform_duree(row):
    if row == "je ne le lis pas":
        return 1
    elif row == "1 mois ou +":
        return 2
    elif row == "1 à 2 semaines":
        return 3
    elif row == "entre 3 jours et une semaine":
        return 4
    elif row == "2-3 jours ou moins":
        return 5
    else:
        return 0

data['duree_livre_200'] = data['duree_livre_200'].apply(transform_duree)



# Transformation familie_lecture qualitative => quantitative
def transform_familie(row):
    if row == "nonrenseigne":
        return 0
    elif row == "fache":
        return 1
    elif row == "moyen":
        return 2
    elif row == "content":
        return 3
    elif row == "j'adore lire":
        return 4
    else:
        return 0

data['familie_lecture'] = data['familie_lecture'].apply(transform_familie)


# Transformation age qualitative => quantitative
def transformAge(row) :
    if row <= 12 :
      return 1
    elif row <= 17 :
        return 2
    elif row <= 26 : 
        return 3
    elif row <= 35 :
        return 4
    elif row <= 50 :
        return 5
    else : 
        return 6

data['age'] = data['age'].apply(transformAge)


def hoe_genre(row):
    genre_list = total_genre["genre"].tolist()
    result = [1 if genre in row else 0 for genre in genre_list]
    return result

data['genre'] = data['genre'].apply(hoe_genre) 

# Vérifier que toutes les entrées dans "genre" sont des listes
data['genre'] = data['genre'].apply(lambda x: x if isinstance(x, list) else [])
# Trouver la longueur maximale des listes dans la colonne "genre"
max_genres = max(data['genre'].apply(len))

# Compléter les listes pour qu'elles aient toutes la même longueur
data['genre'] = data['genre'].apply(lambda x: x + [0] * (max_genres - len(x)))

# Convertir les listes en colonnes
genre_columns = pd.DataFrame(data['genre'].tolist(), 
                             columns=[f"genre_{i}" for i in range(max_genres)], 
                             index=data.index)

# Supprimer la colonne d'origine et concaténer les nouvelles colonnes
data = pd.concat([data.drop(columns=["genre"]), genre_columns], axis=1)

data_quant = data[[
    "genre_humain",
    "age",
    "id_secteur",
    "duree_livre_200",
    "familie_lecture",
    "id_prefere_lire"
]]


# On convertit les colonnes de la dataFrame en float
data = data.astype(float)

data["genre_humain"] = data["genre_humain"].dropna()


# On standardise les données
temp = data.sub(data.mean())



# x_scaled qui est le jeu de data standardisées où on effectura l'ACP
x_scaled = temp.div(data.std())
print(" ")
print(" ")
print("hop hop hop")
print(" ")
print(x_scaled)
x_scaled = x_scaled.fillna(0)


print(x_scaled)

print(x_scaled.isnull().sum()) 




#region Mise en place pour les variables 
pca = PCA(n_components=6)
pca.fit(x_scaled)

pca_res = pca.fit_transform(x_scaled)


# On recupere les valeurs propres des composantes
valeursPropre = pca.singular_values_

# On recupere le pourcentage des valeurs propres
pourcentValeursPropre = pca.explained_variance_ratio_

print(f"Affichage des valeurs propres : {valeursPropre}\n")
print(f"Pourcentage valeurs propres : {pourcentValeursPropre}\n")

#CREATION TABLE QUI RESUME LES VALEURS PROPRES
tableauACP = pd.DataFrame({
    "Dimension " : ["Dim" + str (x + 1) for  x in range (6)],
    "Valeur propre" : str(valeursPropre),
    "% valeur propre" : np.round(pourcentValeursPropre * 100),
    "% cum. val. prop." : np.round(np.cumsum(pourcentValeursPropre) * 100)
})

print(f"TableauACP qui résume les valeurs propres :\n {tableauACP}\n")


# Mise en place du graphique des variables
y1 = list(pourcentValeursPropre)
x1 = range(len(y1))
biplot(pca=pca,components=[0,1],x=x_scaled,cat=y1[0:1],density=False)
plt.show()
#endregion


# K-MEANS

data_scaled = pca_res

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

inertias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(data_scaled)
    inertias.append(kmeans.inertia_)

plt.plot(range(1, 11), inertias, marker='o')
plt.xlabel('Nombre de clusters')
plt.ylabel('Inertie')
plt.title('Méthode du coude')
plt.show()

from sklearn.metrics import silhouette_score

for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(data_scaled)
    score = silhouette_score(data_scaled, labels)
    print(f"Silhouette Score for k={k}: {score}")

k = 6 
kmeans = KMeans(n_clusters=k, random_state=42)
data['cluster'] = kmeans.fit_predict(data_scaled)


cluster_to_label = 0  # Cluster cible
filtered_data = data[data['cluster'] == cluster_to_label]

# Tracer les clusters
plt.figure(figsize=(8, 6))
plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=data['cluster'], cmap='viridis')
plt.title('Visualisation des Clusters avec K-Means')
plt.xlabel('Composante Principale 1')
plt.ylabel('Composante Principale 2')
plt.colorbar(label='Cluster')

# Annoter chaque point avec son index
for i in range(data_scaled.shape[0]):
    plt.annotate(str(i), (data_scaled[i, 0], data_scaled[i, 1]), fontsize=8, alpha=0.7)


plt.show()


