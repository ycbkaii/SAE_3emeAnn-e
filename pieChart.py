import pandas as pd
import matplotlib.pyplot as plt

# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv")

variables = [
    "author",
    "rating_count",
    "review_count",
    "average_rating",
    "genre_and_votes",
    "series",
    "five_star_ratings",
    "four_star_ratings",
    "three_star_ratings",
    "two_star_ratings",
    "one_star_ratings",
    "number_of_pages",
    "publisher",
    "date_published",
]

# On nettoie et on garde que les données qu'on va utiliser
data = data[variables]


# On isole le genre le plus voté pour chaque livre
data_first_genre = data["genre_and_votes"].str.split(",", expand=True)[0]

# On sépare la catégorie du nombre de vote
data_first_genre = data_first_genre.str.split("[0-9]", expand=True, regex=True)[
    0
].to_frame()

# FAUT REGROUPER LES CATEGORIE

data_genre = data_first_genre.groupby(0).size().reset_index(name="count")

data_sans_underscore = data_genre[0].str.split("-", expand=True)[0].str.strip()


data_genre["genre_grp"] = data_sans_underscore

data_genre_bien = (
    data_genre.groupby("genre_grp")  # On groupe par genre
    .sum()  # on calcule la taille
    .sort_values("count", axis=0, ascending=False)  # On trie de manière déscendante
    .reset_index()  # On reset l'index du dataframe
    .drop(0, axis=1)  # On supprime la colonne avec les ancien genre
)

data_genre_principale = data_genre_bien.iloc[:9]
data_autre_genre = data_genre_bien.iloc[9:]
count_autre = data_autre_genre.sum(numeric_only=True).to_list()[0]

df_autre = pd.DataFrame(
    {"genre_grp": "Other (less than 3.4 percent)", "count": count_autre}, index=[1]
)  # On crée la ligne "autre" dans un nouveau dataFrame


data_genre_principale = pd.concat(
    [data_genre_principale, df_autre], ignore_index=True
)  # On concatène

labels = data_genre_principale["genre_grp"]

labels_autre = data_autre_genre["genre_grp"]


fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(100, 100), subplot_kw=dict(aspect="equal")
)

explode =([0] * 9) + [0.1]
wedges, texts, autotexts = ax1.pie(
    data_genre_principale["count"].to_numpy(),
    startangle=90,
    autopct="%1.2f%%",
    radius=1.2,
    explode=explode
)

# TODO voir si on peut mettre les pourcentage sur la légende

ax1.legend(
    wedges,
    labels.to_list(),
    title="Gender",
    loc="upper left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

plt.setp(autotexts, size=10)

ax1.set_title("Principal gender pie chart")

wedges2, texts2, autotexts2 = ax2.pie(
    data_autre_genre["count"].to_numpy(),
    startangle=90,
    autopct="%1.1f%%",
)

ax2.legend(
    wedges2,
    labels_autre.to_list(),
    title="Gender",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

ax2.set_title("Other gender pie chart")
#plt.show()
