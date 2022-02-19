from marshmallow import Schema
from webargs import fields


class UserPerfTrackingOverallScoresRequestSchema(Schema):
    pass


class UserPerfTrackingOverallScoresResponseSchema(Schema):
    latest_overall_score = fields.Float(required=True)
    overall_scores_history_current_user = fields.List(fields.Float)
    overall_scores_history_all_other_users = fields.List(fields.Float)
    average_overall_scores_history_all_other_users = fields.Float(required=True)


user_perf_tracking_overall_scores_request = UserPerfTrackingOverallScoresRequestSchema()
user_perf_tracking_overall_scores_response = UserPerfTrackingOverallScoresResponseSchema()
