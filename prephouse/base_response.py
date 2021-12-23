from typing import Generic, TypeAlias, TypeVar, Union

S = TypeVar("S", str, dict, list[dict])
T = TypeVar("T")


ErrorMessage: TypeAlias = str | None
ErrorResponse: TypeAlias = tuple[ErrorMessage, int]
BaseResponse: TypeAlias = Union[S, tuple[S, int], ErrorResponse]


class BaseTestResponse(Generic[T]):
    response: T
