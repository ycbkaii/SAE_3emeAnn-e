import pandas as pd
import matplotlib.pyplot as plt

# On récupere le fichier csv et on nettoie ce dernier
data = pd.read_csv("csv/bigboss_book.csv", low_memory=False)

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
count_autre = data_autre_genre.sum(numeric_only=True)["count"]
df_autre = pd.DataFrame(
    {"genre_grp": "Other (less than 3.4 percent)", "count": count_autre}, index=[1]
)  # On crée la ligne "autre" dans un nouveau dataFrame


data_genre_principale = pd.concat(
    [data_genre_principale, df_autre], ignore_index=True
)  # On concatène


total_data_autre_genre = data_autre_genre.sum(numeric_only=True)["count"]
total_data_principale_genre = data_genre_principale.sum(numeric_only=True)["count"]


def calcPoucentageAutreGenre(row):
    return (row["count"] / total_data_autre_genre) * 100


def categorizeAutreGenre(row):
    if row["pourcentage"] > 5:
        return "More than 5%"
    elif row["pourcentage"] >= 1:
        return "Between 5% and 1%"
    elif row["pourcentage"] >= 0.1:
        return "Between 1% and 0.1%"
    else :
        return "Less than 0.1%"

def calcPoucentagePrincipaleGenre(row):
    return (row["count"] / total_data_principale_genre) * 100


data_autre_genre = pd.concat(
    [data_autre_genre, data_autre_genre.apply(calcPoucentageAutreGenre, axis=1)], axis=1
).rename(columns={0: "pourcentage"})

data_autre_genre = pd.concat(
    [data_autre_genre, data_autre_genre.apply(categorizeAutreGenre, axis=1)], axis=1
).rename(columns={0: "cat"})


distrib_autre_genre = data_autre_genre.groupby("cat").count().reset_index()

data_principale_pourcentage = data_genre_principale.apply(
    calcPoucentagePrincipaleGenre, axis=1
)

labels = data_genre_principale["genre_grp"]
labels = labels.to_list()
data_principale_pourcentage = data_principale_pourcentage.to_list()
tmp_labels = []
for i in range(len(labels)):
    prct = data_principale_pourcentage[i]
    tmp_labels.append(labels[i] + " - " + str(round(prct, 3)) + "%")


labels = tmp_labels

labels_autre = distrib_autre_genre["cat"].drop_duplicates()

fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(100, 100), subplot_kw=dict(aspect="equal")
)

explode = ([0] * 9) + [0.1]
wedges, texts, autotexts = ax1.pie(
    data_genre_principale["count"].to_numpy(),
    startangle=90,
    autopct="%1.2f%%",
    radius=1.2,
    explode=explode,
)

ax1.legend(
    wedges,
    labels,
    title="Gender",
    loc="upper left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

plt.setp(texts, size=10)

ax1.set_title("Principal gender pie chart")

def prctCatAutre(row) :
    return row["count"]/196
# bar chart parameters
genre_ratios = distrib_autre_genre.apply(prctCatAutre,axis=1).to_list()
print(distrib_autre_genre)
bottom = 1
width = .2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(genre_ratios, labels_autre)])):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                 alpha=0.1 + 0.25 * j)
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

ax2.set_title('Other Gender repartition')
ax2.legend()
ax2.axis('off')
ax2.set_xlim(- 2.5 * width, 2.5 * width)
plt.show()
