# Prephouse Backend (ph-backend)

## Setup Instructions

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop) and
[Docker Compose](https://docs.docker.com/compose/install/)
2. Run Docker Desktop on your machine
3. Run `./setup.sh` on your command line interface (CLI)

## Startup Instructions

1. Run Docker Desktop on your machine
2. Run `docker-compose up` on your CLI to start the local database session and local development server
3. Navigate to [localhost:3001](http://localhost:3001) on your web browser

## Code Style

We are following the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide. A pre-commit hook
has been set up to ensure that the codebase conforms to that guide.

## Documentation

We use the restructuredText format (see [PEP287](https://www.python.org/dev/peps/pep-0287/)) for writing
docstrings in Python functions, classes, modules and so on. If you use VSCode, no further action should be required
since restructuredText is set as the default docstring format. If you use PyCharm, go to Tools > Python Integrated Tools
in the IDE preferences and select restructuredText as the docstring format.
