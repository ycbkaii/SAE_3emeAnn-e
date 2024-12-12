from gensim.models import Word2Vec
from matplotlib import pyplot
from sklearn.decomposition import PCA
import pandas as pd
from gensim.models import FastText

csv_genre = pd.read_csv("csv/peuplement_genre_livre.csv", index_col="id")

data = (
    csv_genre["genre"]
    .str.split("-", expand=True)[0]
    .reset_index(name="genre")["genre"]
    .apply(lambda x: [x])
    .to_list()
)

# model = Word2Vec(
#     sentences=data, vector_size=4, window=5, min_count=1, workers=4, sg=1
# )

model = FastText(vector_size=4, window=3, min_count=1)  # instantiate

model.build_vocab(corpus_iterable=data)

model.train(corpus_iterable=data, total_examples=len(data), epochs=10)

print(model.wv.similar_by_key('Romance'))

raise

X = model.wv.vectors

pca = PCA(n_components=2)
result = pca.fit_transform(X)

pyplot.scatter(result[:, 0], result[:, 1])
words = model.wv.index_to_key
for i, word in enumerate(words):
    pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()
