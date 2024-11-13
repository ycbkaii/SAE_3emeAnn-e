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

CREATE TABLE _ou_utilisateur_lit_generalement (
    id_lieux INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id_lieux, id_user),
    FOREIGN KEY (id_lieux) REFERENCES _lieux_lecture(id_lieux),
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user)
);

CREATE TABLE _critere_de_utilisateur (
    id_critere INT NOT NULL,
    id_user INT NOT NULL,
    PRIMARY KEY (id_critere, id_user),
    FOREIGN KEY (id_critere) REFERENCES _critere_pour_choisir_livre(id_critere),
    FOREIGN KEY (id_user) REFERENCES _utilisateur(id_user)
);

CREATE VIEW _vue_count_lieux_lecture AS
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
