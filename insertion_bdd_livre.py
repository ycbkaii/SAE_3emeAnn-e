import re
import unicodedata
import pandas as pd
import numpy as np

data_extract = pd.read_csv("../csv/bigboss_book.csv")

raw_csv = ['id', 'title', 'description', 'number_of_pages', 'date_published', 'settings', 'isbn', 'average_rating', 'rating_count', 'review_count', 'five_star_ratings','four_star_ratings','three_star_ratings','two_star_ratings','one_star_ratings', 'series']

data_extract = data_extract[raw_csv]


# Fonction pour extraire le nom de la saga et le numéro
def extract_saga_info(text):
    # Vérifiez d'abord si l'entrée est bien une chaîne de caractères
    if isinstance(text, str):
        # Recherche d'une correspondance avec le format "(Nom de la saga #numéro)"
        match = re.search(r'\(([^)]+)#(\d+)\)', text)
        if match:
            saga_number = match.group(2)  # Numéro de la saga
            return int(saga_number)
    # Si l'entrée n'est pas une chaîne ou n'a pas de correspondance, renvoyer None
    return None

# Appliquer la fonction à chaque ligne du DataFrame
data_extract['saga_number'] = data_extract['series'].apply(lambda x: pd.Series(extract_saga_info(x)))

# def decode_text(text):
#     try:
#         decoded_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
#         return decoded_text
#     except UnicodeDecodeError:
#         return text

# data_extract['title'] = data_extract['title'].apply(decode_text)




# Fonction pour nettoyer et convertir chaque date
def clean_and_convert_date(date_str):
    if isinstance(date_str, str):
        # Si la date est une année uniquement
        if re.match(r'^\d{4}$', date_str):
            return date_str
        
        # Si la date contient un jour avec suffixe ("st", "nd", "rd", "th")
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    
    return date_str  # Retourne la date nettoyée ou inchangée

# Application de la fonction pour retirer les suffixes dans la colonne
data_extract['date_published'] = data_extract['date_published'].apply(lambda x: pd.to_datetime(x, errors='coerce') if not re.match(r'^\d{4}$', str(x)) else x)
data_extract['date_published'] = data_extract['date_published'].apply(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)

# Export en CSV
data_extract[['id', 'title', 'description', 'number_of_pages', 'date_published','saga_number', 'settings', 'isbn', 'average_rating', 'rating_count', 'review_count', 'five_star_ratings','four_star_ratings','three_star_ratings','two_star_ratings','one_star_ratings']].to_csv("peuplement_livre.csv", index=False)

