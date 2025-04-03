---------------------------------------------------------------------------
--                        Utilisateur du formulaire                      --
---------------------------------------------------------------------------
SET SCHEMA 'masterbook';

-- On import 'id_vitesse_lecture' et 'nom_categorie' pour la vitesse de lecture
INSERT INTO _vitesse_de_lecture (id_vitesse_lecture, nom_categorie) VALUES
(1, '1 a 2 semaines'),
(2, 'entre 3 jours et une semaines'),
(3, 'je ne le lis pas'),
(4, '2-3 jour ou moins'),
(5, '1 mois ou +');

-- On import 'id_selecton' et 'nom_humeur' pour la selection de l'humeur
INSERT INTO _mood_selection (id_selection, nom_humeur) VALUES
(1, 'moyen'),
(2, 'content'),
(3, 'fache'),
(4, 'j''adore lire'),
(5, 'nonrenseigne');

-- On import 'id_genre' et 'nom_genre' pour le genre de la personne
INSERT INTO masterbook."_genre_personne" (id_genre, nom_genre) VALUES
(2, 'autre');

-- On import 'id_secteur' et 'nom_secteur' pour le secteur de travail
COPY masterbook._secteur_de_travail(id_secteur, nom_secteur)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_secteur.csv'
DELIMITER ','
CSV HEADER;

-- On import 'id_preference' et 'preference' pour les preferences de lecture
COPY masterbook._preference_lecture(id_preference, preference)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_prefere_lire.csv'
DELIMITER ','
CSV HEADER;

-- On importe 'id_vitesse_lecture' et 'vitesse_lecture' pour les vitesses de lecture
COPY masterbook._utilisateur(id_user, age, id_secteur, id_vitesse_lecture, id_selection, id_genre_sex, id_prefere_lire)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_users.csv'
DELIMITER ','
CSV HEADER;

-- Mettre à jour la séquence pour qu'elle commence après le maximum des ids déjà présents
SELECT setval('masterbook._utilisateur_id_user_seq', (SELECT MAX(id_user) FROM masterbook._utilisateur));

---------------------------------------------------------------------------
--                       Critere de choix de livre                       --
---------------------------------------------------------------------------

-- On importe 'id_critere' et 'critere' pour les criteres de choix de livre
COPY masterbook._critere_pour_choisir_livre(id_critere,critere)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_criteres.csv'
DELIMITER ','
CSV HEADER;

-- On importe 'id_critere' et 'critere' pour les criteres de choix de livre
COPY masterbook._critere_de_utilisateur(id_user,id_critere)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_criteres_user.csv'
DELIMITER ','
CSV HEADER;


---------------------------------------------------------------------------
--                       Lieux de lecture                                --
---------------------------------------------------------------------------

-- On importe 'id_lieux' et 'nom_lieux' pour les lieux de lectures
COPY masterbook._lieux_lecture(id_lieux, nom_lieux)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_lieux_lecture.csv'
DELIMITER ','
CSV HEADER;

-- On importe 'id_user' et 'id_lieux' pour les lieux de lectures
COPY masterbook._ou_utilisateur_lit_generalement(id_user, id_lieux)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_lieux_user.csv'
DELIMITER ','
CSV HEADER;

---------------------------------------------------------------------------
--                       Decouverte de livre                             --
---------------------------------------------------------------------------


-- On importe 'id_decouverte' et 'decouverte' pour les decouvertes de livre
COPY masterbook._decouverte_livre(id_decouverte, decouverte)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_decouverte_livre.csv'
DELIMITER ','
CSV HEADER;

-- On importe 'id_user' et 'id_decouverte' pour les decouvertes de livre
COPY masterbook._a_decouvert_livre(id_user, id_decouverte)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_decouverte_livre_user.csv'
DELIMITER ','
CSV HEADER;

---------------------------------------------------------------------------
--                              Raisons de lecture                       --
---------------------------------------------------------------------------

-- On importe 'id_raison_lecture' et 'categorie' pour les raisons de lecture
COPY masterbook._categories_raison_lecture(id_raison_lecture, categorie)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_raisons.csv'
DELIMITER ','
CSV HEADER;

-- On importe 'id_user' et 'id_raison_lecture' pour les raisons de lecture
COPY masterbook._utilisateur_raison(id_user, id_raison_lecture)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_raisons_user.csv'
DELIMITER ','
CSV HEADER;


---------------------------------------------------------------------------
--                            User et auteur                             --
---------------------------------------------------------------------------

-- On importe 'id_genre' et 'nom_genre' pour les genres
COPY masterbook._genre(id_genre, nom_genre)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_updated_genre.csv'
DELIMITER ','
CSV HEADER;

-- On importe 'id_auteur' et 'nom_complet' pour les auteurs
COPY masterbook._auteur(id_auteur, nom_complet, id_genre_sex)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_updated_auteur.csv'
DELIMITER ','
CSV HEADER;


---------------------------------------------------------------------------
--                            Aime genre                                 --
---------------------------------------------------------------------------

-- On importe 'id_genre' et 'nom_genre' pour les genres que l'utilisateur aime
COPY masterbook._genre_aime(id_user, id_genre)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_genres_user.csv'
DELIMITER ','
CSV HEADER;


---------------------------------------------------------------------------
--                            Aime auteur                                --
---------------------------------------------------------------------------

-- On importe 'id_auteur' et 'nom_complet' pour les auteurs que l'utilisateur aime
COPY masterbook._aime_auteur(id_user, id_auteur)
FROM '/docker-entrypoint-initdb.d/csv/formulaire/peuplement_formulaire_users_auteurs.csv'
DELIMITER ','
CSV HEADER;



---------------------------------------------------------------------------
--                            a lu livre                                 --
---------------------------------------------------------------------------

INSERT INTO masterbook."_a_lu_livre_vote_genre_pour_livre"
(id_user, id_genre, id_livre, note_livre, review)
VALUES(5, 0, 630104, 5, '');
