import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity,euclidean_distances

print(cosine_similarity(pd.read_csv("./vectGenre.csv").to_numpy())[204][100])
print("---------------------------------------------------------------")
print(euclidean_distances(pd.read_csv("./vectGenre.csv").to_numpy())[204][100])
print("---------------------------------------------------------------")
# print(pd.read_csv("./cosineSimGenre.csv").to_numpy()[-1])