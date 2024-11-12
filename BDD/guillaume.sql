SET SCHEMA 'masterbook';

-- On drop les tables pour être sur qie cela mets bien à jour

-- Table Livre
CREATE TABLE "_livre" (
	"id_livre" serial NOT NULL UNIQUE,
	"title" varchar(255) NOT NULL,
	"description" varchar(255),
	"number_of_page" int,
	"date_published" date NOT NULL,
	"isbn" varchar(10) NOT NULL UNIQUE,
	"id_saga" int DEFAULT NULL,
	"numéro_opus" int DEFAULT NULL,
	PRIMARY KEY("id")
);


-- Table Genre
CREATE TABLE "_genre" (
	"id_genre" serial NOT NULL UNIQUE,
	"nom_genre" varchar(255),
	PRIMARY KEY("id_genre")
);

-- Table Personnage
CREATE TABLE "_personnage" (
	"id_personnage" serial NOT NULL UNIQUE,
	"Nom_personnage" varchar(100),
	PRIMARY KEY("id_personnage")
);

-- Table Possede_personnage
CREATE TABLE "_possede_personnage" (
	"id_books" int NOT NULL UNIQUE,
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
	"id_publisher" int NOT NULL UNIQUE,
	"id_book" int NOT NULL,
	PRIMARY KEY("id_publisher", "id_book")
);

-- Table Genre_du_livre
CREATE TABLE "_genres_du_livre" (
	"id_genre" int NOT NULL UNIQUE,
	"nombre_votes_utilisateur" int,
	"id_livre" int NOT NULL UNIQUE,
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

------------------------------------------
-- Vue pour les valeurs calculées 
------------------------------------------

CREATE VIEW "rating_livres" AS
SELECT id_livre, AVG(note_livre) as average_rating, COUNT(note_livre) as rating_count
FROM a_lu_livre_vote_genre_pour_livre
GROUP BY id_livre
WHERE note_livre IS NOT NULL
;

CREATE VIEW "review_livres" AS
SELECT id_livre, COUNT(review) as review_count
FROM a_lu_livre_vote_genre_pour_livre
GROUP BY id_livre
WHERE review IS NOT NULL
;

CREATE VIEW "livres_calculees" AS
SELECT review_livres.id_livre, average_rating, rating_count, review_count
FROM review_livres
NATURAL JOIN rating_livres;