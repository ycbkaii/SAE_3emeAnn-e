import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from sklearn.decomposition import FactorAnalysis
from mca import MCA


# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")

# Fonction pour la création de la variable "nombre d'awards"
def awardsEnNb(col_award) :
    try : 
        nbCol = len(col_award.split(','))
        
        if col_award == "nan" or col_award == "":
            return 'None Price'
        elif nbCol <= 2: 
            return 'Few prices'
        elif nbCol <= 4 : 
            return 'Moderate number prices'
        elif nbCol > 4 :
            return 'A lot of prices'

    except : 
        return 'None Price'

# Fonction pour la création de la variable "Taille du livre"
def tailleLivre(col_nbpages) :
    
    try :
        if float(col_nbpages) <= 200:
             return 'Small book'
        elif float(col_nbpages) <= 350 : 
            return 'Book of intermediate size'
        elif float(col_nbpages) <= 550: 
            return 'Big Book'
        else : 
            return 'Very Big Book'
    except : 
        return 'Unknown Size'

# On prépare les variables catégorielles
catTaille = data['number_of_pages'].apply(tailleLivre)
catAwards = data['awards'].apply(awardsEnNb)


# On enregistre 2 variables catégorielles qui nous interessent que nous avons transformé en catégorielle
data_crosstab = pd.crosstab(catAwards,catTaille)
print(data_crosstab)
## AFC

#region STANDARDISATION
# On met en place la standardisation des données
temp = data_crosstab.sub(data_crosstab.mean())
data_scaled = temp.div(data_crosstab.std())
#endregion


#region TEST DE SPHÉRÉCITÉ DE BARLETT
chi_square_value, p_value = calculate_bartlett_sphericity(data_scaled)
print("p_value = ",p_value) 
#endregion


# On va déterminer le nombre de facteurs à conserver dans l'analyse, on fait sans rotation
fa=FactorAnalyzer(n_factors=3,rotation=None)
fa.fit(data_scaled)
ev,v=fa.get_eigenvalues()
print(ev)

plt.scatter(range(1, data_scaled.shape[1] + 1), ev)
plt.plot(range(1, data_scaled.shape[1] + 1), ev)
plt.title('Scree Plot')
plt.xlabel('Factors')
plt.ylabel('Valeurs Propres')
plt.grid()
#plt.show()


# On définis les méthodes d'analyse factorielle
methods = [
    ("FA No Rotation",FactorAnalysis(2,rotation=None)),
    ("FA Varimax", FactorAnalysis(2, rotation="varimax")),
    ("FA Quartimax", FactorAnalysis(2, rotation="quartimax")),
]

fig, axes = plt.subplots(ncols=3, figsize=(15, 5), sharex=True, sharey=True)


for ax, (method, fa) in zip(axes, methods):
    fa.fit(data_scaled)
    components = fa.components_
    vmax = np.abs(components).max()
    ax.scatter(components[0, :], components[1, :])
    ax.axhline(0, -1, 1, color='k')
    ax.axvline(0, -1, 1, color='k')
    for i, j, z in zip(components[0, :], components[1, :], data_scaled.columns):
        ax.text(i + 0.02, j + 0.02, str(z), ha="center")
    ax.set_title(str(method))
    if ax.get_subplotspec().is_first_col():
        ax.set_ylabel("Factor 1")
    ax.set_xlabel("Factor 2")

# Ajuster la disposition des sous-graphiques
plt.tight_layout()
plt.show()
    
