SET SCHEMA 'masterbook';


-- @author Yanis Chiouar
-- @description Mise en place de map les data dans la BDD


-- On importe 'id_perso' et 'nom_perso' pour les personnages
COPY masterbook.temp_import_perso(colonne1, colonne2, colonne3)
FROM '/docker-entrypoint-initdb.d/csv/peuplement_personnages_avec_id_livre.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._personnage (id_personnage, nom_personnage)
SELECT DISTINCT colonne1::INT, colonne2
FROM masterbook.temp_import_perso;




-- On importe 'id_publi' et 'publisher' pour les publishers
COPY masterbook.temp_import_publisher(colonne1, colonne2, colonne3)
FROM '/docker-entrypoint-initdb.d/csv/peuplement_publisher_avec_id_livre.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._publisher (id_publisher, nom_complet)
SELECT DISTINCT colonne1::INT, colonne2
FROM masterbook.temp_import_publisher;



-- Insertion 'genres'
COPY masterbook._genre(id_genre, nom_genre)
FROM '/docker-entrypoint-initdb.d/csv/peuplement_genre_livre.csv'
DELIMITER ','
CSV HEADER;


-- Insertion 'lieux_naissance'
COPY masterbook._lieu_de_naissance(id_lieu, lieu)
FROM '/docker-entrypoint-initdb.d/csv/csv_birth_location.csv'
DELIMITER ','
CSV HEADER;

-- Insertion 'genre_personne'
COPY masterbook._genre_personne(id_genre, nom_genre)
FROM '/docker-entrypoint-initdb.d/csv/csv_genders_person.csv'
DELIMITER ','
CSV HEADER;


-- Insertion 'awards'
COPY masterbook._awards(id_awards, nom_awards)
FROM '/docker-entrypoint-initdb.d/csv/awards.csv'
DELIMITER ','
CSV HEADER;



-- Insertion des saga/series
COPY masterbook.temp_import_saga(colonne1, colonne2)
FROM '/docker-entrypoint-initdb.d/csv/peuplement_serie.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._saga (nom_de_la_saga)
SELECT DISTINCT colonne2
FROM masterbook.temp_import_saga WHERE colonne2 IS NOT NULL;


-- Insertion livre
COPY masterbook.temp_import_livre
FROM '/docker-entrypoint-initdb.d/csv/peuplement_livre.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._livre(
    id_livre,
    title,
    description,
    number_of_page,
    date_published,
    isbn,
    nom_de_la_saga,
    numéro_opus,
    review_count,
    rating_count,
    average_rating,
    five_star_ratings,
    four_star_ratings,
    three_star_ratings,
    two_star_ratings,
    one_star_ratings)
SELECT DISTINCT 
id::INT, 
title, 
description, 
number_of_pages::INT,



CASE 
        WHEN date_published LIKE '% %' THEN NULL
        -- Si la longueur est de 4, on suppose que c'est une année seule, donc on la conserve telle quelle
        WHEN LENGTH(TRIM(date_published)) = 4 OR LENGTH(TRIM(date_published)) = 5 THEN TO_DATE(date_published,'YYYY')

        WHEN LENGTH(TRIM(date_published)) = 3 THEN TO_DATE(date_published,'YYY')

        WHEN LENGTH(TRIM(date_published)) = 2 THEN TO_DATE(date_published,'YY')

        WHEN LENGTH(TRIM(date_published)) = 1 THEN TO_DATE(date_published,'Y')

        -- Si c'est une date complète ou un format "Month YYYY", on extrait les 4 derniers caractères comme année
        WHEN date_published IS NOT NULL AND date_published != '' THEN date_published::DATE
        
        
        ELSE NULL
END AS dateformatee,


isbn,
colonne2,
saga_number::INT,
review_count::INT,
rating_count::INT,
REPLACE(average_rating, ',', '.')::FLOAT,
five_star_ratings::INT,
four_star_ratings::INT,
three_star_ratings::INT,
two_star_ratings::INT,
one_star_ratings::INT
FROM masterbook.temp_import_livre 
INNER JOIN masterbook.temp_import_saga ON temp_import_saga.colonne1 = temp_import_livre.id;







-- Insertion 'auteur'
COPY masterbook.temp_import_auteur
FROM '/docker-entrypoint-initdb.d/csv/peuplement_auteurs.csv'
DELIMITER ','
CSV HEADER;


INSERT INTO masterbook._auteur
SELECT DISTINCT colonne1::INT, colonne2, colonne3::INT, REPLACE(colonne4,'.0','')::INT, colonne5::INT, colonne6::INT, REPLACE(colonne7,',','.')::FLOAT
FROM masterbook.temp_import_auteur;




-- Insertion genre du livre
COPY masterbook._genres_du_livre(id_livre,id_genre,nombre_votes_utilisateur)
FROM '/docker-entrypoint-initdb.d/csv/peuplement_genre_du_livre.csv'
DELIMITER ','
CSV HEADER;



-- Insertion de possede_personnage
INSERT INTO masterbook._possede_personnage
SELECT colonne3::INT, colonne1::INT
FROM  masterbook.temp_import_perso;

-- Insertion de _a_publie
INSERT INTO masterbook._a_publie
SELECT colonne1::INT, colonne3::INT
FROM masterbook.temp_import_publisher;

-- Insertion _genre_auteurs
COPY masterbook._genres_auteurs
FROM '/docker-entrypoint-initdb.d/csv/peuplement_genre_auteurs.csv'
DELIMITER ','
CSV HEADER;


-- Insertion _recompenser_en
COPY masterbook._recompense_en
FROM '/docker-entrypoint-initdb.d/csv/peuplement_recompense_en.csv'
DELIMITER ','
CSV HEADER;

-- Insertion dans _ecrit_par
COPY masterbook._a_ecrit(id_livre, id_auteur)
FROM '/docker-entrypoint-initdb.d/csv/a_ecrit.csv'
DELIMITER ','
CSV HEADER;
