# Prephouse Backend

## Development Setup
1. Download and install [Python 3.10](https://www.python.org/downloads/release/python-3100/)
2. Open a tab, in the root directory of this project, on your command line interface (CLI)
3. Run `./setup.sh` on your CLI to install dependencies and tools through homebrew, and to build the docker image
4. Run `docker-compose up` on your CLI to start the local database session and local development server
5. Run `docker exec -it backend_prephouse_1 bash` in a **separate** tab on your CLI to execute a bash shell in the Docker container
6. Run `python3 create_schema.py` on the bash shell to create the schema on your local database

## Server Startup
1. Run `docker-compose up` on your CLI to start the local database session and local development server
2. Navigate to localhost:5000 on your web browser

## Code Style
We're following the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.
