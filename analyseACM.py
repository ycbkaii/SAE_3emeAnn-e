import pandas as pd
import numpy as np
from mca import MCA
import psycopg2


conn = psycopg2.connect(
    database="masterbook", port="5433", user="root", host="localhost", password="root"
)
cursor = conn.cursor()
#print("Connected")


query_get_data = """
SELECT DISTINCT ON (_utilisateur.id_user) _utilisateur.id_user, _genre_personne.nom_genre AS genre_humain, age, nom_categorie AS duree_livre_200, nom_humeur AS familie_lecture, _genre.nom_genre AS genre 
FROM masterbook._utilisateur 
FULL OUTER JOIN masterbook._genre_aime ON _genre_aime.id_user = _utilisateur.id_user
FULL OUTER JOIN masterbook._genre ON _genre_aime.id_genre = _genre.id_genre
NATURAL JOIN masterbook._vitesse_de_lecture
NATURAL JOIN masterbook._mood_selection
INNER JOIN masterbook._genre_personne ON id_genre_sex = _genre_personne.id_genre ORDER BY _utilisateur.id_user ;
"""

# Affichage de la data recup
cursor.execute(query_get_data)

tuples = cursor.fetchall()

#print(f"La data : {tuples}\n")


# Récupération des noms des colonnes
columns = [desc[0] for desc in cursor.description]

# Création du DataFrame
data = pd.DataFrame(tuples, columns=columns)


# Fonction pour mentionner que le genre pref n'est pas renseigné
def noneToNaSpecified(row):
    if row == None or row == np.nan:
        return "Non renseigné"


# Fonction pour regrouper en tranche d'age
def groupByAge(row):
    if int(row) >= 18 and int(row) <= 25:
        return "Jeune adulte"
    elif int(row) > 25 and int(row) <= 40:
        return "Adulte"
    elif int(row) > 40:
        return "Senior"
    return "Non renseigné"


# # On récupere le fichier csv et on nettoie ce dernier
# data = pd.read_csv("questionnaire_traite.csv")

# variables = ['genre_humain', 'age', 'secteur', 'familie_lecture', 'prefere_lire', 'duree_livre_200', 'genre']
variables = ["genre_humain", "age", "duree_livre_200", "familie_lecture", "genre"]

# data = data.apply(noneToNaSpecified)
data["age"] = data["age"].apply(groupByAge)


# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]

data = data.reset_index(drop=True)

data = data[data["genre_humain"] != "-1"]

dataFromCsv = data

# # Générer des colonnes pour chaque âge
# age_dummies = pd.get_dummies(data["age"], prefix="age")

# # Ajouter les colonnes générées au DataFrame original
# data = pd.concat([data, age_dummies], axis=1)

# # Supprimer la colonne d'origine si souhaité
# data.drop(columns=["age"], inplace=True)


x = pd.concat([data], axis=1)
dc = pd.DataFrame(pd.get_dummies(x))
dc.head()
# On affiche le tableau disjonctif
#print(dc)

# On affiche le graphique
mcaFic = MCA(dc, benzecri=False)
# plt.scatter(mcaFic.fs_c()[:, 0], mcaFic.fs_c()[:, 1])
# for i, j, nom in zip(mcaFic.fs_c()[:, 0], mcaFic.fs_c()[:, 1],  dc.columns):
#     plt.text(i, j, nom)
# plt.show()


# On renseigne les résultats des coordonnées des individus
mca_result = mcaFic.fs_r()
ids_individus = dc.index


#print(mca_result)
