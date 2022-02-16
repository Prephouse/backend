# Prephouse Backend Server (ph-backend)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Instructions

### Setup

1. Download and install [Docker Desktop][docker-desktop], [Docker Compose][docker-compose] and
   [pre-commit][pre-commit]
2. Run Docker Desktop on your machine
3. Copy the environment variable files (.env.\*) and the Firebase configuration
   file (firebase-key.json) to the root directory of this repository
4. Run `./setup.sh`

### Startup

1. Run Docker Desktop on your machine
2. Run `docker-compose up` to start the local database session and local development server
3. Navigate to <http://localhost:3001> on your web browser

> We have separate services for the PSQL database, the database migration and the Flask app.
> Docker will run each service in a particular order such that the database should be up
> and ready by the time that the Flask app starts accepting HTTP requests.

### Development

#### Migration

In order to keep track of changes to the database across every environment, we have
migration scripts to upgrade and downgrade between each change. The migration scripts can
be found in the [migrations](/migrations) directory. The [migrate.sh](migrate.sh) script
includes all the commands you need to perform migrations on your local development environment.

- Run `./migrate.sh -h` to get a list of available migration commands
- Update the [mock.py](prephouse/mock.py) script to reflect your changes to the database schema

**Note:** You usually only need to run `./migrate.sh -u` after you have generated a new database
migration script. Otherwise, Docker automatically runs this command when you start the Docker
container via `docker-compose up`.

#### Packages

- Add any required external Python packages to [requirements.txt](requirements.txt)
- Run `docker-compose up --build --remove-orphans` when you need to install any new packages

#### Miscellaneous

- A live reload of the backend server will be triggered whenever you add, modify or delete files in
  the [prephouse](prephouse) or [tests](tests) directories
- Include in your PRs any changes to the generated gRPC code if you have updated the protobuf
  files in the analyzer-engine repository

[docker-desktop]: https://www.docker.com/products/docker-desktop
[docker-compose]: https://docs.docker.com/compose/install/
[pre-commit]: https://pre-commit.com/

## Developer Tools

We support Visual Studio Code and PyCharm out of the box.

You can test the APIs with any API client such as Postman or a web browser. Firefox, with the
`devtools.jsonview.enabled` flag enabled in the browser configuration, displays an excellent
JSON viewer for any HTTP response with `application/json` as the content type. Chrome and Edge can
accomplish something similar through the use of the JSON Formatter extension
([Chrome][json-formatter-chrome] | [Edge][json-formatter-edge]).

You can view the local Prephouse database with any PostgreSQL client, but we recommend
[Postico][postico] due to its clean and modern user interface. The host, port, username
and password for the Prephouse database can be found in [docker-compose.yml](docker-compose.yml).

[json-formatter-chrome]: https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa
[json-formatter-edge]: https://microsoftedge.microsoft.com/addons/detail/json-formatter-for-edge/njpoigijhgbionbfdbaopheedbpdoddi
[postico]: https://eggerapps.at/postico/

## Code Style

We are following the [Black Code Style][black-code-style] which is enforced in the pre-commit hook.

[pep8]: https://www.python.org/dev/peps/pep-0008/
[black-code-style]: https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html

## Documentation

We use the reStructuredText format (reST) for writing Python docstrings (see [PEP287][]). If you use VSCode,
install the [_Python Docstring Generator_][vsc-ds-generator] extension; reST will be set as the default docstring
format. If you use PyCharm, go to Tools > Python Integrated Tools in the IDE preferences and select reStructuredText
as the docstring format.

[pep287]: https://www.python.org/dev/peps/pep-0287/
[vsc-ds-generator]: https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring
