# Prephouse Backend (ph-backend)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Instructions

### Setup

1. Download and install [Docker Desktop][docker-desktop], [Docker Compose][docker-compose] and
   [pre-commit][pre-commit]
2. Run Docker Desktop on your machine
3. Run `./setup.sh` on your command line interface (CLI)

### Startup

1. Run Docker Desktop on your machine
2. Run `docker-compose up` on your CLI to start the local database session and local development server
3. Navigate to <http://localhost:3001> on your web browser

### Development

- Add any required external Python packages to [requirements.txt](requirements.txt) or, for
  development-only packages, to [requirements-dev.txt](requirements-dev.txt)
- Run `./setup.sh` when you need to install any new packages
- A live reload of the backend server will be triggered whenever you modify the [prephouse](prephouse)
  directory, [tests](tests) directory or their files

[docker-desktop]: https://www.docker.com/products/docker-desktop
[docker-compose]: (https://docs.docker.com/compose/install/)
[pre-commit]: https://pre-commit.com/

## Developer Tools

We support both Visual Studio Code and PyCharm out of the box with the proper
configurations automatically calibrated.

## Code Style

We are following the [PEP8][] style guide. A pre-commit hook
has been created to enforce that guide when you attempt to commit your code to the git repository.

[pep8]: https://www.python.org/dev/peps/pep-0008/

## Documentation

We use the reStructuredText format (reST) for writing docstrings in Python functions, classes, modules and so on
(see [PEP287][]). If you use VSCode, install the [_Python Docstring Generator_][vsc-ds-generator] extension; reST
will be set as the default docstring format. If you use PyCharm, go to Tools > Python Integrated Tools in the IDE
preferences and select reStructuredText as the docstring format.

[pep287]: https://www.python.org/dev/peps/pep-0287/
[vsc-ds-generator]: https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring
