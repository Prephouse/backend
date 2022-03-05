from flask import Blueprint, jsonify

from prephouse.decorators.authentication import private_route
from prephouse.models import UploadQuestion, db
from prephouse.schemas.upload_schema import new_question_upload_id_response_schema

upload_api = Blueprint("upload_api", __name__, url_prefix="/upload")


@upload_api.post("question/")
@private_route
def add_upload_question():
    response = {}
    upload_question_row = UploadQuestion()
    try:
        db.session.add(upload_question_row)
    except Exception:
        db.session.rollback()
        raise
    else:
        db.session.commit()

    response["id"] = upload_question_row.id if upload_question_row.id else -1

    return jsonify(new_question_upload_id_response_schema.dump(response))
