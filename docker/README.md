## Prerequisite

- Docker
- 8 GB of RAM


## Start Containers

### First Time
To build and start the containers for the first time, run:
```bash
docker compose up --build
```

### After First Time
To start the containers after it has been built:
```bash
# With log in terminal
docker compose up
# Without log in terminal
docker compose up -d
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
