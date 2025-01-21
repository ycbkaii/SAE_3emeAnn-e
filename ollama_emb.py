import ollama
import pandas as pd
import datetime as dt
import threading

# model = "mxbai-embed-large"
model = "snowflake-arctic-embed2"

books = pd.read_csv("csv/bigboss_book.csv")

description= books[["description"]]

def embedText(text: str):
    return ollama.embed(model=model, input=text)

start = dt.datetime.now()

def embedDesc() :
    for e in description.sample(1000).to_numpy() :
        embedText(str(e))

list_thread : list[threading.Thread]= []

for i in range(1,6) :
    list_thread.append(threading.Thread(target=embedDesc,name="Thread "+str(i)))

for t in list_thread :
    t.start()

for t in list_thread :
    t.join()

end = dt.datetime.now()
print((end - start).total_seconds())