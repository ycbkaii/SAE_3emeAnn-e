# Docker Database Container Management

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

