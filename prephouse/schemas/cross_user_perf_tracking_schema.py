from marshmallow import Schema
from webargs import fields


class UserPerfTrackingOverallScoresRequestSchema(Schema):
    user_id = fields.UUID(required=True)


class UserPerfTrackingOverallScoresResponseSchema(Schema):
    latest_overall_score = fields.Float(required=True)
    all_user_overall_score_data = fields.List(fields.Float)
    all_users_overall_scores_data = fields.List(fields.Float)
    average_all_overall_score_all_users = fields.Float(required=True)


user_perf_tracking_overall_scores_request = UserPerfTrackingOverallScoresRequestSchema()
user_perf_tracking_overall_scores_response = UserPerfTrackingOverallScoresResponseSchema()
