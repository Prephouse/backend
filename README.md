# Prephouse Backend

## Development Setup

1. Download and install the [Docker Desktop](https://www.docker.com/products/docker-desktop) and
[Docker Compose](https://docs.docker.com/compose/install/)
2. Make sure Docker is running
3. Go to the root directory of this project on your command line interface (CLI)
4. Run `./setup.sh` on your CLI

## Development Startup

1. Make sure Docker is running
2. Run `docker-compose up` on your CLI to start the local database session and local development server
3. Navigate to [localhost:3001](http://localhost:3001) on your web browser

## Code Style

We are following the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide. A pre-commit hook
has been set up to ensure that the codebase conforms to that guide.
