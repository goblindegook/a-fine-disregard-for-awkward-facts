from typing import Any, Callable, Generic, Optional, TypeVar

SourceType = TypeVar("SourceType")
ReturnType = TypeVar("ReturnType")


class Maybe(Generic[SourceType]):
    value: SourceType
    _is_just: bool

    def __init__(self, value: SourceType, is_just: bool):
        self.value = value
        self._is_just = is_just

    @classmethod
    def from_optional(cls, value: Optional[SourceType]) -> "Maybe[SourceType]":
        return Nothing if value is None else Just(value)

    def is_just(self):
        return self._is_just

    def is_nothing(self):
        return not self._is_just

    def map(self, mapper: Callable[[SourceType], ReturnType]) -> "Maybe[ReturnType]":
        return Maybe(mapper(self.value), self._is_just) if self._is_just else Nothing

    def bind(
        self, mapper: Callable[[SourceType], "Maybe[ReturnType]"]
    ) -> "Maybe[ReturnType]":
        return mapper(self.value) if self._is_just else Nothing

    def __eq__(self, other: object):
        return (
            isinstance(other, Maybe)
            and self.is_just() == other.is_just()
            and self.value == other.value
        )

    def __repr__(self):
        return f"Just({repr(self.value)})" if self._is_just else "Nothing"


Nothing: Maybe[Any] = Maybe(None, False)


def Just(value: SourceType) -> Maybe[SourceType]:
    return Maybe(value, True)
