DROP SCHEMA IF EXISTS masterbook CASCADE; 
CREATE SCHEMA masterbook;
SET SCHEMA 'masterbook';

/**
* @author Yanis
* Mise en place du merge
*/

/**
* @author Yanis
*/
-- Création de table 'genre_personne'
CREATE TABLE _genre_personne(
    id_genre SERIAL PRIMARY KEY,
    nom_genre VARCHAR
);


/**
* @author Timothee
*/
-- Table: Awards
CREATE TABLE _awards (
    id_awards SERIAL PRIMARY KEY,
    nom_awards VARCHAR(255)
);

-- Table: Saga (Series)
CREATE TABLE _saga (
    id_saga SERIAL PRIMARY KEY,
    nom_de_la_saga VARCHAR(255)
);




/**
* @author Guillaume
*/

-- Table Livre
CREATE TABLE "_livre" (
	"id_livre" serial NOT NULL UNIQUE,
	"title" varchar(255) NOT NULL,
	"description" varchar(255),
	"number_of_page" int,
	"date_published" date NOT NULL,
	"isbn" varchar(13) DEFAULT NULL,
	"id_saga" int DEFAULT NULL,
	"numéro_opus" int DEFAULT NULL,
    "review_count_others" int,
    "rating_count_others" int,
    "average_rating_others" float,
    FOREIGN KEY (id_saga) REFERENCES _saga(id_saga),
	PRIMARY KEY("id_livre")
);


-- Table Genre
CREATE TABLE "_genre" (
	"id_genre" serial NOT NULL,
	"nom_genre" varchar(255),
	PRIMARY KEY("id_genre")
);

-- Table Personnage
CREATE TABLE "_personnage" (
	"id_personnage" serial,
	"nom_personnage" varchar(100),
	PRIMARY KEY("id_personnage")
);

-- Table Possede_personnage
CREATE TABLE "_possede_personnage" (
	"id_books" int NOT NULL,
	"id_personnage" int NOT NULL,
	PRIMARY KEY("id_books", "id_personnage")
);

-- Table Publisher
CREATE TABLE "_publisher" (
	"id_publisher" serial NOT NULL UNIQUE,
	PRIMARY KEY("id_publisher")
);

-- Table a_publie
CREATE TABLE "_a_publie" (
	"id_publisher" int NOT NULL,
	"id_book" int NOT NULL,
	PRIMARY KEY("id_publisher", "id_book")
);

-- Table Genre_du_livre
CREATE TABLE "_genres_du_livre" (
	"id_genre" int NOT NULL,
	"nombre_votes_utilisateur" int DEFAULT 0,
	"id_livre" int NOT NULL,
	PRIMARY KEY("id_genre", "id_livre")
);

------------------------------------------
-- Clef étrangère table possede_personnage
------------------------------------------

ALTER TABLE "_possede_personnage"
ADD FOREIGN KEY("id_books") REFERENCES "_livre"("id_livre")
ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "_possede_personnage"
ADD FOREIGN KEY("id_personnage") REFERENCES "_personnage"("id_personnage")
ON UPDATE CASCADE ON DELETE CASCADE;


------------------------------------------
-- Clef étrangère table a_publie
------------------------------------------

ALTER TABLE "_a_publie"
ADD FOREIGN KEY("id_publisher") REFERENCES "_publisher"("id_publisher")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "_a_publie"
ADD FOREIGN KEY("id_book") REFERENCES "_livre"("id_livre")
ON UPDATE CASCADE ON DELETE CASCADE;

------------------------------------------
-- Clef étrangère table genres_du_livre
------------------------------------------

ALTER TABLE "_genres_du_livre"
ADD FOREIGN KEY("id_genre") REFERENCES "_genre"("id_genre")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "_genres_du_livre"
ADD FOREIGN KEY("id_livre") REFERENCES "_livre"("id_livre")
ON UPDATE CASCADE ON DELETE CASCADE;




/**
* @author Timothee
*/
-- Table: recompense_en (livre qui a gagné un award)
CREATE TABLE _recompense_en (
    id_livre INT,
    id_awards INT,
    date DATE,
    PRIMARY KEY (id_livre, id_awards, date),
    FOREIGN KEY (id_livre) REFERENCES _livre(id_livre),
    FOREIGN KEY (id_awards) REFERENCES _awards(id_awards)
);

/**
* @author Yoann
*/
-- Création des tables en rapport à utilisateur
CREATE TABLE _vitesse_de_lecture (
    id_vitesse_lecture SERIAL PRIMARY KEY,
    nom_categorie VARCHAR(50) NOT NULL
);

CREATE TABLE _critere_pour_choisir_livre (
    id_critere SERIAL PRIMARY KEY,
    critere VARCHAR(50) NOT NULL
);

CREATE TABLE _secteur_de_travail (
    id_secteur SERIAL PRIMARY KEY,
    nom_secteur VARCHAR(50) NOT NULL
);

CREATE TABLE _lieux_lecture (
    id_lieux SERIAL PRIMARY KEY,
    nom_lieux VARCHAR(50) NOT NULL
);


/**
*@author Noah
*/

-- Table _mood_selection
CREATE TABLE _mood_selection (
    id_selection SERIAL PRIMARY KEY,
    nom_humeur VARCHAR,
    date_selection TIMESTAMP DEFAULT NOW()
);

-- Création table utilisateur 
CREATE TABLE _utilisateur(
    id_user SERIAL PRIMARY KEY,
    age INT,
    id_selection INT NOT NULL,
    id_vitesse_lecture INT NOT NULL,
    id_secteur INT DEFAULT NULL,
    id_genre_sex INT NOT NULL,
    FOREIGN KEY(id_genre_sex) REFERENCES _genre_personne(id_genre),
    FOREIGN KEY (id_secteur) REFERENCES _secteur_de_travail(id_secteur),
    FOREIGN KEY (id_selection) REFERENCES _mood_selection(id_selection),
    FOREIGN KEY (id_vitesse_lecture) REFERENCES _vitesse_de_lecture(id_vitesse_lecture)
);


-- Table pour la création de _genre_aime entre _genre et _utilisateur
CREATE TABLE _genre_aime(
    id_user INT,
    id_genre INT,
    PRIMARY KEY (id_user, id_genre),
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user),
    FOREIGN KEY (id_genre) REFERENCES _genre(id_genre)
);


-- Table _categories_raison_lecture
CREATE TABLE _categories_raison_lecture(
    id_raison_lecture SERIAL PRIMARY KEY,
    categorie VARCHAR
);

-- Table liaison _utilisateur_raison entre _categories_raison_lecture et utilisateur
CREATE TABLE _utilisateur_raison (
    id_user INT,
    id_raison_lecture INT,
    FOREIGN KEY (id_raison_lecture) REFERENCES _categories_raison_lecture(id_raison_lecture) ON DELETE CASCADE,
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user) ON DELETE CASCADE,
    PRIMARY KEY (id_user, id_raison_lecture)
);



-- Vue pour compter les sélections par _mood_selection
CREATE VIEW _humeur_avec_lecture AS
SELECT
    nom_humeur,
    COUNT(nom_humeur) AS count_mood_selected
FROM
    _mood_selection
NATURAL JOIN 
_utilisateur
WHERE _utilisateur.id_selection IS NOT NULL
GROUP BY nom_humeur;


-- Liaison tertiaire avec _utilisateur, genre_livre et _livre
CREATE TABLE _a_lu_livre_vote_genre_pour_livre (
    id_user INT,
    id_genre INT,
    id_livre INT,
    note_livre INT CHECK((note_livre BETWEEN 1 AND 5) OR note_livre IS NULL) DEFAULT NULL,
    review VARCHAR DEFAULT NULL, 
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user),
    FOREIGN KEY (id_genre) REFERENCES _genre(id_genre),
    FOREIGN KEY (id_livre) REFERENCES _livre(id_livre),
    CONSTRAINT unique_a_lu_livre_vote_genre_pour_livre PRIMARY KEY (id_user, id_livre, id_genre)
);





/**
*@author Yoann
*/
-- Table liaison entre 'lieux_lecture' et 'auteur'
CREATE TABLE _ou_utilisateur_lit_generalement (
    id_lieux INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id_lieux, id_user),
    FOREIGN KEY (id_lieux) REFERENCES _lieux_lecture(id_lieux),
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user)
);

-- Table liaison entre 'user' et 'critere_pour_choisir_un_livre'
CREATE TABLE _critere_de_utilisateur (
    id_critere INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id_critere, id_user),
    FOREIGN KEY (id_critere) REFERENCES _critere_pour_choisir_livre(id_critere),
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user)
);

-- Création de vue pour compter le nombre d'utilisateur qui à choisi 'un lieu'
CREATE VIEW vue_count_lieux_lecture AS
SELECT 
    l.id_lieux,
    l.nom_lieux,
    COUNT(oul.id_user) AS count_lieux_selected
FROM 
    _lieux_lecture AS l
LEFT JOIN 
    _ou_utilisateur_lit_generalement AS oul 
ON 
    l.id_lieux = oul.id_lieux
GROUP BY 
    l.id_lieux, l.nom_lieux
ORDER BY 
    count_lieux_selected DESC;




/**
* @author Yanis
*/


-- Création de lieu de naissance
CREATE TABLE _lieu_de_naissance(
    id_lieu SERIAL PRIMARY KEY,
    lieu VARCHAR
);


-- Création de la table 'auteur'
CREATE TABLE _auteur(
    id_auteur SERIAL PRIMARY KEY,
    nom_complet VARCHAR,
    id_genre_sex INT NOT NULL,
    lieu_naissance INT DEFAULT NULL,
    id_genre_1 INT NOT NULL,
    id_genre_2 INT DEFAULT NULL,
    review_count_others int,
    rating_count_others int,
    average_rating_others float,
    FOREIGN KEY (id_genre_1) REFERENCES _genre(id_genre),
    FOREIGN KEY (id_genre_2) REFERENCES _genre(id_genre),
    FOREIGN KEY (id_genre_sex) REFERENCES _genre_personne(id_genre) ON DELETE CASCADE,
    FOREIGN KEY (lieu_naissance) REFERENCES _lieu_de_naissance(id_lieu) ON DELETE CASCADE 
);



-- Création de table liaison entre livre et auteur
CREATE TABLE _a_ecrit(
    id_auteur INT,
    id_livre INT,
    PRIMARY KEY(id_livre, id_auteur),
    FOREIGN KEY (id_auteur) REFERENCES _auteur(id_auteur),
    FOREIGN KEY (id_livre) REFERENCES _livre(id_livre)
);


-- Création de la table de relation 'a_lu_auteur' entre la table 'Auteur' et 'Utilisateur'
CREATE TABLE _a_lu_auteur(
    id_auteur INT,
    id_user INT,
    note_auteur INT DEFAULT NULL CHECK ((note_auteur >= 1 AND note_auteur <=5) OR note_auteur = NULL),
    review VARCHAR DEFAULT NULL,
    PRIMARY KEY(id_auteur, id_user),
    FOREIGN KEY (id_auteur) REFERENCES _auteur(id_auteur) ,
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user)
);


-- Création d'une table de relation 'aime_auteur' entre auteur et utilisateur
CREATE TABLE _aime_auteur(
    id_user INT,
    id_auteur INT,
    PRIMARY KEY(id_user, id_auteur),
    FOREIGN KEY(id_auteur) REFERENCES _auteur(id_auteur),
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user)
);



-- Création d'une vue des valeurs calculées de la table 'Auteur'

-- Création vue pour le 'rating' pour auteur
CREATE VIEW rating_auteur AS
SELECT id_auteur, AVG(note_auteur) AS average_rating, COUNT(note_auteur) AS rating_count 
FROM _a_lu_auteur
WHERE note_auteur IS NOT NULL
GROUP BY id_auteur
;
-- Création vue pour le 'review' pour auteur
CREATE VIEW review_auteur AS
SELECT id_auteur, COUNT(review) AS review_count
FROM _a_lu_auteur
WHERE review IS NOT NULL
GROUP BY id_auteur
;

CREATE VIEW auteur_calculees AS 
SELECT review_auteur.id_auteur, average_rating, rating_count, review_count FROM review_auteur 
NATURAL JOIN rating_auteur
;

/**
* @author Guillaume
*/
------------------------------------------
-- Vues pour les valeurs calculées entre livre et la table d'association a_lu_livre_vote_genre_pour_livre
------------------------------------------

CREATE VIEW "rating_livres" AS
SELECT id_livre, AVG(note_livre) as average_rating, COUNT(note_livre) as rating_count
FROM _a_lu_livre_vote_genre_pour_livre
WHERE note_livre IS NOT NULL
GROUP BY id_livre
;

CREATE VIEW "review_livres" AS
SELECT id_livre, COUNT(review) as review_count
FROM _a_lu_livre_vote_genre_pour_livre
WHERE review IS NOT NULL
GROUP BY id_livre
;

CREATE VIEW "livres_calculees" AS
SELECT review_livres.id_livre, average_rating, rating_count, review_count
FROM review_livres
NATURAL JOIN rating_livres;


/**
* @author Timothee
*/

--Vue : Pour calculer dynamiquement le nombre de livres dans chaque saga
CREATE VIEW nb_livre_in_saga AS
SELECT id_saga, COUNT(*) AS nb_livre_in_saga
FROM _livre
GROUP BY id_saga;

/**
* @author Yanis
*/


CREATE OR REPLACE FUNCTION _update_nombre_vote()
RETURNS TRIGGER AS $$
DECLARE id_genre_existe INT := NULL;
BEGIN
    IF (NEW.id_genre IS NOT NULL) THEN
        -- On vérifie que 'genre_du_livre' avec id_genre est déjà associé au livre
        SELECT id_genre INTO id_genre_existe FROM _genres_du_livre WHERE id_genre = NEW.id_genre AND id_livre = NEW.id_livre;

        -- S'il n'existe pas on insert un row dans _genres_du_livre
        IF id_genre_existe IS NULL THEN 
            INSERT INTO _genres_du_livre VALUES (NEW.id_genre, 1, NEW.id_livre);
        ELSE
            UPDATE _genres_du_livre SET nombre_votes_utilisateur = nombre_votes_utilisateur+1 WHERE id_genre = id_genre_existe AND id_livre = NEW.id_livre;
        END IF;

    END IF;

    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_nombre_vote_pour_genre_livre
AFTER INSERT ON _a_lu_livre_vote_genre_pour_livre
FOR EACH ROW
EXECUTE FUNCTION _update_nombre_vote();


