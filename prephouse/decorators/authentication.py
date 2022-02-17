import functools
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
                app_user = User.query.filter_by(id=firebase_user["uid"]).first()
                if not app_user:
                    app_user = User(
                        name=firebase_user["display_name"],
                        email=firebase_user["email"],
                        id=firebase_user["uid"],
                    )
                    db.session.add(app_user)
                    db.session.commit()
            else:
                uid = request.args.get("test_uid")
                app_user = User.query.filter_by(id=uid).first()
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
