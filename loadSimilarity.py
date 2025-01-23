import pandas as pd

# print(cosine_similarity(pd.read_csv("./vectGenre.csv",index_col="id_genre").to_numpy())[-1][-2])
print("---------------------------------------------------------------")
# print(euclidean_distances(pd.read_csv("./vectGenre.csv").to_numpy())[204][100])
print("---------------------------------------------------------------")
print(pd.read_csv("./cosineSimGenre.csv",index_col="id_genre").to_numpy()[2])
