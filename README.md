# Prephouse Backend

## Development Setup
1. Download and install the following software
   - [Python 3.10](https://www.python.org/downloads/release/python-3100/)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [Docker Compose](https://docs.docker.com/compose/install/)
2. Make sure Docker is running
3. Open a tab, in the root directory of this project, on your command line interface (CLI)
4. Run `./setup.sh` on your CLI
5. Run `docker-compose up --build` on your CLI to build and start the local database session and local development server
6. Run `docker exec -it backend-prephouse-1 python3 create_schema.py` in a **separate** tab on your CLI

## Server Startup
1. Make sure Docker is running
2. Run `docker-compose up` on your CLI to start the local database session and local development server
3. Navigate to [localhost:3001](http://localhost:3001) on your web browser

## Code Style
We're following the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.
