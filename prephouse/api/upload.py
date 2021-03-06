from flask import Blueprint, abort, jsonify, request
from webargs.flaskparser import use_kwargs

from prephouse.decorators.authentication import private_route
from prephouse.models import Feedback, Upload, UploadQuestion, db
from prephouse.schemas.upload_schema import (
    new_question_upload_request_schema,
    new_question_upload_response_schema,
    new_upload_session_request_schema,
    new_upload_session_response_schema,
    upload_cloudfronturl_request_schema,
    upload_instructions_request_schema,
    upload_instructions_response_schema,
)
from prephouse.utils.recaptcha import validate_recaptcha

upload_api = Blueprint("upload_api", __name__, url_prefix="/upload")


@upload_api.post("record")
@use_kwargs(new_upload_session_request_schema, location="query")
@private_route
def add_upload_record(category, token):
    if not validate_recaptcha(token, "submit_practice_session"):
        abort(400)

    response = {}
    upload_record_row = Upload(
        category=category,
        user_id=request.user.id,
    )
    try:
        db.session.add(upload_record_row)
    except Exception:
        db.session.rollback()
        raise
    else:
        db.session.commit()

    response["id"] = upload_record_row.id if upload_record_row.id else -1

    return jsonify(new_upload_session_response_schema.dump(response))


@upload_api.post("question")
@use_kwargs(new_question_upload_request_schema, location="query")
@private_route
def add_upload_question(upload_id, question_id):
    response = {}
    upload = Upload.query.get(upload_id)
    if upload is None or upload.user_id != request.user.id:
        abort(401)

    upload_question_row = UploadQuestion(upload_id=upload_id, question_id=question_id)
    try:
        db.session.add(upload_question_row)
    except Exception:
        db.session.rollback()
        raise
    else:
        db.session.commit()

    response["id"] = upload_question_row.id if upload_question_row.id else -1

    return jsonify(new_question_upload_response_schema.dump(response))


@upload_api.get("/instructions")
@use_kwargs(upload_instructions_request_schema, location="query")
def get_user_instructions(category, medium, origin):
    video_only_features = Feedback.FeedbackCategory.get_video_only_features()
    response = {
        "feedback_categories": [
            c.get_feature_name()
            for c in Feedback.FeedbackCategory
            if medium == Upload.UploadMedium.VIDEO_AUDIO or c not in video_only_features
        ],
        "post_analysis": (
            "The analysis will take a considerable amount of time. Once the analysis has "
            "been completed, you will receive an email to inform you of the completion. "
            "The email will contain a link to a page with the playback of your submission "
            "along with the corresponding feedback. Your past submissions and feedbacks "
            "can also be accessed in the <i>My Progress</i> page. Your submissions will also "
            "be included as part of the global leaderboard in the <i>Leaderboard</i> page."
        ),
        "confirmation": (
            "Your submissions will be stored securely on the Prephouse servers, will "
            "never be shared with anyone outside of Prephouse or used for any purposes "
            "other to generate feedback. If you have any further questions or you are not "
            "satisfied with the feedback, please fill out the form in our "
            "<i>Support</i> page."
        ),
    }

    if category == Upload.UploadCategory.INTERVIEW:
        response["pre_analysis"] = (
            "Once you have answered the question and ended the interview, your mock interview "
            "will be submitted to the Prephouse servers for automated analysis. The analysis "
            "generates an overall score for your interview as well as numerical and textual "
            "feedback for the following criteria."
        )
        if origin == Upload.UploadOrigin.RECORD:
            response["overview"] = (
                "You will be asked an interview question from the Prephouse "
                "question bank. The question is selected at random. For each question, "
                "you will be asked to record yourself using your webcam and microphone with "
                "your answer to that question. These recordings collectively form your mock "
                "interview. You can only answer one question at a time. Moreover, there is a "
                "time limit of 30 minutes across all questions, so please plan your time "
                "accordingly."
            )
        elif origin == Upload.UploadOrigin.UPLOAD:
            response["overview"] = (
                "You will be asked an interview question from the Prephouse question "
                "bank. The question is selected at random. For each question, you will be asked "
                "to upload a media file from your computer with your answer to that question. "
                "These uploads collectively form your mock interview. There is a time limit of "
                "30 minutes across all questions, so please plan your time accordingly."
            )
    elif category == Upload.UploadCategory.PRESENTATION:
        response["pre_analysis"] = (
            "Once you have completed your presentation, or once the time limit has "
            "been exceeded, your mock presentation will be submitted to the Prephouse "
            "servers for automated analysis. The analysis generates an overall score "
            "for your presentation as well as numerical and textual feedback for the "
            "following criteria."
        )
        if origin == Upload.UploadOrigin.RECORD:
            response["overview"] = (
                "You will be asked to record a presentation of up to 30 minutes using "
                "your webcam and microphone."
            )
        elif origin == Upload.UploadOrigin.UPLOAD:
            response["overview"] = (
                "You will be asked to upload a presentation of up to 30 minutes from "
                "your computer."
            )

    return jsonify(upload_instructions_response_schema.dump(response))


@upload_api.post("/cloudfront")
@use_kwargs(upload_cloudfronturl_request_schema, location="query")
def add_cloudfront_url(file, cloudfront, manifest):
    upload_row = UploadQuestion.query.filter_by(id=file)
    upload_row.update({"cloudfront_url": cloudfront})
    upload_row.update({"manifest_file": manifest})
    db.session.commit()
    return {}
