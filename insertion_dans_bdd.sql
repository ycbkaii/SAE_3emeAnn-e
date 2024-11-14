






-- -- Insert pour livre


-- INSERT INTO _possede_personnage (id_book, id_personnage)
-- SELECT id_book, id_perso
-- FROM 'csv/personnages_avec_id_livre.csv' 


-- INSERT INTO _a_publie (id_publisher, id_book)
-- SELECT id_publi, id_book
-- FROM 'csv/publisher_avec_id_livre.csv';


-- @author Yanis Chiouar
-- @description Mise en place de map les data dans la BDD

-- On créé une table temporaire pour stocker les datas
CREATE TABLE temp_import_perso (
    colonne1 VARCHAR,
    colonne2 VARCHAR,
    colonne3 VARCHAR
);


CREATE TABLE temp_import_publisher (
    colonne1 VARCHAR,
    colonne2 VARCHAR,
    colonne3 VARCHAR
);


CREATE TABLE temp_import_saga (
    colonne1 VARCHAR,
    colonne2 VARCHAR
);

CREATE TABLE temp_import_livre (
    id VARCHAR ,
    title VARCHAR,
    description VARCHAR,
    number_of_pages FLOAT,
    date_published VARCHAR,
    saga_number FLOAT,
    settings VARCHAR,
    isbn VARCHAR(13),
    average_rating VARCHAR,
    rating_count VARCHAR,
    review_count VARCHAR,
    five_star_ratings VARCHAR,
    four_star_ratings VARCHAR,
    three_star_ratings VARCHAR,
    two_star_ratings VARCHAR,
    one_star_ratings VARCHAR
);

CREATE TABLE temp_import_auteur (
    colonne1 VARCHAR,
    colonne2 VARCHAR,
    colonne3 VARCHAR,
    colonne4 VARCHAR,
    colonne5 VARCHAR,
    colonne6 VARCHAR,
    colonne7 VARCHAR
);


-- On importe 'id_perso' et 'nom_perso' pour les personnages
\COPY masterbook.temp_import_perso(colonne1, colonne2, colonne3)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_personnages_avec_id_livre.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._personnage (id_personnage, nom_personnage)
SELECT DISTINCT colonne1::INT, colonne2
FROM masterbook.temp_import_perso;




-- On importe 'id_publi' et 'publisher' pour les publishers
\COPY masterbook.temp_import_publisher(colonne1, colonne2, colonne3)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_publisher_avec_id_livre.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._publisher (id_publisher, nom_complet)
SELECT DISTINCT colonne1::INT, colonne2
FROM masterbook.temp_import_publisher;





-- Insertion 'genres'
\COPY masterbook._genre(id_genre, nom_genre)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_genre_livre.csv'
DELIMITER ','
CSV HEADER;


-- Insertion 'lieux_naissance'
\COPY masterbook._lieu_de_naissance(id_lieu, lieu)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/csv_birth_location.csv'
DELIMITER ','
CSV HEADER;

-- Insertion 'genre_personne'
\COPY masterbook._genre_personne(id_genre, nom_genre)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/csv_genders_person.csv'
DELIMITER ','
CSV HEADER;


-- Insertion 'awards'
\COPY masterbook._awards(id_awards, nom_awards)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/awards.csv'
DELIMITER ','
CSV HEADER;



-- Insertion des saga/series
\COPY masterbook.temp_import_saga(colonne1, colonne2)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_serie.csv'
DELIMITER ','
CSV HEADER;

INSERT INTO masterbook._saga (nom_de_la_saga)
SELECT DISTINCT colonne2
FROM masterbook.temp_import_saga WHERE colonne2 IS NOT NULL;




-- Insertion livre
\COPY masterbook.temp_import_livre
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_livre.csv'
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
\COPY masterbook.temp_import_auteur
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_auteurs.csv'
DELIMITER ','
CSV HEADER;


INSERT INTO masterbook._auteur
SELECT DISTINCT colonne1::INT, colonne2, colonne3::INT, REPLACE(colonne4,'.0','')::INT, colonne5::INT, colonne6::INT, REPLACE(colonne7,',','.')::FLOAT
FROM masterbook.temp_import_auteur;
















\COPY masterbook._genres_du_livre(id_livre,id_genre,nombre_votes_utilisateur)
FROM '/home/bkaii/Documents/COURS_PORTATIFS/S5/SAE/scripts_insertions/peuplement_genre_du_livre.csv'
DELIMITER ','
CSV HEADER;


