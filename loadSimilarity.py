import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

cosSimGenreBooks =  cosine_similarity(pd.read_csv("./vectGenre.csv",index_col="id_genre").to_numpy())
# print("---------------------------------------------------------------")
vectDescBooks =  pd.read_feather("./vectDesc1024")
print(vectDescBooks)
vectDescBooks = vectDescBooks.to_numpy()
def calcSim2Books(id_books1,id_books2 ) :
    livre1 : np.ndarray = vectDescBooks[id_books1]
    livre2 : np.ndarray = vectDescBooks[id_books2]
    return cosine_similarity(livre1.reshape(1,-1),livre2.reshape(1,-1))

#print(calcSim2Books(42708,43277))