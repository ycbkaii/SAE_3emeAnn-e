import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from biplot import biplot
import random as rd


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")


# On récupere les colonnes quantitatives
variables = ['rating_count', 'review_count', 'average_rating', 'five_star_ratings', 'four_star_ratings', 'three_star_ratings', 'two_star_ratings', 'one_star_ratings', 'number_of_pages']

# Pour le graphique des individus on va récupérer une variable qualitative 'date_published'
variableQualitative = data['date_published'].astype(str)

# On créé une fonction pour qualitativiser la variable
def datePublished(date) :
    dateRetenu = date.split()[-1]
    if dateRetenu == None or dateRetenu == 'nan' : 
        return 'Date Inconnu'

    if int(dateRetenu) >= 2010 :
        return 'Livre Très Récent'
    elif int(dateRetenu) < 2010 and int(dateRetenu) >= 2000 : 
        return 'Livre Récent'
    else :
        return 'Ancien Livre'

variableQualitative = variableQualitative.apply(datePublished)

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

print(data)



# On peut commencer l'analyse en composante principale

# On remplace les virgules ',' en '.' pour qu'ils soient considérés comme des floats
data = data.replace(",", ".", regex=True) 

# On remplace les valeurs NONE dans les colonnes en 0
data.fillna("0", inplace=True) 

# On convertit les colonnes de la dataFrame en float
data = data.astype(float)

# On standardise les données
temp = data.sub(data.mean())



# x_scaled qui est le jeu de data standardisées où on effectura l'ACP
x_scaled = temp.div(data.std())

pca = PCA(n_components=9)
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
    "Dimension " : ["Dim" + str (x + 1) for  x in range (9)],
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



# Mise en place du graphique des individus
pca_df = pd.DataFrame({
    "Dim1" :  pca_res[:,0],
    "Dim2" :  pca_res[:,1],
    "cat_date" : variableQualitative.to_numpy()
})


# La pallette de couleurs
palette = plt.get_cmap('Dark2')
couleurs = dict(zip(pca_df["cat_date"].drop_duplicates(),palette(range(len(pca_df['cat_date'].drop_duplicates())))))
position = dict(zip(couleurs.keys(),range(len(pca_df['cat_date'].drop_duplicates())))) 



pca_df.plot.scatter("Dim1", "Dim2", c=[couleurs[p] for p in pca_df["cat_date"]])
for cont, coul in couleurs.items():
    plt.scatter(135, position[cont] + 10.15, c=[coul])
    plt.text(136, position[cont]  + 10, cont)
plt.xlabel("Dimension 1 (%)")
plt.ylabel("Dimension 2 (%)")
plt.suptitle("Premier plan factoriel (%)")
plt.show()