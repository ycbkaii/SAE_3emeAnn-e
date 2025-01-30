import ollama
import pandas as pd
import datetime as dt
import threading

# model = "nomic-embed-text" # Un blanced
model = "bge-m3"  # Le plus gros
# model = "all-minilm:33m" # Le plus petit


def embedText(text: str):
    return ollama.embed(model=model, input=text, options={"num_ctx": 8192})


def embedDescAll():
    description = pd.read_csv("csv/bigboss_book.csv", usecols=["description"])

    def embedDesc(listRes: list, start: int, end: int):
        for e in description.to_numpy()[start:end]:
            listRes.append(embedText(str(e))["embeddings"][0])

    listEmb = []
    for j in range(13):
        indice = j * 4000
        list_thread: list[threading.Thread] = []
        for i in range(4):
            start = i * 1000 + indice
            end = (i + 1) * 1000 + indice
            print(end, start)
            list_thread.append(
                threading.Thread(
                    target=embedDesc,
                    name="Thread " + str(i),
                    args=(listEmb, start, end),
                )
            )
        for t in list_thread:
            t.start()
        for t in list_thread:
            t.join()
        print(len(listEmb[0]))
    embedDesc(listEmb, 52000, 52200)
    return listEmb


# embedDescAll()


def embedGenreAll():
    genre = pd.read_csv("csv/peuplement_genre_livre.csv", index_col="id").to_numpy()
    listVecGenre = []

    def processFils(start: bool):
        if start:
            for gen in genre[:400]:
                listVecGenre.append(embedText(str(gen))["embeddings"][0])
        else:
            for gen in genre[400:]:
                listVecGenre.append(embedText(str(gen))["embeddings"][0])

    thread1 = threading.Thread(
        target=processFils, args=[True], name="Tread pour le début"
    )
    thread2 = threading.Thread(
        target=processFils, args=[False], name="Tread pour la fin"
    )

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    return listVecGenre


def saveVectGenre():
    embedGenre = embedGenreAll()
    pd.DataFrame(embedGenre).to_csv("./vectGenre.csv", index_label="id_genre")


def saveVectDesc():
    resEmbedDesc = embedDescAll()
    pd.DataFrame(resEmbedDesc).to_csv("./vectDesc1024.csv", index_label="id_livre")


saveVectGenre()
saveVectDesc()
