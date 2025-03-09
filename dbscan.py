from analyseACM import mca_result
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


# Standardisation des coordonnées pour DBSCAN
scaler = StandardScaler()
mca_scaled = scaler.fit_transform(mca_result)


# Appliquer DBSCAN
dbscan = DBSCAN(
    eps=0.5, min_samples=5
)  # Ajustez `eps` et `min_samples` selon vos besoins
clusters = dbscan.fit_predict(mca_scaled)


# Visualiser les clusters dans le premier plan factoriel
plt.figure(figsize=(8, 6))
plt.scatter(
    mca_result[:, 1], mca_result[:, 0], c=clusters, cmap="viridis", s=50, alpha=0.7
)
plt.title("DBSCAN Clusters sur le plan factoriel 1-2")
plt.xlabel("Dimension 2")
plt.ylabel("Dimension 1")
plt.colorbar(label="Cluster")
plt.show()
