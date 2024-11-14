import re
import pandas as pd

data_extract = pd.read_csv("../csv/bigboss_book.csv")

raw_csv = ['id', 'series']
data_extract = data_extract[raw_csv]

# Fonction pour extraire le nom de la saga et le numéro
def extract_saga_info(text):
    # Vérifiez d'abord si l'entrée est bien une chaîne de caractères
    if isinstance(text, str):
        # Recherche d'une correspondance avec le format "(Nom de la saga #numéro)"
        match = re.search(r'\(([^)]+)#(\d+)\)', text)
        if match:
            saga_name = match.group(1)  # Nom de la saga
            saga_number = match.group(2)  # Numéro de la saga
            return saga_name, int(saga_number)
    # Si l'entrée n'est pas une chaîne ou n'a pas de correspondance, renvoyer None
    return None, None

# Appliquer la fonction à chaque ligne du DataFrame
data_extract[['saga_name', 'saga_number']] = data_extract['series'].apply(lambda x: pd.Series(extract_saga_info(x)))

# Export en CSV
data_extract[['id', 'saga_name']].to_csv("peuplement_serie.csv",header=True, index=False)