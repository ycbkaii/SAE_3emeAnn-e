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
            return 'Aucun Prix'
        elif nbCol <= 2: 
            return 'Peu de prix'
        elif nbCol <= 4 : 
            return 'Moyennement de prix'
        elif nbCol > 4 :
            return 'Beaucoup de prix'

    except : 
        return 'Aucun Prix'

# Fonction pour la création de la variable "Taille du livre"


# On prépare les variables catégorielles
catAwards = data['awards'].apply(awardsEnNb)
    
