import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
from sqlalchemy import create_engine
from utilities import getBooksById

def acpReco(target_id : int) :
    # CONSTANTE
    # target_id = 20
    Nombre_livre = 10

    # host = "localhost"       # Adresse de la BDD
    host = "localhost"
    port = 5433              # Port par défaut de PostgreSQL
    database = "masterbook"     # Nom de la base
    user = "root" # Nom d'utilisateur
    password = "root" # Mot de passe

    # Créer l'objet de connexion
    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

    # print(engine)


    # On récupere le fichier csv et on nettoie ce dernier
    # data = pd.read_csv("questionnaire_traite.csv")
    # print(test)
    # total_genre = pd.read_csv("peuplement_genre_livre.csv")
    query = "SELECT DISTINCT ON (_utilisateur.id_user) _utilisateur.id_user, _utilisateur.id_secteur, _utilisateur.id_prefere_lire, _genre_personne.nom_genre AS genre_humain, age, nom_categorie AS duree_livre_200, nom_humeur AS familie_lecture, _genre.nom_genre AS genre FROM masterbook._utilisateur LEFT JOIN masterbook._genre_aime ON _genre_aime.id_user = _utilisateur.id_user LEFT JOIN masterbook._genre ON _genre_aime.id_genre = _genre.id_genre NATURAL JOIN masterbook._vitesse_de_lecture NATURAL JOIN masterbook._mood_selection LEFT JOIN masterbook._genre_personne ON id_genre_sex = _genre_personne.id_genre ORDER BY _utilisateur.id_user ;"
    data = pd.read_sql_query(query, engine)


    query = "SELECT * FROM masterbook._genre"
    total_genre = pd.read_sql_query(query, engine)
    # print(total_genre)
    total_genre = total_genre.rename(columns={'nom_genre': 'genre'})



    # Supprimer les espaces en début et fin de chaîne
    total_genre['genre'] = total_genre['genre'].str.strip()

    # Mettre toutes les chaînes en minuscules pour éviter les doublons liés à la casse
    total_genre['genre'] = total_genre['genre'].str.lower()

    # Supprimer les doublons
    total_genre = total_genre.drop_duplicates(subset=['genre'], keep='first')

    # On récupere les colonnes et on les transforme
    variables = [
        "id_user",
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

    # On supprime les data qui possèdent -1
    data = data[data['genre_humain'] != '-1']
    data = data[~data['genre'].isna()]



    data_verif = data[variables]

    data_verif = data_verif.reset_index(drop=True)
    data = data.reset_index(drop=True)
    # Réindexer le DataFrame sur 'id_user' pour garantir un accès direct
    data = data.set_index("id_user")
    data_verif = data_verif.set_index("id_user")

    # print(data_verif)


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
        elif row == "entre 3 jours et une semaines":
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

    def hoe_genre_cleaned(row):
        if(row != None) :
            genre_list = total_genre["genre"].tolist()
            row = row.strip()
            row= row.lower()
            result = [1 if genre in row else 0 for genre in genre_list]
            return result

    data['genre'] = data['genre'].apply(hoe_genre_cleaned) 

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

    # print(data)

    # data["genre_humain"] = data["genre_humain"].dropna()


    # On standardise les données
    temp = data.sub(data.mean())



    # x_scaled qui est le jeu de data standardisées où on effectura l'ACP
    x_scaled = temp.div(data.std())
    # print(" ")
    # print(" ")
    # print("hop hop hop")
    # print(" ")
    # print(x_scaled)
    x_scaled = x_scaled.fillna(0)


    # print(x_scaled)

    # print(x_scaled.isnull().sum()) 




    #region Mise en place pour les variables 
    pca = PCA(n_components=6)
    pca.fit(x_scaled)

    pca_res = pca.fit_transform(x_scaled)

    # print(pca_res)

    # On recupere les valeurs propres des composantes
    valeursPropre = pca.singular_values_

    # On recupere le pourcentage des valeurs propres
    pourcentValeursPropre = pca.explained_variance_ratio_

    # print(f"Affichage des valeurs propres : {valeursPropre}\n")
    # print(f"Pourcentage valeurs propres : {pourcentValeursPropre}\n")

    #CREATION TABLE QUI RESUME LES VALEURS PROPRES
    tableauACP = pd.DataFrame({
        "Dimension " : ["Dim" + str (x + 1) for  x in range (6)],
        "Valeur propre" : str(valeursPropre),
        "% valeur propre" : np.round(pourcentValeursPropre * 100),
        "% cum. val. prop." : np.round(np.cumsum(pourcentValeursPropre) * 100)
    })

    # print(f"TableauACP qui résume les valeurs propres :\n {tableauACP}\n")


    # Mise en place du graphique des variables
    y1 = list(pourcentValeursPropre)
    x1 = range(len(y1))
    # biplot(pca=pca,components=[0,1],x=x_scaled,cat=y1[0:1],density=False)
    # plt.show()
    #endregion


    # K-MEANS

    data_scaled = pca_res

    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt

    # Calcul de l'inertie pour différents k
    inertias = []
    range_k = range(1, 11) 

    for k in range_k:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data_scaled)
        inertias.append(kmeans.inertia_)

    # print(f"Inertie : {inertias}")

    # Calcul des différences successives entre les inerties
    inertia_diff = np.diff(inertias)
    # print(f"Inertie différence : {inertia_diff}")

    # Calcul de la deuxième différence (pour détecter le coude)
    inertia_diff2 = np.diff(inertia_diff)
    # print(f"Inertie différence seconde : {inertia_diff2}")

    optimal_k = np.argmin(inertia_diff2) + 3  
    # print(f"Le nombre optimal de clusters selon la méthode du coude est : {optimal_k}")

    # Visualisation pour vérifier le coude (avec un marker sur k optimal)
    plt.plot(range_k, inertias, marker='o', label='Inertie')
    plt.axvline(x=optimal_k, color='r', linestyle='--', label=f"Optimal k = {optimal_k}")
    plt.title("Méthode du Coude")
    plt.xlabel("Nombre de Clusters k")
    plt.ylabel("Inertie")
    plt.legend()
    # plt.show()


    from sklearn.metrics import silhouette_score

    for k in range(2, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(data_scaled)
        score = silhouette_score(data_scaled, labels)
        # print(f"Silhouette Score for k={k}: {score}")

    k = optimal_k
    # k = 5
    kmeans = KMeans(n_clusters=k, random_state=42)
    data['cluster'] = kmeans.fit_predict(data_scaled)


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


    # plt.show()


    # Ajouter une colonne 'user_id' si ce n'est pas déjà fait
    data['user_id'] = data.index

    # Regrouper les utilisateurs par cluster
    clusters = data.groupby('cluster')['user_id'].apply(list)

    # Afficher les utilisateurs par cluster
    # print(clusters)

    from scipy.spatial.distance import euclidean

    # Récupérer les centroids des clusters
    centroids = kmeans.cluster_centers_

    # Calculer les distances entre chaque paire de centroids
    distances_between_centroids = pd.DataFrame(
        [[euclidean(centroids[i], centroids[j]) for j in range(len(centroids))] for i in range(len(centroids))],
        columns=[f'Cluster {i}' for i in range(len(centroids))],
        index=[f'Cluster {i}' for i in range(len(centroids))]
    )

    # Afficher la matrice de distances entre clusters
    # print(distances_between_centroids)

    from scipy.spatial.distance import euclidean

    def get_neighbors_in_cluster(target_id, data, pca_coords, n_neighbors=None):

        # Récupérer l'ID du cluster auquel appartient l'utilisateur cible
        target_cluster = data.loc[target_id, 'cluster']
        # print(target_cluster)
        
        # Filtrer les utilisateurs appartenant au même cluster
        same_cluster_users = data[data['cluster'] == target_cluster]
        # print(same_cluster_users)

        if(len(same_cluster_users) == 1):
            same_cluster_users = data['cluster']
        
        
        # Récupérer les indices des utilisateurs dans le cluster
        cluster_indices = same_cluster_users.index
        
        # Coordonées PCA de l'utilisateur cible
        target_coords = pca_coords[target_id]
        
        # Calculer la distance entre l'utilisateur cible et les autres utilisateurs dans le cluster
        distances = []
        for user_index in cluster_indices:
            if user_index != target_id:  # Ne pas inclure l'utilisateur cible lui-même
                if user_index != target_id and user_index < len(pca_coords):  
                    # print(f"user_index = {user_index}, max index possible = {len(pca_coords) - 1}")
                    dist = euclidean(target_coords, pca_coords[user_index])
                    distances.append((user_index, dist))
                else:
                    print(f"Ignoré : user_index {user_index} hors limites pour pca_coords")

        
        # Trier par distance croissante
        distances_sorted = sorted(distances, key=lambda x: x[1])
        
        # Limiter au nombre de voisins si spécifié
        if n_neighbors:
            distances_sorted = distances_sorted[:n_neighbors]
        
        return distances_sorted

    # data = data.reset_index(drop=True)  # Réinitialiser les indices du DataFrame

    neighbors = get_neighbors_in_cluster(target_id, data, data_scaled, n_neighbors=20)

    # for neighbor_id, distance in neighbors:
    #     print(f"ID: {neighbor_id}, Distance: {distance:.2f}")
    from scipy.spatial.distance import pdist, squareform

    # Calculer la matrice de distances entre les utilisateurs
    distance_matrix = squareform(pdist(data_scaled, metric='euclidean'))


    def extract_neighbors(neighbor, data):
        neighbors_df = data.iloc[0:0]
        # print(neighbors_df)
        # print(data)
        # print("voisin : ")
        # print(neighbor)
        # Parcourir chaque utilisateur
        for user in neighbor :
            # print("user : ")
            # print(user)
            # print(data.loc[[user[0]]])
            neighbors_df = pd.concat([neighbors_df, data.loc[[user[0]]]])

        return neighbors_df




    # Créer les DataFrames des voisins pour les deux ensembles
    neighbors_original = extract_neighbors(neighbors, data_verif)

    # print(" ")
    # print(" ")
    # HERE TARGET
    # print("Target : ")
    # print(data_verif.loc[[target_id]])
    # print(" ")
    # # Afficher les résultats
    # print("Voisins : ")
    # print(neighbors_original)


    neighbors_genres = neighbors_original["genre"].value_counts()

    # print("genres")
    # print(neighbors_genres)

    def transform_duree_in_nbPage(row):
        if row == "je ne le lis pas":
            return 100
        elif row == "1 mois ou +":
            return 200
        elif row == "1 a 2 semaines":
            return 500
        elif row == "entre 3 jours et une semaines":
            return 900
        elif row == "2-3 jour ou moins":
            return 100000
        else:
            return 100

    neighbors_original['duree_livre_200'] = neighbors_original['duree_livre_200'].apply(transform_duree_in_nbPage)


    neighbors_duree_livre = neighbors_original["duree_livre_200"].value_counts()

    # print("duree 200")
    # print(neighbors_duree_livre)



    neighbors_prefere_lire = neighbors_original["id_prefere_lire"].value_counts()

    # print("prefere_lire")
    # print(neighbors_prefere_lire)

    # TODO remplacer par bdd aussi
    # data2 = pd.read_csv("questionnaire_traite.csv")
    query = "SELECT DISTINCT ON (_utilisateur.id_user) _utilisateur.id_user, _utilisateur.id_secteur, _utilisateur.id_prefere_lire, _genre_personne.nom_genre AS genre_humain, age, nom_categorie AS duree_livre_200, nom_humeur AS familie_lecture, _genre.nom_genre AS genre, _auteur.nom_complet AS auteur_favori  FROM masterbook._utilisateur FULL OUTER JOIN masterbook._genre_aime ON _genre_aime.id_user = _utilisateur.id_user FULL OUTER JOIN masterbook._genre ON _genre_aime.id_genre = _genre.id_genre NATURAL JOIN masterbook._vitesse_de_lecture NATURAL JOIN masterbook._mood_selection INNER JOIN masterbook._genre_personne ON id_genre_sex = _genre_personne.id_genre LEFT JOIN masterbook._aime_auteur on _aime_auteur.id_user = _utilisateur.id_user LEFT JOIN masterbook._auteur ON _auteur.id_auteur = _aime_auteur.id_auteur ORDER BY _utilisateur.id_user ;"
    data2 = pd.read_sql_query(query, engine)

    data2 = data2[data2['genre_humain'] != '-1']

    data2 = data2.reset_index(drop=True)

    variable2 =[
        "genre_humain",
        "age",
        "genre", 
        "id_secteur",
        "duree_livre_200",
        "familie_lecture",
        "id_prefere_lire",
        "auteur_favori"
    ]

    data2 = data2[variable2]

    auteurs_list = []

    for id in neighbors_original.index :
        for auteur in data2.loc[[id]]["auteur_favori"]:
            # print(auteur)
            if( auteur != None) :
                auteur = auteur.replace('[', '')
                auteur = auteur.replace(']', '')
                auteur = auteur.replace('\'','')
            
            if(isinstance(auteur, list)) :
                # print("liste")
                for i in range(auteur.len()) :
                    auteurs_list.append(auteur)
                    # print(auteurs_list)
            else :
                auteurs_list.append(auteur)
                # print(auteurs_list)


    # TODO PROBLEME AVEC / genre_votes_filtrés[genre_id] !!!!

    def separer_elements_en_liste_plate(tableau):
        """
        Sépare les éléments d'un tableau à l'aide du délimiteur ',' et retourne une liste plate.

        :param tableau: Liste de chaînes à traiter
        :return: Liste plate contenant tous les éléments séparés
        """
        resultat = []
        for element in tableau:
            if element:  # Vérifie si l'élément n'est pas une chaîne vide
                noms = [nom.strip() for nom in element.split(',')]
                resultat.extend(noms)  # Ajoute les noms à la liste plate
        return resultat

    auteurs_list = separer_elements_en_liste_plate(auteurs_list)

    from collections import Counter
    auteurs_list = Counter(auteurs_list)
    # print(auteurs_list)


    ####################################################
    #  
    # RECUP BOOK & AUTHOR
    # 
    ####################################################



    # authors = pd.read_csv("Big_boss_authors.csv")
    # books = pd.read_csv("bigboss_book.csv")
    query = "SELECT * FROM masterbook._a_ecrit INNER JOIN masterbook._auteur ON _a_ecrit.id_auteur = _auteur.id_auteur INNER JOIN masterbook._livre ON _a_ecrit.id_livre = _livre.id_livre INNER JOIN masterbook._genres_du_livre ON _livre.id_livre = _genres_du_livre.id_livre"
    books = pd.read_sql_query(query, engine)
    books = books.loc[:, ~books.columns.duplicated()]
    books = books.drop_duplicates()
    # print(books.columns)


    query = "SELECT * FROM masterbook._genres_du_livre"
    genre_livre = pd.read_sql_query(query, engine)

    # print(genre_livre.columns)


    # Normalisation des auteurs et des genres recherchés
    auteurs_set = {auteur.upper() for auteur in auteurs_list}  
    # print(auteurs_set)
    genres_lower = set(neighbors_original["genre"].str.lower().str.strip())  
    total_genre["genre"] = total_genre["genre"].str.lower().str.strip()

    # Liste des seuils de pages à prendre en compte
    page_thresholds = sorted(neighbors_original["duree_livre_200"].unique())

    # Initialisation des structures
    livres_list = []
    livres_debug = []
    livres_seen = set()

    # Comptage des occurrences des livres et genres
    livres_count = Counter(livres_list)
    genres_count = Counter(neighbors_original["genre"])
    duree_count = Counter(neighbors_original["duree_livre_200"])

    # Poids par distance des voisins
    distance_weights = {user[0]: 1 / (1 + user[1]) for user in neighbors}

    # Normalisation des poids des durées
    if duree_count:
        max_duree_count = max(duree_count.values())
        duree_weight = {k: 1 + (v / max_duree_count) for k, v in duree_count.items()}
    else:
        duree_weight = {k: 1 for k in page_thresholds}

    # Filtrer les votes des genres pour ne garder que ceux présents dans neighbors_original["genre"]
    # genre_votes_filtrés = genre_livre.groupby("id_genre")["nombre_votes_utilisateur"].sum()
    # print(genre_votes_filtrés)

    genre_votes_filtrés_Init = genre_livre[genre_livre["id_genre"].isin(total_genre[total_genre["genre"].isin(genres_lower)]["id_genre"])]
    # print("++++++++++++++22222++++++++++++++++++")
    # print(genre_votes_filtrés_Init)
    # Normalisation des votes restants


    # Dictionnaire des scores pondérés des livres
    livres_scores = {}

    for _, row in books.iterrows():
        id_livre = row["id_livre"]
        id_genre = row["id_genre"]
        nb_pages = row["number_of_page"]
        duree_livre = row["number_of_page"]

        # Vérification si le livre est pertinent (auteur, genre ou durée)
        has_author = row["nom_complet"] in auteurs_set
        has_genre = id_genre in total_genre.index and total_genre.loc[id_genre, "genre"] in genres_lower
        has_duree = duree_livre in duree_count

        if not (has_author or has_genre or has_duree):
            continue  # Livre non pertinent

        # Poids basé sur la durée de lecture
        page_weight = duree_weight.get(duree_livre, 0.5)

        # Score initial
        score = 1.0

        # if (id_livre == 15782868) :
        #     print("initial")
        #     print(score)

        # Boost pour les auteurs préférés
        if row["nom_complet"] in auteurs_set:
            score += 1
        # if (id_livre == 15782868) :
        #     print("auteur")
        #     print(score)
        # Poids des occurrences du livre
        score += livres_count.get(id_livre, 0) * 2

        # if (id_livre == 15782868) :
        #     print("JSP auteur")
        #     print(score)

        # Récupérer tous les genres associés à ce livre dans la table books
        id_genres = books[books["id_livre"] == id_livre]["id_genre"].unique()
        # if (id_livre == 15782868) :
        # # print(id_genres)
        # # Score basé uniquement sur les genres pertinents du livre
        #     print("Genres de référence :", id_genres)
        #     print("Genres présents :", genre_votes_filtrés_Init["id_genre"].unique())

        genre_votes_filtrés = genre_votes_filtrés_Init[genre_votes_filtrés_Init["id_genre"].isin(id_genres)]
        # genre_score = 0
        # genre_count = 0
        # print("début")
        # print(score)
        # print("le reste : ")
        for genre_id in id_genres:
            # print(genre_id in genre_votes_filtrés["id_genre"])
            # print(genre_id)
            # if (id_livre == 15782868) :
            #     print(genre_id)
            #     print(genre_votes_filtrés["id_genre"])
            if genre_id in genre_votes_filtrés["id_genre"].values:
                # print("le nb vote = ")
                genre_votes_filtrés_Livre = genre_votes_filtrés[genre_votes_filtrés["id_livre"] == id_livre]
                # print(genre_votes_filtrés)
                # if (id_livre == 15782868) :
                #     print(genre_votes_filtrés_Livre["nombre_votes_utilisateur"].values) 
                score += genre_votes_filtrés_Livre["nombre_votes_utilisateur"].sum() * 10
                # print("le score")
                # print(genre_score)
                # genre_count += 1

        # Moyenne pondérée des genres pertinents
        # if genre_count > 0:
        #     genre_score /= genre_count  
        # else:
        #     genre_score = 0  

        # score += genre_score * 10  # Facteur ajustable

        # if (id_livre == 15782868) :
        #     print("Genre +")
        #     print(score)

        # Pénalité pour genres non pertinents
        nb_genres_non_pertinents = sum(1 for genre_id in id_genres if genre_id not in genre_votes_filtrés["id_genre"].values)
        score -= nb_genres_non_pertinents * 100

        # if (id_livre == 15782868) :
        #     print("Genre -")
        #     print(score)

        # Poids basé sur la proximité des voisins
        for user_id, distance in neighbors:
            if user_id in distance_weights:
                score += distance_weights[user_id] * 10

        # print(score)
        # Appliquer le poids des pages
        score *= page_weight

        # if (id_livre == 15782868) :
        #     print("Nb page")
        #     print(score)
        # print("plus le poid")
        # print(score)
        # Stocker le score final
        livres_scores[id_livre] = score

    # Normalisation des scores
    if livres_scores:
        # print(livres_scores)
        min_score = min(livres_scores.values())
        max_score = max(livres_scores.values())

        if max_score > min_score:
            livres_scores = {k: ((v - min_score) / (max_score - min_score)) * 100 for k, v in livres_scores.items()}

    # Sélection des livres recommandés (avant prise en compte des notes)
    livres_selectionnes = sorted(livres_scores.items(), key=lambda x: x[1], reverse=True)[:50]


    # Création d'une copie explicite pour éviter le SettingWithCopyWarning
    selected_books_df = books[books["id_livre"].isin([livre[0] for livre in livres_selectionnes])].copy()

    # Normalisation de la note moyenne
    if selected_books_df["average_rating"].max() > selected_books_df["average_rating"].min():
        selected_books_df.loc[:, "average_rating_norm"] = (selected_books_df["average_rating"] - selected_books_df["average_rating"].min()) / \
                                                        (selected_books_df["average_rating"].max() - selected_books_df["average_rating"].min())
    else:
        selected_books_df.loc[:, "average_rating_norm"] = 0.5  # Valeur neutre

    # Normalisation du nombre de votes
    if selected_books_df["rating_count"].max() > selected_books_df["rating_count"].min():
        selected_books_df.loc[:, "rating_count_norm"] = (selected_books_df["rating_count"] - selected_books_df["rating_count"].min()) / \
                                                        (selected_books_df["rating_count"].max() - selected_books_df["rating_count"].min())
    else:
        selected_books_df.loc[:, "rating_count_norm"] = 0.5  # Valeur neutre


    # Calcul du score final
    final_scores = {}
    for _, row in selected_books_df.iterrows():
        id_livre = row["id_livre"]
        base_score = dict(livres_selectionnes).get(id_livre, 0)

        rating_score = row["average_rating_norm"] * 2
        rating_count_score = row["rating_count_norm"] * 5

        final_scores[id_livre] = base_score + rating_score + rating_count_score

    # Trier les livres par score décroissant et récupérer uniquement les IDs
    top_livres = [livre[0] for livre in sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:Nombre_livre]]

    # Affichage des recommandations triées (seulement les IDs)
    # print(" ")
    # print(data_verif.loc[[target_id]])
    # print(" ")
    # print(" ")
    # # Afficher les résultats
    # print("Voisins : ")
    # print(neighbors_original)
    # print(f"\nTop {Nombre_livre} livres recommandés :")
    print(getBooksById(top_livres))
    # print(books.columns)
    for id in top_livres :
        # print(" ")
        book = books.loc[books["id_livre"] == id, ["id_livre", "title", "nom_complet", "number_of_page", "rating_count", "average_rating", "id_genre"]].drop_duplicates()
        # print(book[["id_livre", "title", "nom_complet", "number_of_page", "rating_count", "average_rating"]].drop_duplicates())
        # print('Genres :')
        genre_list = [] 
        for id_genre in book["id_genre"]:
            genres = total_genre.loc[total_genre["id_genre"] == id_genre, "genre"].tolist()
            genre_list.extend(genres)

        # print(genre_list) 
        # print(" ")


    # plt.show()
    return getBooksById(top_livres)

# acpReco(20)