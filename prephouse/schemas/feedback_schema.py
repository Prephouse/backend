from typing import Optional, TypedDict


class _OptionalSingleFeedbackSchema(TypedDict, total=False):
    time_start: int
    time_end: int


class _SingleFeedbackSchema(_OptionalSingleFeedbackSchema):
    id: str
    upload_id: str
    category: int
    comment: Optional[str]
    score: float


# awaiting support for typing.TypeAlias in mypy
FeedbackSchema = list[_SingleFeedbackSchema]  # type alias
