import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("questionnaire_traite.csv")

data = data[data["confidentialite"] != "Non"]

total_genre = data["genre"].drop_duplicates()

total_genre = total_genre[total_genre.str.split().str.len() < 2]

sous_genre_historique = [
    "Roman Antique",
    "Roman historique",
    "Documents/Archives historiques",
    "Récit médiéval",
]
sous_genre_fantasy = [
    "Romantic fantasy",
    "Dark fantasy",
    "Fantasy humoristique",
    "L’héroïque fantasy / Sword and sorcery",
    "Modern fantasy",
]


sous_genre_policier = set()
sous_genre_science_fiction = set()
genre_philosophie = set()


def splitgenre(row, sous_genre: set):
    for e in row.split(";"):
        if e != "-1" and e != "Aucun" and len(e.split(",")) < 2 :
            sous_genre.add(e)


data["sous_genre_policier"].drop_duplicates().apply(
    lambda x: splitgenre(x, sous_genre_policier)
)
data["sous_genre_science_fiction"].drop_duplicates().apply(
    lambda x: splitgenre(x, sous_genre_science_fiction)
)
data["genre_philosophie"].drop_duplicates().apply(
    lambda x: splitgenre(x, genre_philosophie)
)


def hoe_sous_genre(row: str, sous_genre):
    result = [1 if genre in row else 0 for genre in sous_genre]
    return result


def hoe_genre(row, total_genre: pd.DataFrame):
    genre_list = total_genre.to_list()
    result = [2 if genre in row else 0 for genre in genre_list]
    return result


dfVectorize = pd.DataFrame(
    [],
    columns=["Age", "Genre","Vitesse lecture"]
    + total_genre.to_list()
    + sous_genre_historique
    + sous_genre_fantasy
    + list(sous_genre_policier)
    + list(sous_genre_science_fiction)
    + list(genre_philosophie),
)


def vectorizeRow(row):
    tabGenre = {"Homme": 1, "Femme": 2, "Non binaire": 3}
    tabVitesseLecture = {
        "je ne le lis pas": 0,
        "1 a 2 semaines": 2,
        "entre 3 jours et une semaines": 3,
        "2-3 jour ou moins": 4,
        "1 mois ou +": 5,
    }
    rowSelect = row[
        [
            "age",
            "genre_humain",
            "genre",
            "sous_genre_historique",
            "sous_genre_fantaisie",
            "sous_genre_policier",
            "sous_genre_science_fiction",
            "genre_philosophie",
            "duree_livre_200"
        ]
    ]
    age = rowSelect["age"] / 100
    vit_lecture = tabVitesseLecture[rowSelect["duree_livre_200"]]
    genreSexe = tabGenre[rowSelect["genre_humain"]]
    vect_genre = hoe_genre(rowSelect["genre"], total_genre)
    vect_sous_genre_historique = hoe_sous_genre(
        rowSelect["sous_genre_historique"], sous_genre_historique
    )
    vect_sous_genre_fantasy = hoe_sous_genre(
        rowSelect["sous_genre_fantaisie"], sous_genre_fantasy
    )
    vect_sous_genre_policier = hoe_sous_genre(
        rowSelect["sous_genre_policier"], sous_genre_policier
    )
    vect_sous_genre_science_fiction = hoe_sous_genre(
        rowSelect["sous_genre_science_fiction"], sous_genre_science_fiction
    )
    vect_genre_philosophie = hoe_sous_genre(
        rowSelect["genre_philosophie"], genre_philosophie
    )

    dfVectorize.loc[row.name] = (
        [age]
        + [genreSexe]
        + [vit_lecture]
        + vect_genre
        + vect_sous_genre_historique
        + vect_sous_genre_fantasy
        + vect_sous_genre_policier
        + vect_sous_genre_science_fiction
        + vect_genre_philosophie
    )


data.apply(vectorizeRow, axis=1)
dfVectorize.to_csv("userVectorize.csv",index_label="id_user")
print(cosine_similarity(dfVectorize))
