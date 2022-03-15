import functools
import random
from typing import Callable, ParamSpec, TypeAlias, Union

import rollbar
from firebase_admin import auth
from firebase_admin.auth import (
    CertificateFetchError,
    ExpiredIdTokenError,
    InvalidIdTokenError,
    RevokedIdTokenError,
    UserDisabledError,
)
from firebase_admin.exceptions import FirebaseError
from flask import Response, current_app, request
from sqlalchemy.exc import StatementError

from prephouse.models import User, db

P = ParamSpec("P")
ErrorResponse: TypeAlias = Union[tuple[dict[str, str], int], Response]


ANIMALS = [
    "Kangaroo",
    "Monkey",
    "Moose",
    "Mosquito",
    "Ostrich",
    "Otter",
    "Puffin",
    "Python",
    "Red Panda",
    "Rooster",
    "Scorpion",
    "Seahorse",
    "Sloth",
    "Slug",
    "Snail",
    "Snake",
    "Sparrow",
    "Swordfish",
    "Tarantula",
    "Tiger",
    "Tortoise",
    "Turtle",
    "Vampire Bat",
    "Walrus",
    "Whale",
    "Wolf",
    "Wolverine",
    "Zebra",
    "Alpaca",
    "Cat",
    "Chicken",
    "Dog",
    "Camel",
    "Duck",
    "Goat",
    "Goose",
    "Hedgehog",
    "Pigeon",
    "Rabbit",
    "Silkmoth",
    "Silver fox",
    "Turkey",
    "Donkey",
    "Goldfish",
    "Guinea Pig",
    "Guppy",
    "Horse",
    "Koi",
    "Llama",
    "Ringneck Dove",
    "Sheep",
    "Siamese Fighting Fish",
    "Yak",
    "Water Buffalo",
]


def private_route(f: Callable[P, ErrorResponse]) -> Callable[P, ErrorResponse]:
    @functools.wraps(f)
    def wrap(*args: P.args, **kwargs: P.kwargs) -> ErrorResponse:
        auth_header = request.headers.get("Authorization")
        if not auth_header and not current_app.debug:
            return {"message": "No token provided"}, 401

        try:
            if auth_header or not current_app.debug:
                id_token = auth_header.split(" ").pop()
                firebase_user = auth.verify_id_token(id_token, check_revoked=True)
                app_user = User.query.get(firebase_user["uid"])
                if not app_user:
                    app_user = User(
                        name=f"Anonymous {random.choice(ANIMALS)}",
                        email=firebase_user["email"],
                        id=firebase_user["uid"],
                    )
                    db.session.add(app_user)
                    db.session.commit()
            else:
                uid = request.args.get("test_uid")
                app_user = User.query.get(uid)
                if not app_user:
                    raise ValueError
        except (ValueError, InvalidIdTokenError):
            return {"message": "Invalid token provided"}, 401
        except ExpiredIdTokenError:
            return {"message": "Expired token provided"}, 401
        except (RevokedIdTokenError, UserDisabledError):
            return {"message": "Revoked token provided"}, 401
        except (FirebaseError, CertificateFetchError, StatementError):
            rollbar.report_exc_info(request=request)
            return {"message": "Unable to find or create user"}, 500
        else:
            request.user = app_user

        return f(*args, **kwargs)

    return wrap
