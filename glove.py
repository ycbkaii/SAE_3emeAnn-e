from gensim.models import KeyedVectors

glove_file = 'glove.840B.300d.txt'

model = KeyedVectors.load_word2vec_format(glove_file,binary=False,no_header=True)

print(model)