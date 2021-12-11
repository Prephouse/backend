from typing import Optional, TypedDict


class _OptionalSingleFeedbackType(TypedDict, total=False):
    time_start: int
    time_end: int


class _SingleFeedbackType(_OptionalSingleFeedbackType):
    id: str
    upload_id: str
    category: int
    comment: Optional[str]
    score: float


# awaiting support for typing.TypeAlias in mypy
FeedbackType = list[_SingleFeedbackType]  # type alias
