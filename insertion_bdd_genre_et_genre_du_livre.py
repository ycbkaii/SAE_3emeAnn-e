import pandas as pd

raw_csv = pd.read_csv("csv/bigboss_book.csv")

data_extract = raw_csv[["id","genre_and_votes"]]

# On drop les livres ou ya pas de genres
data_extract = data_extract.dropna()

# Function to split genre and votes
def split_genres(row):
    genres = row['genre_and_votes'].split(', ')
    df_list = []
    for genre in genres:
        parts = genre.split()
        new_id = row['id']
        new_genre = ' '.join(parts[:-1]) 
        new_votes = 1 if parts[-1] == "1user" else int(parts[-1])      # Last element is votes + cas spécifique de 1user
        df_list.append({'id': new_id, 'genre': new_genre, 'votes': new_votes})
    return pd.DataFrame(df_list)

# Apply the function to all rows and concatenate results
genre_du_livre = pd.concat([split_genres(row) for index, row in data_extract.iterrows()], ignore_index=True)

genre = genre_du_livre['genre']

genre_unique = genre.drop_duplicates()

genre_du_livre.to_csv("csv/peuplement_genre_du_livre.csv")
genre_unique.to_csv("csv/peuplement_genre_livre.csv")