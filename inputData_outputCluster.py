import psycopg2
from k_means_clustering_ACM import mca_df, dataFromCsv
from scipy.spatial.distance import euclidean

from utilities import getBooksById


def acmReco(userId: int, mca_df=mca_df):
    conn = psycopg2.connect(
        database="masterbook",
        port="5433",
        user="root",
        host="localhost",
        password="root",
    )
    cursor = conn.cursor()
    print("Connected")

    # TODO Ici on recoit l'ID de l'utilisateur qui vient de se connecter pour l'affichage de ses recommandations et on fait un transform pour l'integrer dans les clusters
    target_id = userId
    target_point = mca_df.loc[target_id, ["Dim1", "Dim2"]].values

    # On recupere le cluster associé à la target point
    cluster_point = mca_df.loc[target_id, "Cluster"]

    print(target_point)

    # On exclu les clusters qui ne sont pas associés
    mca_df = mca_df[mca_df["Cluster"] == cluster_point]

    # On calcule la distance entre les points et le target point
    mca_df["distance_to_target"] = mca_df.apply(
        lambda row: euclidean(target_point, [row["Dim1"], row["Dim2"]]), axis=1
    )

    # On prend les 10 points les plus proches
    points_les_plus_proches = mca_df.drop(index=target_id).sort_values(
        by="distance_to_target"
    )[:10]
    print(points_les_plus_proches)

    # On affiche les utilisateurs qui sont les plus proches de notre target
    print(f"Target Point : \n {dataFromCsv.loc[target_id]}\n\n")
    for i in points_les_plus_proches.index:
        print(f"{dataFromCsv.loc[i]}\n\n")

    # Fonction pour afficher les "''"
    def escapeString(row):
        if row != None:
            return row.replace("'", "''")

    dataFromCsv["genre"] = dataFromCsv["genre"].apply(escapeString)

    # Le genre qu'on retrouve le plus de fois
    genres_le_plus_linked = (
        dataFromCsv.loc[[i for i in points_les_plus_proches.index]]
        .groupby("genre")
        .count()
        .sort_values(by="genre_humain")
    )
    if len(genres_le_plus_linked) >= 2:
        genres_le_plus_linked = genres_le_plus_linked[-2:]
    genres_le_plus_linked = genres_le_plus_linked.index.to_numpy()

    # On regarde si les personnes du cluster sont familiés avec la lecture
    familieLecture = (
        dataFromCsv.loc[[i for i in points_les_plus_proches.index]]
        .groupby("familie_lecture")
        .count()
        .idxmax()[0]
    )

    print(f"Genres proposés :{genres_le_plus_linked}")
    print(f"Familiarité générale avec la lecture : {familieLecture}")

    # On définit des constantes pour savoir si la durée du livre en fonction de la familiarité de l'utilisateur
    FACHE = "<=100"
    MOYEN = ">100 AND number_of_page<=170"
    CONTENT = ">170 AND number_of_page<=230"
    JADORE_LIRE = ">230"
    nb_pages_sql_query = ">0"

    if familieLecture == "fache":
        nb_pages_sql_query = FACHE
    elif familieLecture == "moyen":
        nb_pages_sql_query = MOYEN
    elif familieLecture == "content":
        nb_pages_sql_query = CONTENT
    elif nb_pages_sql_query == "j'adore lire":
        nb_pages_sql_query = JADORE_LIRE

    # Les genres selected
    if len(genres_le_plus_linked) == 2:
        genre_selected = f"nom_genre = '{genres_le_plus_linked[1]}'"
        genre_selected_2 = f"nom_genre = '{genres_le_plus_linked[0]}'"
    else:
        genre_selected = f"nom_genre = '{genres_le_plus_linked[1]}'"
        genre_selected_2 = genre_selected

    # TRaduire la philosophie
    if genre_selected == "nom_genre = 'Philosophie'":
        genre_selected = "nom_genre = 'Philosophy'"
    elif genre_selected_2 == "nom_genre = 'Philosophie'":
        genre_selected_2 = "nom_genre = 'Philosophy'"

    # TRaduire la fantaisie
    if genre_selected == "nom_genre = 'Fantaisie'":
        genre_selected = "nom_genre = 'Fantasy'"
    elif genre_selected_2 == "nom_genre = 'Fantaisie'":
        genre_selected_2 = "nom_genre = 'Fantasy'"

    # TODO Faire SQL pour afficher les livres en rapport
    queryToSelectBooksFirstGenre = f"(SELECT id_livre ,title, average_rating FROM masterbook._livre NATURAL JOIN masterbook._genres_du_livre NATURAL JOIN masterbook._genre WHERE (number_of_page {nb_pages_sql_query}) AND average_rating > 4.0 AND rating_count >= 300 AND ({genre_selected}))" 

    queryToSelectBooksSecondGenre = f"(SELECT id_livre ,title, average_rating FROM masterbook._livre NATURAL JOIN masterbook._genres_du_livre NATURAL JOIN masterbook._genre WHERE (number_of_page {nb_pages_sql_query}) AND average_rating > 4.0 AND rating_count >= 300 AND ({genre_selected_2}))" 

    queryToSelectBooks = f"SELECT * FROM ({queryToSelectBooksFirstGenre} UNION {queryToSelectBooksSecondGenre}) ORDER BY average_rating DESC LIMIT 10"

    cursor.execute(queryToSelectBooks)

    tuples = cursor.fetchall()

    print(f"Les livres proposés : {tuples}\n")
    
    print(f"A partir des IDS on a ces livres : {getBooksById(tuples)}\n")

    conn.commit()
    conn.close()
    print("Connexion closed")
    
    return getBooksById(tuples)

