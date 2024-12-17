from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import torch

# Charger le modèle et le tokenizer BERT
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)


# Définir la fonction de traitement du texte
def traitement_texte(texte):
    # Tokeniser le texte
    encoding = tokenizer.encode_plus(
        texte,
        truncation=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors="pt",
    )
    encoding.to(device)
    # Exécuter le modèle BERT
    outputs = model(encoding["input_ids"], attention_mask=encoding["attention_mask"])

    # Récupérer la représentation du texte
    representation = outputs.last_hidden_state[:, 0, :]

    return representation


# Définir les genres de livres
csv_genre = pd.read_csv("bdd_docker/csv/formulaire/peuplement_updated_genre.csv", index_col="id_genre")

genres = (
    csv_genre["genre"]
    .str.split("-", expand=True)[0]
    .reset_index(name="genre")["genre"]
    .drop_duplicates()
    .to_list()
)

genre_principaux = [
    "Fantasy",
    "Fiction",
    "Romance",
    "Young Adult",
    "Nonfiction",
    "Historical",
    "Mystery",
    "Science Fiction",
    "Sequential Art"
]

# Traiter les genres pour produire des représentations
representations = {}
for genre in genres:
    representations[genre] = traitement_texte(genre)

for genre in genre_principaux:
    representations[genre] = traitement_texte(genre)


# Calculer la similitude entre les genres
similaires = {}
for i, genre1 in enumerate(genres):
    similaires[genre1] = []
    for j, genre2 in enumerate(genre_principaux):
            if device != "cpu":
                similarity = torch.cosine_similarity(
                    representations[genre1], representations[genre2]
                )
            else:
                similarity = cosine_similarity(
                    representations[genre1].detach().numpy(),
                    representations[genre2].detach().numpy(),
                )
            similaires[genre1].append((genre2, similarity.item()))

# Afficher les résultats
# for genre1, similaires_genre2 in similaires.items():
#     print(f"Similarité entre {genre1} et les autres genres :")
#     for genre2, similarity in similaires_genre2:
#         print(f"- {genre2}: {similarity:.4f}")

data = pd.DataFrame(similaires)

data.to_csv("sim.csv")