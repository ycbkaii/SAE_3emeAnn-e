import pandas as pd
import re
import unicodedata
import os

# Vérifier si le dossier 'csv' existe, sinon le créer
# if not os.path.exists("csv"):
#     os.makedirs("csv")

# Chargement du fichier CSV d'origine
raw_csv = pd.read_csv("../csv/bigboss_book.csv")

# Extraire uniquement les colonnes "id" et "awards"
data_extract = raw_csv[["id", "awards"]].dropna()  # On supprime les lignes sans données dans "awards"

# Fonction pour nettoyer et décoder les textes encodés
def decode_text(text):
    try:
        decoded_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
        return decoded_text
    except UnicodeDecodeError:
        return text

# Fonction pour extraire les noms des prix, les années et l'id du livre
def split_awards(row):
    awards = row['awards'].split(', ')
    df_list = []
    for award in awards:
        award_name_year = re.findall(r'(.+?)\((\d{4})\)', decode_text(award))
        if award_name_year:
            for match in award_name_year:
                award_name = match[0].strip().replace('for', '').strip()
                award_year = match[1]
                # Vérification que l'année est bien un nombre à 4 chiffres
                if award_year.isdigit():
                    df_list.append({'id_livre': row['id'], 'nom_awards': award_name, 'date': award_year})
                else:
                    print(f"Année non valide trouvée : {award_year} dans l'entrée : {award}")
    return pd.DataFrame(df_list)

# Appliquer la fonction et concaténer les résultats
awards_data = pd.concat([split_awards(row) for index, row in data_extract.iterrows()], ignore_index=True)

# Créer un dataframe pour "awards" avec des prix uniques et des IDs
awards_unique = awards_data[['nom_awards']].drop_duplicates().reset_index(drop=True)
awards_unique['id_award'] = awards_unique.index + 1  # Générer un id_award unique

# Créer le dataframe "recompense_en" avec id_livre, id_award et date (année uniquement)
recompense_en = awards_data.merge(awards_unique, on='nom_awards')[['id_livre', 'id_award', 'date']]


# On rajoute 01-01 à l'année
def rajout0101(row) :
    return row+"-01-01"

recompense_en['date'] = recompense_en['date'].apply(rajout0101)

awards_unique[['id_award', 'nom_awards']].to_csv("awards.csv", index=False)
recompense_en.drop_duplicates().to_csv("peuplement_recompense_en.csv", index=False)

print("Les fichiers awards.csv et recompense_en.csv ont été générés avec succès.")