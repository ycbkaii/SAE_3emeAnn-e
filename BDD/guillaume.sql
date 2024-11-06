SET SCHEMA 'masterbook';

-- Table Livre
CREATE TABLE "Livre" (
	"id" serial NOT NULL UNIQUE,
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
CREATE TABLE "genres" (
	"id_genre" serial NOT NULL UNIQUE,
	"nom_genre" varchar(255),
	PRIMARY KEY("id_genre")
);

-- Table Personnage
CREATE TABLE "Personnage" (
	"id_personnage" serial NOT NULL UNIQUE,
	"Nom_personnage" varchar(100),
	PRIMARY KEY("id_personnage")
);

-- Table Possede_personnage
CREATE TABLE "possede_personnage" (
	"id_books" int NOT NULL UNIQUE,
	"id_personnage" int NOT NULL,
	PRIMARY KEY("id_books", "id_personnage")
);

-- Table Publisher
CREATE TABLE "Publisher" (
	"id_publisher" serial NOT NULL UNIQUE,
	PRIMARY KEY("id_publisher")
);

-- Table a_publie
CREATE TABLE "a_publie" (
	"id_publisher" int NOT NULL UNIQUE,
	"id_book" int NOT NULL,
	PRIMARY KEY("id_publisher", "id_book")
);

-- Table Genre_du_livre
CREATE TABLE "genres_du_livre" (
	"id_genre" int NOT NULL UNIQUE,
	"nombre_votes_utilisateur" int,
	"id_livre" int NOT NULL UNIQUE,
	PRIMARY KEY("id_genre", "id_livre")
);

------------------------------------------
-- Clef étrangère table possede_personnage
------------------------------------------

ALTER TABLE "possede_personnage"
ADD FOREIGN KEY("id_books") REFERENCES "Livre"("id")
ON UPDATE CASCADE ON DELETE NO ACTION;

ALTER TABLE "possede_personnage"
ADD FOREIGN KEY("id_personnage") REFERENCES "Personnage"("id_personnage")
ON UPDATE CASCADE ON DELETE CASCADE;


------------------------------------------
-- Clef étrangère table a_publie
------------------------------------------

ALTER TABLE "a_publie"
ADD FOREIGN KEY("id_publisher") REFERENCES "Publisher"("id_publisher")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "a_publie"
ADD FOREIGN KEY("id_book") REFERENCES "Livre"("id")
ON UPDATE CASCADE ON DELETE CASCADE;

------------------------------------------
-- Clef étrangère table genres_du_livre
------------------------------------------

ALTER TABLE "genres_du_livre"
ADD FOREIGN KEY("id_genre") REFERENCES "genres"("id_genre")
ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "genres_du_livre"
ADD FOREIGN KEY("id_livre") REFERENCES "Livre"("id")
ON UPDATE CASCADE ON DELETE CASCADE;
