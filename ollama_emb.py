import ollama
import pandas as pd
import datetime as dt
import threading
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# model = "nomic-embed-text" # Un blanced
# model = "snowflake-arctic-embed2" # Le plus gros
model = "all-minilm:33m" # Le plus petit

books = pd.read_csv("csv/bigboss_book.csv")
genre = pd.read_csv("csv/peuplement_genre_livre.csv",index_col="id").to_numpy()
description= books[["description"]]


def embedText(text: str):
    return ollama.embed(model=model, input=text)

start = dt.datetime.now()

def embedDesc(listRes : list) :
    for e in description.sample(1).to_numpy() :
        listRes.append(embedText(str(e))["embeddings"])

def embedDescAll() :
    list_thread : list[threading.Thread]= []
    listEmb = []
    for i in range(1,5) :
        list_thread.append(threading.Thread(target=embedDesc,name="Thread "+str(i),args=(listEmb,)))
    for t in list_thread :
        t.start()
    for t in list_thread :
        t.join()
    print(listEmb)


# embedDescAll()

def embedGenreAll() :
    listVecGenre = []
    for gen in genre :
        listVecGenre.append(embedText(str(gen))["embeddings"][0])
    return listVecGenre

embedGenre = embedGenreAll()
pd.DataFrame(embedGenre).to_csv("./vectGenre.csv")
pd.DataFrame(cosine_similarity(embedGenre)).to_csv("./cosineSimGenre.csv",index_label="id_genre")
end = dt.datetime.now()
print((end - start).total_seconds())