from analyseACM import mca_result
from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt


# On prépare le clustering pour entrainer notre IA non-supervisé


# K-Means sur les coordonnées

# On applique K-means avec un différent nombre de clusters
distortions = []
K = [i for i in range(1, 10)]

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(mca_result)
    distortions.append(kmeans.inertia_)

# On fait la méthode du coude pour savoir combien de clusters on va garder
# plt.figure(figsize=(8, 5))
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('Nombre de Clusters (k)')
# plt.ylabel('Distorsion')
# plt.title('Méthode du Coude pour déterminer k optimal')
# plt.show()

# ON mentionne K = 4
k = 4

kmeans = KMeans(n_clusters=k, random_state=42)
kmeans.fit(mca_result)

# Ajout des clusters aux résultats ACM pour visualisation
clusters = kmeans.labels_
mca_df = pd.DataFrame(
    mca_result, columns=[f"Dim{i + 1}" for i in range(mca_result.shape[1])]
)
mca_df["Cluster"] = clusters

# Visualisation des clusters sur les deux premières dimensions
plt.figure(figsize=(8, 5))
for cluster in range(k):
    cluster_points = mca_df[mca_df["Cluster"] == cluster]
    plt.scatter(
        cluster_points["Dim2"],
        cluster_points["Dim1"],
        label=f"Cluster {cluster}",
        alpha=0.6,
    )

    # Ajout de titres pour les points (l'id des utilisateurs)
    for i, row in cluster_points.iterrows():
        plt.text(row["Dim2"], row["Dim1"], str(i), fontsize=8, alpha=0.7, color="black")

# plt.title('Clusters après K-means (ACM)')
# plt.xlabel('Dimension 1')
# plt.ylabel('Dimension 2')
# plt.legend()
# plt.grid()
# plt.show()

print(mca_df)
