from flask import current_app
from marshmallow import ValidationError


@current_app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return e.messages, 422
