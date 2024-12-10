COPY masterbook._genre(id_genre, nom_genre)
FROM 'csv/peuplement_genre_livre.csv'
DELIMITER ','
CSV HEADER;

COPY masterbook._genres_du_livre(id_livre,id_genre,nombre_votes_utilisateur)
FROM 'csv/peuplement_genre_livre.csv'
DELIMITER ','
CSV HEADER;