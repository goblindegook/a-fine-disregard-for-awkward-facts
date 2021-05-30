from typing import Callable, Generic, TypeVar

LeftSource = TypeVar("LeftSource")
RightSource = TypeVar("RightSource")
LeftReturn = TypeVar("LeftReturn")
RightReturn = TypeVar("RightReturn")
ReturnType = TypeVar("ReturnType")


class Either(Generic[LeftSource, RightSource]):
    def is_left(self):
        raise NotImplementedError

    def is_right(self):
        raise NotImplementedError

    def map(
        self, mapper: Callable[[RightSource], RightReturn]
    ) -> "Either[LeftSource, RightReturn]":
        raise NotImplementedError

    def map_left(
        self, mapper: Callable[[LeftSource], LeftReturn]
    ) -> "Either[LeftReturn, RightSource]":
        raise NotImplementedError

    def bind(
        self,
        mapper: Callable[[RightSource], "Either[LeftSource, RightReturn]"],
    ) -> "Either[LeftSource, RightReturn]":
        raise NotImplementedError

    def get(self, or_else: Callable[[LeftSource], RightSource]) -> RightSource:
        raise NotImplementedError

    def fold(
        self,
        left_mapper: Callable[[LeftSource], ReturnType],
        right_mapper: Callable[[RightSource], ReturnType],
    ) -> ReturnType:
        raise NotImplementedError

    def bimap(
        self,
        left_mapper: Callable[[LeftSource], LeftReturn],
        right_mapper: Callable[[RightSource], RightReturn],
    ) -> "Either[LeftReturn, RightReturn]":
        raise NotImplementedError

    def __eq__(self, other: object):
        raise NotImplementedError


class Left(Either[LeftSource, RightSource]):
    value: LeftSource

    def __init__(self, value: LeftSource):
        self.value = value

    def is_left(self):
        return True

    def is_right(self):
        return False

    def map(
        self, mapper: Callable[[RightSource], RightReturn]
    ) -> Either[LeftSource, RightReturn]:
        return Left(self.value)

    def map_left(
        self, mapper: Callable[[LeftSource], LeftReturn]
    ) -> "Either[LeftReturn, RightSource]":
        return Left(mapper(self.value))

    def bind(
        self,
        mapper: Callable[[RightSource], Either[LeftSource, RightReturn]],
    ) -> Either[LeftSource, RightReturn]:
        return Left(self.value)

    def get(self, or_else: Callable[[LeftSource], RightSource]) -> RightSource:
        return or_else(self.value)

    def fold(
        self,
        left_mapper: Callable[[LeftSource], ReturnType],
        right_mapper: Callable[[RightSource], ReturnType],
    ) -> ReturnType:
        return left_mapper(self.value)

    def bimap(
        self,
        left_mapper: Callable[[LeftSource], LeftReturn],
        right_mapper: Callable[[RightSource], RightReturn],
    ) -> Either[LeftReturn, RightReturn]:
        return Left(left_mapper(self.value))

    def __eq__(self, other: object):
        return isinstance(other, Left) and self.value == other.value

    def __repr__(self):
        return f"Left({repr(self.value)})"


class Right(Either[LeftSource, RightSource]):
    value: RightSource

    def __init__(self, value: RightSource):
        self.value = value

    def is_left(self):
        return False

    def is_right(self):
        return True

    def map(
        self, mapper: Callable[[RightSource], RightReturn]
    ) -> Either[LeftSource, RightReturn]:
        return Right(mapper(self.value))

    def map_left(
        self, mapper: Callable[[LeftSource], LeftReturn]
    ) -> "Either[LeftReturn, RightSource]":
        return Right(self.value)

    def bind(
        self,
        mapper: Callable[[RightSource], Either[LeftSource, RightReturn]],
    ) -> Either[LeftSource, RightReturn]:
        return mapper(self.value)

    def get(self, or_else: Callable[[LeftSource], RightSource]) -> RightSource:
        return self.value

    def fold(
        self,
        left_mapper: Callable[[LeftSource], ReturnType],
        right_mapper: Callable[[RightSource], ReturnType],
    ) -> ReturnType:
        return right_mapper(self.value)

    def bimap(
        self,
        left_mapper: Callable[[LeftSource], LeftReturn],
        right_mapper: Callable[[RightSource], RightReturn],
    ) -> Either[LeftReturn, RightReturn]:
        return Right(right_mapper(self.value))

    def __eq__(self, other: object):
        return isinstance(other, Right) and self.value == other.value

    def __repr__(self):
        return f"Right({repr(self.value)})"
