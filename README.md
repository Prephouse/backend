# Prephouse Backend

## Development Setup
1. Download and install [Python 3.10](https://www.python.org/downloads/release/python-3100/)
2. Open a tab, in the root directory of this project, on your command line interface (CLI)
3. Run `./setup.sh` on your CLI to install dependencies and tools through homebrew, and to build the docker image
4. Run `docker-compose up` on your CLI to start the local database session and local development server
5. Run `python3` on your CLI to open the Python REPL
6. Run the following code on the Python REPL to create the schema on your local database
   ```python-repl
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

## Server Startup
1. Run `docker-compose up` on your CLI to start the local database session and local development server
2. Navigate to localhost:5000 on your web browser

## Code Style
We're following the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide.
