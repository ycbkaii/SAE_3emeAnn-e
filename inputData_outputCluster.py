
import psycopg2
from k_means_clustering_ACM import mca_df, dataFromCsv
from scipy.spatial.distance import euclidean


conn = psycopg2.connect(database="masterbook",
                    port="5433",
                    user="root",
                    host="localhost",
                    password="root"
                    )
cursor = conn.cursor()
print("Connected")


# TODO Ici on recoit l'ID de l'utilisateur qui vient de se connecter pour l'affichage de ses recommandations
target_id = 10
target_point = mca_df.loc[target_id, ['Dim1', 'Dim2']].values

# On recupere le cluster associé à la target point
cluster_point = mca_df.loc[target_id, 'Cluster']


print(target_point)

# On exclu les clusters qui ne sont pas associés
mca_df = mca_df[mca_df["Cluster"] == cluster_point]

# On calcule la distance entre les points et le target point 
mca_df["distance_to_target"] = mca_df.apply(lambda row: euclidean(target_point, [row["Dim1"], row["Dim2"]]), axis=1)


# On prend les 10 points les plus proches
points_les_plus_proches = mca_df.drop(index=target_id).sort_values(by="distance_to_target")[:10]
print(points_les_plus_proches)

# On affiche les utilisateurs qui sont les plus proches de notre target
for i in points_les_plus_proches.index :
    print(f"{dataFromCsv.loc[i]}\n\n")
    
# TODO Faire SQL pour afficher les livres en rapport

# query="SELECT * from masterbook._publisher;"
# cursor.execute(query)

# tuples = cursor.fetchall()

# print(tuples)

conn.commit()
conn.close()
print("Connexion closed")