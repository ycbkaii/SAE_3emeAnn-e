import pandas as pd
import numpy as np

# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("../csv/Big_boss_authors.csv")


# On met les genres sexuels des personnes en CSV
genders_data = data['author_gender'].drop_duplicates()
csv_genders = genders_data.to_csv("csv_genders_person.csv")






# On enleve les espaces inutiles pour les lieux de naissances comme un 'trim'
def enleverEspace(row) :
    #  retirer les lignes où la colonne 'brithplace' est ""
    if row.strip() == "" :
        return np.nan
    
    return row.strip()
data['birthplace'] = data['birthplace'].apply(enleverEspace)


# On met les lieux de naissances des auteurs en CSV
birth_location_data = data['birthplace'].drop_duplicates()
csv_birth_location = birth_location_data.dropna().to_csv("csv_birth_location.csv")



# On fait auteur pour le CSV

# On recupere le csv fait par guillaume pour les 'genre_livre'
dataGenreLivre = pd.read_csv("peuplement_genre_livre.csv")


# on remplace le 'genre_sexuel' par l'id du genre sexuel
def replaceGenderToId(row) :
    for i in range(len(genders_data)) :
        if row == genders_data[i] :
            return i
    return np.nan

data['author_gender'] = data['author_gender'].apply(replaceGenderToId) 



# # On remplace les lieux par les ids des lieux
def replaceLocationToId(row) :
    found = False
    i = 0
    index_birthplace = birth_location_data.index.tolist()
    values_birthplace = birth_location_data.values.tolist()
    while not(found) and i < len(values_birthplace) :
        
        if isinstance(row, str) and row.strip() == values_birthplace[i] : 
            return index_birthplace[i]
        

        i+=1
    return np.nan

data['birthplace'] = data['birthplace'].apply(replaceLocationToId)


# On garde que les colonnes associés à l'auteur
dataAuteurCsv= data[['author_id', 'author_name', 'author_gender', 'birthplace', 'author_review_count', 'author_rating_count', 'author_average_rating']].to_csv("peuplement_auteurs.csv",index=False) 


# On fait la table de liason en CSV du genres de l'auteurs


# Refaire transformation de genre, essayer avec un nouveau dataFrame et on récolte les genres via auteur avec son id et on prend les genres du CSV et on fait un ETL
# Mettre en lien les genres avec auteur
dataGenreLiaisonAuteur = pd.DataFrame({
    'id_genre' : [None],
    'id_auteur' : [None]
})


# Fonction pour checker si le genre de auteur est le même que celui de la table genre
def like(str1, str2) :
    normalized_str1 = ''.join(str1.lower().split())
    normalized_str2 = ''.join(str2.lower().split())
    
    # Compare les deux chaînes normalisées
    return normalized_str1 == normalized_str2


j = 0

index_genre = dataGenreLivre['genre'].index.tolist()
values_genre = dataGenreLivre['genre'].values.tolist()
while j < len(data['author_genres']) :
    author_genre = data['author_genres'][j]
    
    genre_a_lauteur = author_genre.lower().strip()

    
    i = 0
    genre_a_lauteur_split = genre_a_lauteur.split(',')
    for g in genre_a_lauteur_split :
        found = False
        while not(found) and i < len(values_genre) :
            
            
            
                
            if isinstance(g, str) and like(g, values_genre[i]) :
                
                nouvelle_ligne = pd.DataFrame({
                    'id_genre' : [index_genre[i]],
                    'id_auteur' : [data['author_id'][j]]
                })
                
                dataGenreLiaisonAuteur = pd.concat([dataGenreLiaisonAuteur, nouvelle_ligne], ignore_index=True)
                found = True
            else :
                if '-' in g :
                    # On split le '-' pour voir si c'est trouvé dans les 'genres'
                    genreSansTiret = g.split('-')
                    for genreS in genreSansTiret :
                        if isinstance(genreS, str) and like(genreS, values_genre[i]) :
                
                            nouvelle_ligne = pd.DataFrame({
                                'id_genre' : [index_genre[i]],
                                'id_auteur' : [data['author_id'][j]]
                            })
                            
                            dataGenreLiaisonAuteur = pd.concat([dataGenreLiaisonAuteur, nouvelle_ligne], ignore_index=True)
                            found = True

            i+=1

    j+=1

dataGenreLiaisonAuteur = dataGenreLiaisonAuteur.drop_duplicates()
dataGenreLiaisonAuteur = dataGenreLiaisonAuteur.drop(index=0)
# On transforme en CSV 'peuplement_genre_auteurs.csv'
csv_peuplement_genre_auteurs = dataGenreLiaisonAuteur.to_csv("peuplement_genre_auteurs.csv",index=False)


