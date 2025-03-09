# Docker Container Management

## Start Container

### First Time
To build and start the container for the first time, run:
```bash
docker compose up --build
```

### After First Time
To start the container after it has been built:
```bash
docker compose up
```

## Stop Container
To stop the running container:
```bash
docker compose down
```

### Clear Volume and Drop Database
To stop the container, clear all volumes, and drop the database:
```bash
docker compose down -v
```

## Access Docker Bash Terminal
To access the bash terminal in the `postgres-local` container:
```bash
docker exec -ti postgres-local bash
```

## Manage the Database

### Launch SQL Script
To execute a SQL script in the `masterbook` database:
```bash
psql -U root -d masterbook -f script_insertion_formulaire.sql
```

### Connect to the `masterbook` Database
To connect to the `masterbook` database:
```bash
psql -U root -d masterbook
```

