# Prephouse Backend Server (ph-backend)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Instructions

### Setup

1. Download and install [Docker Desktop][docker-desktop], [Docker Compose][docker-compose] and
   [pre-commit][pre-commit]
2. Run Docker Desktop on your machine
3. Copy the environment variable files (.env.\*) to the root directory of this repository
4. Run `./setup.sh`

### Startup

1. Run Docker Desktop on your machine
2. Run `docker-compose up` to start the local database session and local development server
3. Navigate to <http://localhost:3001> on your web browser

### Development

- Add any required external Python packages to [requirements.txt](requirements.txt) or, for
  development-only packages, to [requirements-dev.txt](requirements-dev.txt)
- Run `./setup.sh` when you need to install any new packages
- A live reload of the backend server will be triggered whenever you add, modify or delete files in
  the [prephouse](prephouse) or [tests](tests) directories

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
[Postico][postico] due to its clean and modern user interface. The username and password
for the Prephouse database can be found in [docker-compose.yml](docker-compose.yml).

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

## Implementation

This section clarifies some details on the implementation of the backend server subsystem. We try to defer as many
details as possible to the official library documentations, but sometimes our implementation may deviate from other
similar projects.

### Database models and queries

We use [Flask-SQLAlchemy][flask-sqlalchemy] as our object relational mapper (ORM). The global database
instance is created and stored in the [models.py](prephouse/models.py) module.

The database models are declared within [models.py](prephouse/models.py). For columns with an enum type,
use a native Python `Enum` and declare the enum class inside the corresponding model class, i.e., as an
inner class. These enum classes should be annotated with the `@enum.unique` decorator to prevent
two or more enum members from having the same values. Furthermore, if your enum values are entirely integers,
consider the use of `IntEnum` over the more generic `Enum` class. The former class subclasses the enum values
as Python `int`s and therefore enables us to perform many of the same operations on the enum members.

When you need to make a database query, use the Flask-SQLAlchemy wrapper functions to create your query.
For example, use a `.filter` on the query object (for clarity, the query object refers to the query property
in a particular Flask-SQLAlchemy model such as `Model.query`) in lieu of a raw SQL `WHERE` clause. This
reduces the amount of boilerplate code and helps prevent SQL injection attacks. In the **extremely rare**
case where the Flask-SQLAlchemy wrapper functions are not suitable, make sure to use a prepared statement
for the query. Moreover, do not forget to commit the results of any insertion, update or deletion query
with the `query.commit()` function; otherwise, the changes will not be saved in the database.

[flask-sqlalchemy]: https://flask-sqlalchemy.palletsprojects.com/en/2.x/

### REST APIs

We use [Flask][flask] as our backend framework. Our Flask application comes into two variations, namely
the standard variation and test variation. In the standard variation, which is designed for the staging
and production environments, the Flask configurations are "strict" and are similar to what you would expect
in a production-ready web server. In the test variation, the Flask configurations are lenient with
minimal security checks and, in some cases, may be randomized.

In order to implement a new API endpoint, follow these steps:

1. Create a Flask blueprint within a new Python module in the [api](prephouse/api) package
2. Register your blueprint in the app initialization module (i.e., [prephouse/\_\_init\_\_.py](prephouse/__init__.py))
3. Choose the appropriate URL prefix for the blueprint
4. Create the Python function for the API endpoint
5. Annotate the Python function with the relevant HTTP method(s)

```python
# Blueprint Example
from flask import Blueprint

some_api = Blueprint("some_api", __name__, url_prefix="/api")


@some_api.get("/")
def my_method():
    """
    Implementation goes here.
    """
```

The relevant HTTP security mechanisms, such as CORS and CSP headers, are automatically sent with each HTTP response.
Avoid any modifications to these mechanisms for your specific API endpoint.

When an HTTP request is successful, the corresponding API should always return a JSON array or JSON object with a
2XX status code. Otherwise, the API should call `flask.abort()` with the most relevant HTTP status code and,
where applicable, with a dictionary of reasons for the failure.

If you need the current app context for your API, import the `current_app` object from the Flask library.
Do not try to import the `app` object from [prephouse/\_\_init\_\_.py](prephouse/__init__.py) as that would
likely cause import errors.

[flask]: https://flask.palletsprojects.com/en/2.0.x/

### Schema declaration and validation

We use the [marshmallow] library to declare the schemas for our HTTP query parameters, request body and response data,
and to validate those data against the relevant schemas. The schemas are located in the [schemas](prephouse/schemas)
package. Each Python module in that package should correspond to a single Flask blueprint.

Before retrieving the HTTP query parameters and request body, you should call the `validate` method on the
corresponding schema. If marshmallows returns errors in the validation process, then the API should abort
immediately with an HTTP 422 error code. Likewise, before returning the HTTP response, you should call the `dump`
method on the corresponding schema to serialize the HTTP response data in accordance with the schema fields. The
following code block provides a minimal example of the schema validation.

```python
from flask import abort, current_app, jsonify, request
from marshmallow import Schema, fields


class SomeRequestSchema(Schema):
    school: fields.str(required=True)


class SomeResponseSchema(Schema):
    country: fields.str()


some_request_schema = SomeRequestSchema()
some_response_schema = SomeResponseSchema()


@current_app.route("/")
def my_method():
    if validation_errors := some_request_schema.validate(request.args):
        abort(422, validation_errors)
    # some logic goes here...
    res = {"country": "Canada"}
    return jsonify(some_response_schema.dump(res))
```

In order to reference a native Python `Enum` as a schema field type, declare the field type as the type of the enum
values and then map the enum values to a single list and call `validate.OneOf()` on the list as the validator for that
field. Consider the following `IntEnum` as an example.

```python
import enum
from marshmallow import fields, Schema, validate


class SomeEnum(enum.IntEnum):
    HELLO = 0
    BYE = 1


class SomeSchema(Schema):
    greeting = fields.Int(validate=validate.OneOf(list(map(int, SomeEnum))))
```

[marshmallow]: https://marshmallow.readthedocs.io/en/stable/
