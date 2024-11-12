import pandas as pd

raw_csv = pd.read_csv("csv/bigboss_book.csv")

data_extract = raw_csv[["genre_and_votes"]]

# On drop les livres ou ya pas de genres
data_extract = data_extract.dropna()

def split_genres(row):
    genres = row['genre_and_votes'].split(', ')
    df_list = []
    for genre in genres:
        parts = genre.split()
        new_genre = ' '.join(parts[:-1])
        df_list.append({'genre': new_genre})
    return pd.DataFrame(df_list)

# Apply the function to all rows and concatenate results
all_genres = pd.concat([split_genres(row) for index, row in data_extract.iterrows()], ignore_index=True)
all_different_genre = all_genres.drop_duplicates()

# Export en CSV
all_different_genre.to_csv("csv/peuplement_genre_livre.csv",header=False)