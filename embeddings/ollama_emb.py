import ollama
import pandas as pd
import threading

MODEL = "bge-m3"  # Le meilleurs pour les desc


def check_ollama():
    try:
        ollama.pull(MODEL)
        ollama.embed(model=MODEL, input="test")
        return "Ollama is running and ready for embed"
    except Exception as e:
        return e


def embed_text(text: str):
    return ollama.embed(model=MODEL, input=text, options={"num_ctx": 8192})


def embed_desc_all():
    description = pd.read_csv("csv/bigboss_book.csv", usecols=["description"],index_col="id")
    def embed_desc(list_res: list, start_i: int, end_i: int):
        for e in description.to_numpy()[start_i:end_i]:
            list_res.append(embed_text(str(e))["embeddings"][0])

    list_embedings = []
    for j in range(13):
        indice = j * 4000
        list_thread: list[threading.Thread] = []
        for i in range(4):
            start = i * 1000 + indice
            end = (i + 1) * 1000 + indice
            print(end, start)
            list_thread.append(
                threading.Thread(
                    target=embed_desc,
                    name="Thread " + str(i),
                    args=(list_embedings, start, end),
                )
            )
        for t in list_thread:
            t.start()
        for t in list_thread:
            t.join()
        print(len(list_embedings[0]))
    embed_desc(list_embedings, 52000, 52200)
    return list_embedings


def saveVectDesc():
    resEmbedDesc = embed_desc_all()
    pd.DataFrame(resEmbedDesc).to_csv("./vectDesc1024.csv", index_label="id_livre")

saveVectDesc()