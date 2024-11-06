DROP SCHEMA IF EXISTS masterbook CASCADE; 
CREATE SCHEMA masterbook;
SET SCHEMA 'masterbook';

-- Création de table 'genre_personne'
CREATE TABLE genre_personne(
    id_genre SERIAL PRIMARY KEY,
    nom_genre VARCHAR
);


-- Création de lieu de naissance
CREATE TABLE lieu_de_naissance(
    id_lieu SERIAL PRIMARY KEY,
    lieu VARCHAR
);


-- Création de la table 'auteur'
CREATE TABLE auteur(
    id_auteur SERIAL PRIMARY KEY,
    nom_complet VARCHAR,
    id_genre INT,
    lieu_naissance INT,
    FOREIGN KEY (id_genre) REFERENCES genre_personne(id_genre) ON DELETE CASCADE,
    FOREIGN KEY (lieu_naissance) REFERENCES lieu_de_naissance(id_lieu) ON DELETE CASCADE 
);






-- Création de la table de relation 'a_lu_auteur' entre la table 'Auteur' et 'Utilisateur'
CREATE TABLE a_lu_auteur(
    id_auteur INT,
    id_user INT,
    note_auteur INT DEFAULT NULL CHECK ((note_auteur >= 1 AND note_auteur <=5) OR note_auteur = NULL),
    review VARCHAR DEFAULT NULL,
    PRIMARY KEY(id_auteur, id_user),
    FOREIGN KEY (id_auteur) REFERENCES auteur(id_auteur) ,
    FOREIGN KEY (id_user) REFERENCES utilisateur(id_user)
);



-- Création d'une vue des valeurs calculées de la table 'Auteur'

-- Création vue pour le 'rating' pour auteur
CREATE VIEW rating_auteur AS
SELECT id_auteur, AVG(note_auteur) AS average_rating, COUNT(note_auteur) AS rating_count 
FROM a_lu_auteur
GROUP BY id_auteur
WHERE note_auteur IS NOT NULL
;
-- Création vue pour le 'review' pour auteur
CREATE VIEW review_auteur AS
SELECT id_auteur, COUNT(review) AS review_count
FROM a_lu_auteur
GROUP BY id_auteur
WHERE review IS NOT NULL;


CREATE VIEW auteur_calculees AS 
SELECT review_auteur.id_auteur, average_rating, rating_count, review_count FROM review_auteur 
NATURAL JOIN rating_auteur
;


