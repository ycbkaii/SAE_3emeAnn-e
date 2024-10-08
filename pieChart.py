import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

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
data_first_genre = data_first_genre.str.split("[0-9]", expand=True, regex=True)[0].to_frame()
data_first_genre = data_first_genre.rename(columns={0: 'Cat originale'})


# On compte pour chaque catégorie
data_genre = data_first_genre.groupby('Cat originale').size().reset_index(name="count")

# On regroupe les catégorie en enlevant les sous-catégorie (ex : Youg Adult-Teen -> Youg Adult)
data_catégorie_princiale = data_genre['Cat originale'].str.split("-", expand=True)[0].str.strip()


data_genre["genre_grp"] = data_catégorie_princiale
data_genre_bien = (
    data_genre.groupby("genre_grp")  # On groupe par genre
    .sum()  # on calcule la taille
    .sort_values("count", axis=0, ascending=False)  # On trie de manière déscendante
    .reset_index()  # On reset l'index du dataframe
    .drop('Cat originale', axis=1)  # On supprime la colonne avec les ancien genre
)

# On selectionne les 9 genres principaux
data_genre_principale = data_genre_bien.iloc[:9]

# les autres genre seront afficher comme 'autre'
data_autre_genre = data_genre_bien.iloc[9:] 
count_autre = data_autre_genre.sum(numeric_only=True)["count"]
df_autre = pd.DataFrame(
    {"genre_grp": "Other - 188 genders", "count": count_autre}, index=[1]
)  # On crée la ligne "autre" dans un nouveau dataFrame


data_genre_principale = pd.concat(
    [data_genre_principale, df_autre], ignore_index=True
)  # On concatène la nouvelle ligne

# les totaux pour les pourcentage
total_data_autre_genre = data_autre_genre.sum(numeric_only=True)["count"]
total_data_principale_genre = data_genre_principale.sum(numeric_only=True)["count"]

# Fonction de calcule de prct et de cat.
def calcPoucentageAutreGenre(row):
    return (row["count"] / total_data_autre_genre) * 100

def calcPoucentagePrincipaleGenre(row):
    return (row["count"] / total_data_principale_genre) * 100

def categorizeAutreGenre(row):
    if row["count"] > 800:
        return "More than 800 books"
    elif row["count"] >= 100:
        return "Between 800 and 100 books"
    elif row["count"] >= 10:
        return "Between 100 and 10 books"
    elif row["count"] >= 2:
        return "Between 10 and 2 books"
    else:
        return "1 books"


def prctCatAutre(row):
    '''Pour les ratios du bar chart'''
    return row["count"] / 188


# On applique les fonctions
data_autre_genre = pd.concat(
    [data_autre_genre, data_autre_genre.apply(calcPoucentageAutreGenre, axis=1)], axis=1
).rename(columns={0: "pourcentage"})

data_principale_pourcentage = data_genre_principale.apply(
    calcPoucentagePrincipaleGenre, axis=1
)
data_autre_genre = pd.concat(
    [data_autre_genre, data_autre_genre.apply(categorizeAutreGenre, axis=1)], axis=1
).rename(columns={0: "cat"})
# Pour le bar chart
distrib_autre_genre = data_autre_genre.groupby("cat").count().reset_index()

# On créer les labels
labels = data_genre_principale["genre_grp"]
labels = labels.to_list()
data_principale_pourcentage = data_principale_pourcentage.to_list()
tmp_labels = []
for i in range(len(labels)):
    prct = data_principale_pourcentage[i]
    tmp_labels.append(labels[i] + " - " + str(round(prct, 4)) + "%")

labels = tmp_labels

labels_autre = distrib_autre_genre["cat"].drop_duplicates()


# Below code is copied and adapted from https://matplotlib.org/stable/gallery/pie_and_polar_charts/bar_of_pie.html
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(192, 108))

explode = ([0] * 9) + [0.1]
wedges, texts, autotexts = ax1.pie(
    data_genre_principale["count"].to_numpy(),
    startangle=90,
    autopct="%1.2f%%",
    radius=1,
    explode=explode,
    pctdistance=0.8
)

ax1.legend(
    wedges,
    labels,
    title="Gender",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
)

plt.setp(texts, size=11)

ax1.set_title("Principal genders pie chart")

# bar chart parameters
genre_ratios = distrib_autre_genre.apply(prctCatAutre, axis=1).to_list()
bottom = 1
width = 0.2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(genre_ratios, labels_autre)])):
    bottom -= height
    bc = ax2.bar(
        0, height, width, bottom=bottom, color="C0", label=label, alpha=0.1 + 0.20 * j
    )
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type="center")

ax2.set_title("Other Gender repartition by number of books")
ax2.legend()
ax2.axis("off")
ax2.set_xlim(-2.5 * width, 2.5 * width)

# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[-1].theta1, wedges[-1].theta2
center, r = wedges[-1].center, wedges[-1].r
bar_height = 1

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(
    xyA=(-width / 2, bar_height),
    coordsA=ax2.transData,
    xyB=(x, y),
    coordsB=ax1.transData,
)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(
    xyA=(-width / 2, 0), coordsA=ax2.transData, xyB=(x, y), coordsB=ax1.transData
)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

# Afficher en plein ecran pour + de lisibilité
# manager = plt.get_current_fig_manager()
# manager.full_screen_toggle()    
plt.show()
