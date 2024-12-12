from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import torch

# Charger le modèle et le tokenizer BERT
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Exemple de genres (descriptions ou noms)
genres = ["Mystery", "Thriller", "Romance", "Fantasy", "Science Fiction"]

# Tokeniser et encoder les genres
embeddings = []
for genre in genres:
    inputs = tokenizer(genre, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    embeddings.append(outputs.last_hidden_state.mean(dim=1).detach().numpy())


# Calculer la similarité du cosinus entre tous les genres
similarity_matrix = cosine_similarity(embeddings)

# Afficher la matrice de similarité
similarity_df = pd.DataFrame(similarity_matrix, index=genres, columns=genres)
print(similarity_df)