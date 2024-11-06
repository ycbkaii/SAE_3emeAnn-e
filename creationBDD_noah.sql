CREATE TABLE utilisateurs(
    id_user SERIAL PRIMARY KEY,
    age INT,
    nom_humeur VARCHAR REFERENCES humeur(nom_humeur)
);

CREATE TABLE categories_raison_lecture(
    id_raison_lecture SERIAL PRIMARY KEY,
    categorie VARCHAR 
);

CREATE TABLE utilisateur_raison (
    id_user INT REFERENCES utilisateurs(id_user) ON DELETE CASCADE,
    id_raison_lecture INT REFERENCES categories_raison_lecture(id_raison_lecture) ON DELETE CASCADE,
    id_vitesse_lecture INT REFERENCES vitesse_de_lecture(id_vitesse_lecture) ON DELETE CASCADE,
    PRIMARY KEY (id_user, categorie_raison, categorie_vitesse)
);

CREATE TABLE humeur (
    nom_humeur VARCHAR PRIMARY KEY
);

CREATE TABLE mood_selection (
    id_selection SERIAL PRIMARY KEY,
    nom_humeur VARCHAR REFERENCES humeur(nom_humeur),
    id_user INT REFERENCES utilisateurs(id_user),
    date_selection TIMESTAMP DEFAULT NOW()
);

-- Vue pour compter les sélections par humeur
CREATE VIEW humeur_avec_lecture AS
SELECT
    h.nom_humeur,
    COUNT(ms.nom_humeur) AS count_mood_selected
FROM
    humeur h
LEFT JOIN
    mood_selection ms ON h.nom_humeur = ms.nom_humeur
GROUP BY
    h.nom_humeur;


CREATE TABLE a_lu_livre_vote_genre_pour_livre (
    id_vote_avis_livre SERIAL,
    id_user INT REFERENCES utilisateurs(id_user),
    id_genre INT REFERENCES genre_livre(id_genre),
    id_livre INT REFERENCES livre(id_livre),
    note_livre INT CHECK(note_livre BETWEEN 1 AND 5) DEFAULT NULL,
    review VARCHAR DEFAULT NULL, 
    CONSTRAINT unique_a_lu_livre_vote_genre_pour_livre PRIMARY KEY (id_user, id_livre)
);

