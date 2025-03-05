# Utiliser l'image officielle PostgreSQL
FROM postgres:latest

# Variables d'environnement pour configurer PostgreSQL
ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=root
ENV POSTGRES_DB=masterbook


# Copier vos fichiers CSV et les scripts SQL
COPY csv/ /docker-entrypoint-initdb.d/csv/

# Ajouter les permissions nécessaires
RUN chmod -R 755 /docker-entrypoint-initdb.d/
RUN chmod -R 755 /docker-entrypoint-initdb.d/csv/


COPY script_creation_masterbook_bdd.sql /docker-entrypoint-initdb.d/01_script_creation_masterbook_bdd.sql
COPY insertion_dans_bdd.sql /docker-entrypoint-initdb.d/02_insertion_dans_bdd.sql
COPY script_insertion_formulaire.sql /docker-entrypoint-initdb.d/03_insertion_formulaire.sql









