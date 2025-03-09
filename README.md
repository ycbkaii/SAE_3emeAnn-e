# Comment installer l'api

## Prerequis :

- docker
- python3

Dans le dossier /docker et dans le dossier /bdd_docker, executer la commande :

`docker compose up -d --build`

L'initialisation du système peut prendre plusieurs minutes la premier fois, donc soyez patient

Ensuite dans la raçine (ou il y a index.py) executer les commande :

Uniquement première fois :

  `python -m pip install -r requirements.txt`

`fastapi dev index.py`
