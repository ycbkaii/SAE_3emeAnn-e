"""
    insertion_formulaire.py
    Ce script permet de traiter les données du formulaire 
    Il traite les données du formulaire, les nettoie et les prépare pour l'insertion dans la base de données.
    Il génère également des fichiers CSV pour peupler les tables de la base de données.
    authors : Yanis Ponthou, Lucas Desperrois
"""

# Import des bilibothèques
import re
from unidecode import unidecode
from rapidfuzz import process, fuzz
import pandas as pd
import numpy as np
import ast


###----------###

# Les Fonctions de traitements

# Fonction qui renomme les colonnes du dataframe et retourne le dataframe
def renameColumnDf(df :pd.DataFrame):
    # Renommage des colonnes
    return df.rename(columns={"J'accepte que mes données soient utilisées dans le cadre de ce projet, conformément à la politique de confidentialité.":"confidentialite","êtes-vous ? ":"genre_humain","Quel âge avez vous ? (ex : 20 ans)":"age","Dans quel secteur travaillez-vous ?":"secteur","Êtes-vous familier avec la lecture ?":"familie_lecture","Pourquoi lisez-vous ?":"raison_lecture","Où lisez vous ?":"lieu_lecture","Vous préférez lire":"prefere_lire","Quels sont vos principaux critères pour choisir un livre ?":"critere_livre","Durée de lecture d'un livre de 200 pages ?":"duree_livre_200","Méthode de découverte de nouveaux livres ?":"decouverte_livre","Quel est le genre qui vous attire le plus parmi ceux-là ?":"genre","Quel sous genre historique vous intéresse ?":"sous_genre_historique","Quel genre/courant philosophique vous intéresse ?":"genre_philosophie","Quel sous genre de fantaisie vous intéresse ?":"sous_genre_fantaisie","Quel sous genre  policier  vous intéresse ?":"sous_genre_policier","Quels sont les autres genres qui vous attire ? (Hors celui déjà choisi)":"autre_genre_attire","Quels sont vos auteurs favoris ?":"auteur_favori"})
    

# Fonction qui traite les valeurs du dataframe en prenant une liste de nom de colonne en paramètres et retourne le dataframe
def deleteInutileColumn(df :pd.DataFrame,listNameDelete : list[str]):
    df = df.drop(listNameDelete,axis=1)
    return df

# Fusione les colonnes de sous genres de science fiction
def fusionColumn(df :pd.DataFrame):
   df["sous_genre_science_fiction"] = pd.concat([df["Quel sous genre de Science-fiction vous intéresse ?.1"], df["Quel sous genre de Science-fiction vous intéresse ?"]],ignore_index=True)
   return df;

# Trate les Nan d'un dataFrame
def traitementNaNetChaineInutile(df:pd.DataFrame):
    df.replace('', np.nan, inplace=True)
    for columns in df.columns:
        df[columns] = df[columns].fillna("-1")
    return df;

# Fonction qui transforme les les chaines d'age en entier (20ans : 20)
def transformAge(df:pd.DataFrame):
    df['age'] = df['age'].apply(lambda x: int(re.search(r'\b\d+\b', str(x)).group()) if re.search(r'\b\d+\b', str(x)) else None)
    return df

# Fonction pour traiter les formats des noms d'auteurs saisie dans le formulaire
def applyAuteurSeparator(row):
    # On remplace les "et" et ", " par ","
    # Remplacer les occurrences spécifiques ", " et " ," par une virgule
    row = re.sub(r',\s+|\s+,', ',', row)

    row = re.sub(r'\s+$', '',row)
    # Remplacer " - " (avec espaces éventuels mais pas ceux suivie d'un 1) et "et" par une virgule
    row = re.sub(r'\s*-\s*(?!\d)', ',', row)
    # Supprimer les espaces inutiles autour des virgules
    row = re.sub(r'\s*,\s*', ',', row)
    # Remplacer les "et" par une virgule
    row = re.sub(r'\s*et\s*', ',', row)
    # Supprime les / avec espaces
    row = re.sub(r'\s*/\s*', ',', row)
    # Supprime les & avec espaces
    row = re.sub(r'\s*&\s*', ',', row)
    # Éliminer espaces en début de chaine
    row = re.sub(r'^ +','',row)
    # Retirer les points de fin de phrase
    row = re.sub(r'[\.…]', '',row)
    # Retirer les deux points en fin de phrase
    row = re.sub(r':$','',row) 
    row = re.sub(r',$', '', str(row))
    # motifs à supprimer
    motifs = [" etc","  pour la detente"," et tant d'autres"," et tant d'autres",",et plein d'autres !",",et beaucoup d'autres"]
    pattern = "|".join(map(re.escape, motifs))  # Rejoint les motifs avec des 'ou' (|) et échappe les caractères spéciaux
    return re.sub(pattern, '', row)  # Remplace tous les motifs par ''
    return row

# Fonction pour traiter la familiarité avec la lecture
def treatmentFamilieLecture(df: pd.DataFrame):
    # Initialiser les listes pour les familles de lecture
    listeFamilleLecture = []
    listeFamilleLectureUser = []    
    familie_lecture_dict = {}
    familie_lecture_id = 1
    # On traite la colonne familie_lecture
    df['familie_lecture'] = df['familie_lecture'].apply(lambda x: x.lower())
    df['familie_lecture'] = df['familie_lecture'].apply(lambda x: unidecode(x))
    # On parcout le dataframe
    for i, row in df.iterrows():
        familie_lecture = row['familie_lecture'] 
        # si pas de -1 (valeur à pas traiter)
        if familie_lecture not in familie_lecture_dict and familie_lecture != '-1':
            # On l'ajoute au dictionne familie_lecture
            familie_lecture_dict[familie_lecture] = familie_lecture_id
            listeFamilleLecture.append({'id_familie_lecture': familie_lecture_id, 'familie_lecture': familie_lecture})
            familie_lecture_id += 1
        if familie_lecture == '-1':
            df.at[i, 'id_selection'] = "-1"
        else:
            # on l'ajoute l'association user familie_lecture
            df.at[i, 'id_selection'] = familie_lecture_dict.get(familie_lecture, None)
    # Rajotu d'une colonne pour les valeurs non renseignées
    row_vide = {'id_familie_lecture': 5, 'familie_lecture': 'nonrenseigne'}
    listeFamilleLecture.append(row_vide)
    # Conversion en dataframe et csv
    peuplementFamilleLecture = pd.DataFrame(listeFamilleLecture)
    peuplementFamilleLecture.to_csv("scripts_insertions/peuplement_formulaire_familie_lecture.csv", index=False)
    return df

# Fonction pour nettoyer et normaliser les genres
def clean_genre(genre):
    genre = genre.strip().lower()
    genre = unidecode(genre)
    genre = genre.replace(' ', '').replace('.', '').replace(')', '')
    return genre

# Fonction pour appliquer les transformations habituelles aux genres
def apply_remplacement_genre(genre):
    phrases_specifiques = [
        "pasconcernej'aidejachoisiavant", "j'aidejachoisiavant", "cesontlesmemeschoixdoncriendeplusametrre", 
        "lisantvraimentdetout", "ilestdifficiledechoisir", "leslivresdontonretireunelecondevie", 
        "sociologiemaispasdethemeparticulier", "jalterneeconomie"
    ]
    declencheurs = ["pas", "aucun", "plus", "trop", "vraiment"]
    phrases_bizzares = ["dependdumomententretouscesgenres", "feelgood", "histoirevraiestemoignage", "histoirevraitemoignage", "feelsgood"]
    # On traite les valeurs non renseignées ou non souhaitable qui sont des valeurs à ne pas traiter
    if not isinstance(genre, str) :
        return "-1"
    genre_clean = unidecode(genre.lower().strip())
    
    if genre_clean in phrases_specifiques:
        return "-1"
    if any(trigger in genre_clean for trigger in declencheurs):
        return "-1"
    for parcours in phrases_bizzares:
        if parcours in genre_clean:
            genre_clean = genre_clean.replace(parcours, '')
    return genre_clean

# Fonction pour traiter les genres
def treatmentGenre(df: pd.DataFrame):
    listeGenres = []
    listeGenresUser = []
    nouveaux_genres = []
    # Charger les genres existants depuis peuplement_genre_livre.csv
    genres_existants = pd.read_csv("scripts_insertions/peuplement_genre_livre.csv")
    genres_existants["genre_clean"] = genres_existants["genre"].str.lower().str.replace(" ", "")
    genres_dict = {row['genre_clean']: row['id_genre'] for _, row in genres_existants.iterrows()}
    genre_id = max(genres_dict.values()) + 1 

    # Combiner toutes les colonnes de genres et sous-genres en une seule colonne
    df['all_genres'] = df[['genre', 'sous_genre_historique', 'genre_philosophie', 'sous_genre_fantaisie', 'sous_genre_policier', 'autre_genre_attire', 'sous_genre_science_fiction']].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)

    df['all_genres'] = df['all_genres'].apply(lambda x: x.lower())
    df['all_genres'] = df['all_genres'].apply(lambda x: unidecode(x))
    df['all_genres'] = df['all_genres'].apply(lambda x: x.replace(';', ','))
    df['all_genres'] = df['all_genres'].apply(lambda x: x.replace('.', ''))  # Correction: enlever les points
    df['all_genres'] = df['all_genres'].apply(lambda x: x.replace(')', ''))  # Correction: enlever les parenthèses
    df['all_genres'] = df['all_genres'].apply(lambda x: x.split(','))  # Correction: split par ','
    # On parcout le dataframe
    for i, row in df.iterrows():
        for genre in row['all_genres']:
            genre = genre.strip()
            
            genre = apply_remplacement_genre(genre)
            # si pas de -1 (valeur à pas traiter)
            if genre and genre != '-1' and genre != '' and genre!='1' :
                genre_clean = genre.lower().replace(" ", "")
                match_found = False

                # Utiliser rapidfuzz pour trouver les correspondances avec les genres existants
                best_match = process.extractOne(genre_clean, genres_dict.keys(), scorer=fuzz.ratio, score_cutoff=70)
                if best_match:
                    matched_genre = best_match[0]
                    listeGenresUser.append({'id_user': i + 1, 'id_genre': genres_dict[matched_genre]})
                    match_found = True
                # Si aucune correspondance trouvée, vérifier chaque partie des noms existants en les splitant
                if not match_found and genre!="-1" and genre !='""' :
                    nouveaux_genres.append({'id_genre': genre_id, 'genre': genre})
                    listeGenresUser.append({'id_user': i + 1, 'id_genre': genre_id})
                    genres_dict[genre_clean] = genre_id
                    genre_id += 1
    # Conversion en dataframe et csv
    peuplementGenresUser = pd.DataFrame(listeGenresUser)
    peuplementGenresUser.to_csv("scripts_insertions/peuplement_formulaire_genres_user.csv", index=False)
    peuplementGenres = pd.DataFrame(nouveaux_genres)
    peuplementGenres.to_csv("scripts_insertions/peuplement_updated_genre.csv", index=False)
    return df
# Fonction pour traiter preferences lectures
def treatmentPrefereLire(df: pd.DataFrame):
    # Initialiser les listes pour les preferences de lecture
    listePrefereLire = []
    listePrefereLireUser = []
    prefere_id=1
    prefere_lire_dict = {}
    # On traite la colonne prefere_lire
    df['prefere_lire'] = df['prefere_lire'].apply(lambda x: x.lower())
    df['prefere_lire'] = df['prefere_lire'].apply(lambda x: unidecode(x))
    df['prefere_lire'] = df['prefere_lire'].apply(lambda x: x.replace(';', ','))
    df['prefere_lire'] = df['prefere_lire'].apply(lambda x: x.replace('.', ''))  # Correction: enlever les points
    df['prefere_lire'] = df['prefere_lire'].apply(lambda x: x.replace(')', ''))  # Correction: enlever les parenthèses
    df['prefere_lire'] = df['prefere_lire'].apply(lambda x: x.split(','))  # Correction: split par ','
    # On parcout le dataframe
    for i, row in df.iterrows():
        for prefere_lire in row['prefere_lire']:
            prefere_lire = prefere_lire.strip()
            # si pas de -1 (valeur à pas traiter)
            if prefere_lire and prefere_lire != '-1':
                if prefere_lire not in prefere_lire_dict:
                    # On l'ajoute au dictionne des preferences
                    prefere_lire_dict[prefere_lire] = prefere_id
                    listePrefereLire.append({'id_prefere_lire': prefere_id, 'prefere_lire': prefere_lire})
                    prefere_id += 1
                # on l'ajoute l'association user preference
                listePrefereLireUser.append({'id_user': i + 1, 'prefere_lire': prefere_lire_dict[prefere_lire]})
                if prefere_lire == '-1':
                    df.at[i, 'id_prefere_lire'] = "-1"
                else:
                    df.at[i, 'id_prefere_lire'] = prefere_lire_dict[prefere_lire]
    newRowPrefereLire = {'id_prefere_lire': 0, 'prefere_lire': 'inconnu'}
    listePrefereLire.append(newRowPrefereLire)
    # Conversion en dataframe et csv
    peuplementUserPrefereLire = pd.DataFrame(listePrefereLireUser)
    peuplementUserPrefereLire.to_csv("scripts_insertions/peuplement_formulaire_prefere_lire_user.csv", index=False)
    peuplementPrefereLire = pd.DataFrame(listePrefereLire)
    df['id_prefere_lire'] = df['id_prefere_lire'].fillna("-1")
    peuplementPrefereLire.to_csv("scripts_insertions/peuplement_formulaire_prefere_lire.csv", index=False)
    return df

# Fonction pour traiter les méthodes de découverte de lecture
def treatmentDecouverteLivre(df: pd.DataFrame):
    # Initialiser les listes pour les méthodes de découverte de lecture
    listeDecouverteLivre = []
    listeDecouverteLivreUser = []
    decouverte_livre_dict = {}
    decouverte_id = 1
    # On traite la colonne decouverte_livre
    df['decouverte_livre'] = df['decouverte_livre'].apply(lambda x: x.lower())
    df['decouverte_livre'] = df['decouverte_livre'].apply(lambda x: unidecode(x))
    df['decouverte_livre'] = df['decouverte_livre'].apply(lambda x: x.replace(';', ','))
    df['decouverte_livre'] = df['decouverte_livre'].apply(lambda x: x.replace('.', ''))  # Correction: enlever les points
    df['decouverte_livre'] = df['decouverte_livre'].apply(lambda x: x.replace(')', ''))  # Correction: enlever les parenthèses
    df['decouverte_livre'] = df['decouverte_livre'].apply(lambda x: x.split(','))  # Correction: split par ','
    # On parcout le dataframe
    for i, row in df.iterrows():
        for decouverte_livre in row['decouverte_livre']:
            decouverte_livre = decouverte_livre.strip()
            # si pas de -1 (valeur à pas traiter)
            if decouverte_livre and decouverte_livre != '-1':
                if decouverte_livre not in decouverte_livre_dict:
                    # On l'ajoute au dictionne des preferences
                    decouverte_livre_dict[decouverte_livre] = decouverte_id
                    listeDecouverteLivre.append({'id_decouverte_livre': decouverte_id, 'decouverte_livre': decouverte_livre})
                    decouverte_id += 1
                # on l'ajoute l'association user preference
                listeDecouverteLivreUser.append({'id_user': i + 1, 'id_decouverte_livre': decouverte_livre_dict[decouverte_livre]})
    # Conversion en dataframe et csv
    peuplementDecouverteLivreUser = pd.DataFrame(listeDecouverteLivreUser)
    peuplementDecouverteLivreUser.to_csv("scripts_insertions/peuplement_formulaire_decouverte_livre_user.csv", index=False)
    peuplementDecouverteLivre = pd.DataFrame(listeDecouverteLivre)
    peuplementDecouverteLivre.to_csv("scripts_insertions/peuplement_formulaire_decouverte_livre.csv", index=False)
    return df

# Fonction pour traiter les secteurs
def treatmetSecteur(df: pd.DataFrame):
    # Initialisation des listes pour les secteurs
    listeNouveauSecteurs = []
    secteurs_dict = {}
    secteur_id = 1

    df['secteur'] = df['secteur'].apply(lambda x: x.lower())

    df['secteur'] = df['secteur'].apply(lambda x: unidecode(x))
    df['secteur'] = df['secteur'].replace("jesuisencoreetudiant,eninformatique.", "informatique/technologie")
    df['secteur'] = df['secteur'].apply(lambda x: "retraite" if "retraite" in x else x)
    # On parcout le dataframe
    for i, row in df.iterrows():
        secteur = row['secteur']
        # si pas de -1 (valeur à pas traiter)
        if secteur not in secteurs_dict and secteur != '-1':
            secteurs_dict[secteur] = secteur_id
            listeNouveauSecteurs.append({'id_secteur': secteur_id, 'secteur': secteur})
            secteur_id += 1
        if secteur == '-1':
            df.at[i, 'id_secteur'] = "-1"
        else:
            # on l'ajoute l'association user secteur
            df.at[i, 'id_secteur'] = secteurs_dict[secteur]
    # Ajout d'une ligne pour les valeurs non renseignées
    newRowSecteurVideo = {'id_secteur': 0, 'secteur': 'inconnu'}
    listeNouveauSecteurs.append(newRowSecteurVideo)
    # Conversion en dataframe et csv
    peuplementSecteur = pd.DataFrame(listeNouveauSecteurs)
    peuplementSecteur.to_csv("scripts_insertions/peuplement_formulaire_secteur.csv", index=False)
    return df
  
# Fonction pour traiter les genres
def treatmentLieuxLecture(df: pd.DataFrame):
    # Initialisation des listes pour les lieux de lecture
    listeLieuxLecture = []
    listeLieuxUser = []
    lieux_dict = {}
    lieu_id = 1
    # On traite la colonne lieu_lecture
    df['lieu_lecture'] = df['lieu_lecture'].apply(lambda x: x.lower())
    df['lieu_lecture'] = df['lieu_lecture'].apply(lambda x: unidecode(x))
    df['lieu_lecture'] = df['lieu_lecture'].apply(lambda x: x.replace('?', ''))
    df['lieu_lecture'] = df['lieu_lecture'].apply(lambda x: x.split(';'))  # Correction: split par ';'
    # On parcout le dataframe
    for i, row in df.iterrows():
        for lieu in row['lieu_lecture']:
            lieu = lieu.strip()
            if lieu and lieu != '-1':
                if lieu not in lieux_dict:
                    # On l'ajoute au dictionne des lieux
                    lieux_dict[lieu] = lieu_id
                    listeLieuxLecture.append({'id_lieu': lieu_id, 'lieu': lieu})
                    lieu_id += 1
                # on l'ajoute l'association user lieu
                listeLieuxUser.append({'id_user': i + 1, 'id_lieu': lieux_dict[lieu]})
    # Conversion en dataframe et csv
    peuplementLieuxUser = pd.DataFrame(listeLieuxUser)
    peuplementLieuxUser.to_csv("scripts_insertions/peuplement_formulaire_lieux_user.csv", index=False)
    peuplementLieuxLecture = pd.DataFrame(listeLieuxLecture)
    peuplementLieuxLecture.to_csv("scripts_insertions/peuplement_formulaire_lieux_lecture.csv", index=False)
    return df

#   Fonction pour traiter la vitesse de lecture
def treatementVitesseLecture(df: pd.DataFrame):
    # Initialisation des listes pour les vitesses de lecture
    listeVitesseLecture = []
    df['duree_livre_200'] = df['duree_livre_200'].apply(lambda x: x.lower())
    df['duree_livre_200'] = df['duree_livre_200'].apply(lambda x: unidecode(x))
    vitesse_dict = {}
    vitesse_id = 1
    # On parcout le dataframe
    for i, row in df.iterrows():
        vitesse = row['duree_livre_200']
        # si pas de -1 (valeur à pas traiter)
        if vitesse not in vitesse_dict and vitesse != '-1':
            # On l'ajoute au dictionne des vitesses
            vitesse_dict[vitesse] = vitesse_id
            listeVitesseLecture.append({'id_vitesse_lecture': vitesse_id, 'vitesse_lecture': vitesse})
            vitesse_id += 1
        if vitesse == '-1':
            df.at[i, 'id_vitesse_lecture'] = "-1"
        else:
            # on l'ajoute l'association user vitesse
            df.at[i, 'id_vitesse_lecture'] = vitesse_dict[vitesse]
    # Ajout d'une ligne pour les valeurs non renseignées
    peuplementVitesseLecture = pd.DataFrame(listeVitesseLecture)
    peuplementVitesseLecture.to_csv("scripts_insertions/peuplement_formulaire_vitesse_lecture.csv", index=False)
    return df
# Fonction pour traiter les utilisateurs
def treatmentUser(df: pd.DataFrame):
    # Initialiser les listes pour les utilisateurs
    listeUsers = []

    df = transformAge(df)
    for i, row in df.iterrows():
        # On utilsie les valeurs créer par les autres traitement sur chaque
        # Ligne du questionnaire traité pour créer un utilisateur (voir le modèle de données)
        user_info = {
            'id_user': i + 1,
            'age': row['age'],
            'id_secteur': 0 if row.get('id_secteur', 0) == "-1" else row.get('id_secteur', None),
            'id_vitesse_lecture': 3 if row.get('id_vitesse_lecture', 3) == "-1" else row.get('id_vitesse_lecture', None),
            'id_selection': 5 if row.get('id_selection', 5) == "-1" else row.get('id_selection', None),
            'id_genre_sex': 1 if row.get('genre_humain') == 'Homme' else 0,
            'id_prefere_lire': 0 if row.get('id_prefere_lire', 0) == "-1" else row.get('id_prefere_lire', None),
        }
        listeUsers.append(user_info)
    # Conversion en dataframe et csv
    peuplementUsers = pd.DataFrame(listeUsers)
    
    # Convertir les colonnes id en type int
    peuplementUsers['id_user'] = peuplementUsers['id_user'].astype(int)
    peuplementUsers['id_secteur'] = peuplementUsers['id_secteur'].astype(int)
    peuplementUsers['id_vitesse_lecture'] = peuplementUsers['id_vitesse_lecture'].astype(int)
    peuplementUsers['id_selection'] = peuplementUsers['id_selection'].astype(int)
    peuplementUsers['id_genre_sex'] = peuplementUsers['id_genre_sex'].astype(int)
    peuplementUsers['id_prefere_lire'] = peuplementUsers['id_prefere_lire'].astype(int)
    
    peuplementUsers.to_csv("scripts_insertions/peuplement_formulaire_users.csv", index=False)
    return df
# Fonction pour traiter les criteres de lecture
def treatmentCriteres(df: pd.DataFrame):
    listeCriteres = []
    listeCriteresUser = []
    criteres_dict = {}
    critere_id = 1

    df['critere_livre'] = df['critere_livre'].apply(lambda x: x.lower())
    df['critere_livre'] = df['critere_livre'].apply(lambda x: unidecode(x))
    df['critere_livre'] = df['critere_livre'].apply(lambda x: x.replace(';', ','))
    df['critere_livre'] = df['critere_livre'].apply(lambda x: x.replace('.', ''))  # Correction: enlever les points
    df['critere_livre'] = df['critere_livre'].apply(lambda x: x.replace(')', ''))  # Correction: enlever les parenthèses
    df['critere_livre'] = df['critere_livre'].apply(lambda x: x.split(','))  # Correction: split par ','

    for i, row in df.iterrows():
        for critere in row['critere_livre']:
            # Séparer les critères contenant "et", "et/ou" et "/"
            sous_criteres = re.split(r'\bet\b|et/ou|/', critere)
            for sous_critere in sous_criteres:
                sous_critere = sous_critere.strip()
                if sous_critere and sous_critere != '-1':
                    if sous_critere not in criteres_dict:
                        criteres_dict[sous_critere] = critere_id
                        listeCriteres.append({'id_critere': critere_id, 'critere': sous_critere})
                        critere_id += 1
                    listeCriteresUser.append({'id_user': i + 1, 'id_critere': criteres_dict[sous_critere]})

    peuplementCriteresUser = pd.DataFrame(listeCriteresUser)
    peuplementCriteresUser.to_csv("scripts_insertions/peuplement_formulaire_criteres_user.csv", index=False)
    peuplementCriteres = pd.DataFrame(listeCriteres)
    peuplementCriteres.to_csv("scripts_insertions/peuplement_formulaire_criteres.csv", index=False)
    return df

# Fonction pour traiter les raisons de lecture
def traitementRaisonLecture(df: pd.DataFrame):
    # Initialiser les listes pour les raisons de lecture
    listeRaisons = []
    listeRaisonsUser = []
    raisons_dict = {}
    raison_id = 1
    # On traite la colonne raison_lecture
    df['raison_lecture'] = df['raison_lecture'].apply(lambda x: x.lower())
    df['raison_lecture'] = df['raison_lecture'].apply(lambda x: unidecode(x))
    df['raison_lecture'] = df['raison_lecture'].apply(lambda x: x.replace('?', ''))
    df['raison_lecture'] = df['raison_lecture'].apply(lambda x: x.replace('.',''))  
    df['raison_lecture'] = df['raison_lecture'].apply(lambda x: x.replace('!',''))  
    df['raison_lecture'] = df['raison_lecture'].apply(lambda x: x.split(';'))  # Correction: split par ';'
   

    # On parcout le dataframe
    for i, row in df.iterrows():
        for raison in row['raison_lecture']:
            raison = raison.strip()
            # si pas de -1 (valeur à pas traiter)
            if raison and raison != '-1':
                if raison not in raisons_dict:
                    # On l'ajoute au dictionne des raisons
                    raisons_dict[raison] = raison_id
                    listeRaisons.append({'id_raison': raison_id, 'raison': raison})
                    raison_id += 1
                # on l'ajoute l'association user raisons
                listeRaisonsUser.append({'id_user': i + 1, 'id_raison': raisons_dict[raison]})
    # Conversion en dataframe et csv
    peuplementRaisonsUser = pd.DataFrame(listeRaisonsUser)
    peuplementRaisonsUser.to_csv("scripts_insertions/peuplement_formulaire_raisons_user.csv", index=False)
    peuplementRaisons = pd.DataFrame(listeRaisons)
    peuplementRaisons.to_csv("scripts_insertions/peuplement_formulaire_raisons.csv", index=False)
    return df

# Fonction pour nettoyer et normaliser les noms d'auteurs
def clean_author_name(name):
    """Nettoie et normalise les noms d'auteurs tout en gardant les espaces."""
    return unidecode(name).strip().lower()

# Fonction pour appliquer les transformations habituelles aux auteurs
def apply_remplacement(phrase):
    phrase = unidecode(phrase.lower().strip())
    phrases_specifiques = [
        "l'auteur ne m'importe peu", "Jsp", "Aucun en particulier", "?", "", 
        "c'est selon l'histoire", "AFNOR", "t", "c", "p", "Jsp", "Coll", 
        "beaucoup d'autres", "je laisse la chance a tous a partir du moment ou le resume me plait", 
        "developpement personnel avec l'accord tollteque", "le mois d'or pour ce qui concerne la grossesse", 
        "plein d'autres !","tant d'autres","autres","jsp"
    ]
    declencheurs = ["pas", "aucun", "plus", "trop", "l'auteur ne m'importe peu", "vraiment"]
    phrases_bizzares = [",et beaucoup d'autres", " et autres", "Vraiment ! Comment choisir ? Entre les pepites en autoedition et ce en me Je dirais "]
    # Remplacer les occurrences spécifiques,", " et " ," par une virgule
    if not isinstance(phrase, str):
        return "-1"
    
    if phrase in phrases_specifiques:
        return "-1"
    if any(trigger in unidecode(phrase.lower()) for trigger in declencheurs):
        return "-1"
    for parcours in phrases_bizzares:
        if parcours in phrase:
            phrase = phrase.replace(parcours, '')
    return phrase

# Fonction pour traiter les auteurs
def treatmentAuteur(df: pd.DataFrame):
    listeAuteursUser = []
    nouveaux_auteurs = []
    nouveaux_auteurs_set = set()  # Ensemble pour suivre les auteurs déjà ajoutés
    
    # Charger les auteurs existants depuis peuplement_auteurs.csv
    auteurs_existants = pd.read_csv("scripts_insertions/peuplement_auteurs.csv")
    auteurs_existants["author_name_clean"] = auteurs_existants["author_name"].apply(clean_author_name)
    auteurs_dict = {row['author_name_clean']: row['author_id'] for _, row in auteurs_existants.iterrows()}
    auteur_id = max(auteurs_dict.values()) + 1 if auteurs_dict else 1

    # Appliquer les transformations sur la colonne 'auteur_favori'
    df['auteur_favori'] = df['auteur_favori'].apply(applyAuteurSeparator)
    df['auteur_favori'] = df['auteur_favori'].apply(lambda x: [unidecode(a).strip() for a in x.split(',')])
    df['auteur_favori'] = df['auteur_favori'].apply(lambda x: [apply_remplacement(a) for a in x])
    df['auteur_favori'] = df['auteur_favori'].apply(lambda x: [a for a in x if a != '-1'])
    df['auteur_favori'] = df['auteur_favori'].astype(str)
    for i, row in df.iterrows():
        id_user = i + 1
        try:
            auteurs = ast.literal_eval(row['auteur_favori'])  # Convertir la chaîne de caractères en liste
        except (ValueError, SyntaxError):
            continue  # Ignorer les lignes avec des valeurs invalides
        
        for auteur in auteurs:
            if auteur == '-1':
                continue
            auteur_clean = clean_author_name(auteur)
            match_found = False

            # Comparer l'auteur avec les auteurs existants en utilisant RapidFuzz
            best_match = process.extractOne(
                auteur_clean, 
                auteurs_dict.keys(), 
                scorer=fuzz.ratio, 
                # Nous avons choisi un seuil de similarité à 80%
                score_cutoff=80  
            )
            # Si match à 80%
            if best_match:
                matched_author_clean, score = best_match[0], best_match[1]
                listeAuteursUser.append({'id_user': id_user, 'id_auteur': auteurs_dict[matched_author_clean]})
                match_found = True

            # Si aucune correspondance trouvée, vérifier chaque partie des noms existants
            if not match_found:
                for existing_author_clean in auteurs_dict.keys():
                    existing_author_parts = existing_author_clean.split()
                    for part in existing_author_parts:
                        best_match = process.extractOne(
                            auteur_clean, 
                            [part], 
                            scorer=fuzz.ratio, 
                            score_cutoff=85  
                        )
                        if best_match:
                            matched_author_clean, score = best_match[0], best_match[1]
                            listeAuteursUser.append({'id_user': id_user, 'id_auteur': auteurs_dict[existing_author_clean]})
                            match_found = True
                            break
                    if match_found:
                        break
            
            
            # Si la correspondance n'est pas trouvée, ajouter l'auteur comme nouveau
            if not match_found:
                # Si aucune correspondance trouvée, ajouter l'auteur comme nouveau
                if auteur_clean not in nouveaux_auteurs_set:
                    nouveaux_auteurs.append({'author_id': auteur_id, 'author_name': auteur,'id_genre_sex':2})
                    nouveaux_auteurs_set.add(auteur_clean)
                    listeAuteursUser.append({'id_user': id_user, 'id_auteur': auteur_id})
                    auteurs_dict[auteur_clean] = auteur_id
                    auteur_id += 1
                else:
                    # Si l'auteur existe déjà dans les nouveaux auteurs, utiliser l'ID existant
                    existing_auteur_id = [a['author_id'] for a in nouveaux_auteurs if a['author_name'] == auteur][0]
                    listeAuteursUser.append({'id_user': id_user, 'id_auteur': existing_auteur_id})

    # Sauvegarder les résultats dans des fichiers CSV
    peuplementAuteursUser = pd.DataFrame(listeAuteursUser)
    peuplementAuteursUser.to_csv("scripts_insertions/peuplement_formulaire_users_auteurs.csv", index=False)
    peuplementAuteurs = pd.DataFrame(nouveaux_auteurs)
    peuplementAuteurs.to_csv("scripts_insertions/peuplement_updated_auteur.csv", index=False)
    return df

#------------#

# Fonction qui lance les transformations sur la dataFrame
def treatmentFormulaire():
    # Stock les réponses du formulaire dans df
    df = pd.read_csv("Questionnaire.csv")
    # Je renomme les colonnes
    df = renameColumnDf(df)
    # Je fusionne plusieurs colonne du meme nom (sous-genre-science-fiction)
    df = fusionColumn(df)
    # Je supprime les colonnes inutiles ( les colonnes utilee à la fusion, horodateur)
    df = deleteInutileColumn(df,['Horodateur','Quel sous genre de Science-fiction vous intéresse ?.1','Quel sous genre de Science-fiction vous intéresse ?'])
    # Supprime les NaN
    df = traitementNaNetChaineInutile(df=df)
    # On traite le secteur de travail
    df = treatmetSecteur(df=df)
    # On traite les genre de lecture
    df = treatmentGenre(df=df)
    # On traite la vitesse de lecture
    df = treatementVitesseLecture(df=df)
    # On traite les lieux de lecture
    df = treatmentLieuxLecture(df=df)
    # On traite les criteres de lecture
    df = treatmentCriteres(df=df)
    # On traite la familiarite avec la lecture
    df = treatmentFamilieLecture(df=df)
    # On traite les raisons de lecture
    df = traitementRaisonLecture(df=df)
    # On traite prefere lire
    df = treatmentPrefereLire(df=df)
    # On traite la decouverte de livre
    df = treatmentDecouverteLivre(df=df)
    # On traite les users
    df = treatmentUser(df=df)
    # On traite les auteurs
    df = treatmentAuteur(df=df)
    # tous les changements visible sur ce csv
    df.to_csv("questionnaire_traite.csv", index=False)

# Lancement du traitement sur le csv du questionnaire
treatmentFormulaire()






    


