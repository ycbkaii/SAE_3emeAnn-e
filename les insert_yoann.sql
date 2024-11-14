INSERT INTO _personnage (id_personnage, nom_personnage)
SELECT DISTINCT id_perso, nom_personnage FROM 'csv/personnages_avec_id_livre.csv';

INSERT INTO _publisher (id_publisher, nom_complet)
SELECT DISTINCT id_publi, nom_complet 
FROM 'csv/publisher_avec_id_livre.csv';


INSERT INTO _possede_personnage (id_book, id_personnage)
SELECT id_book, id_perso
FROM 'csv/personnages_avec_id_livre.csv' 


INSERT INTO _a_publie (id_publisher, id_book)
SELECT id_publi, id_book
FROM 'csv/publisher_avec_id_livre.csv';
