from marshmallow import Schema, validate
from webargs import fields

from prephouse.models import Upload


class LeaderboardRequestSchema(Schema):
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=25)


class LeaderboardResponseSchema(Schema):
    class SingleLeaderboardEntry(Schema):
        standing = fields.Int(validate=validate.Range(min=1), required=True)
        session_id = fields.UUID(required=True)
        username = fields.Str(required=True)
        score = fields.Float(required=True)
        date_uploaded = fields.DateTime(required=True)
        category = (
            fields.Int(
                required=True,
                validate=validate.OneOf(list(map(int, Upload.UploadCategory))),
            ),
        )
        category_name = fields.Str(required=True)
        includes_video = fields.Bool(required=True)
        engine_version = fields.Str()

    next_page = fields.Int(required=True)
    has_next = fields.Bool(required=True)
    total_pages = fields.Int(required=True)
    uploads = fields.List(
        fields.Nested(SingleLeaderboardEntry),
        required=True,
    )


class LeaderboardOverviewRequestSchema(Schema):
    pass


class LeaderboardOverviewResponseSchema(Schema):
    latest_overall_score = fields.Float(missing=None)
    average_overall_score_user = fields.Float(missing=None)
    average_overall_score_global = fields.Float(missing=None)


leaderboard_request_schema = LeaderboardRequestSchema()
leaderboard_response_schema = LeaderboardResponseSchema()
leaderboard_overview_request_schema = LeaderboardOverviewRequestSchema()
leaderboard_overview_response_schema = LeaderboardOverviewResponseSchema()
