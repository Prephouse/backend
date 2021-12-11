from typing import Generic, TypeVar, Union

S = TypeVar("S", dict, list[dict])
T = TypeVar("T")


# awaiting support for typing.TypeAlias in mypy
ErrorMessage = Union[str, None]  # type alias
ErrorResponse = tuple[ErrorMessage, int]  # type alias
BaseResponse = Union[S, tuple[S, int], ErrorResponse]  # type alias


class TestResponse(Generic[T]):
    response: T
