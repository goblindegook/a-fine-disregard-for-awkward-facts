from hypothesis import given, infer
from hypothesis.strategies import functions

from disregard.either import Left, Right

pure_unary_function = functions(like=lambda x: x, pure=True)


class TestFunctorLaws:
    @given(value=infer)
    def test_identity(self, value: str):
        assert Right(value).map(lambda i: i) == Right(value)

    @given(f=pure_unary_function, g=pure_unary_function, value=infer)
    def test_composition(self, f, g, value: str):
        assert Right(value).map(f).map(g) == Right(g(f(value)))


class TestMonadLaws:
    @given(f=pure_unary_function, value=infer)
    def test_left_identity(self, f, value: str):
        assert Right(value).bind(lambda x: Right(f(x))) == Right(f(value))

    @given(value=infer)
    def test_right_identity(self, value: str):
        assert Right(value).bind(lambda x: Right(x)) == Right(value)

    @given(f=pure_unary_function, g=pure_unary_function, value=infer)
    def test_associativity(self, f, g, value: str):
        assert Right(value).bind(lambda x: Right(f(x))).bind(
            lambda x: Right(g(x))
        ) == Right(g(f(value)))


class TestLeft:
    def test_str(self):
        assert repr(Left(1)) == "Left(1)"

    def test_is_right(self):
        assert Left(1).is_right() is False

    def test_is_left(self):
        assert Left(1).is_left() is True

    def test_get(self):
        assert Left(1).get(lambda x: f"L:{x}") == "L:1"

    def test_map_left(self):
        assert Right(1).map_left(lambda x: x + 1) == Right(1)

    def test_fold(self):
        assert Left(1).fold(lambda x: f"L:{x}", lambda x: f"R:{x}") == "L:1"

    def test_bimap(self):
        assert Left(1).bimap(lambda x: f"L:{x}", lambda x: f"R:{x}") == Left("L:1")


class TestRight:
    def test_str(self):
        assert repr(Right(1)) == "Right(1)"

    def test_is_right(self):
        assert Right(1).is_right() is True

    def test_is_left(self):
        assert Right(1).is_left() is False

    def test_get(self):
        assert Right(1).get(lambda x: x) == 1

    def test_map_left(self):
        assert Left(1).map_left(lambda x: x + 1) == Left(2)

    def test_fold(self):
        assert Right(1).fold(lambda x: f"L:{x}", lambda x: f"R:{x}") == "R:1"

    def test_bimap(self):
        assert Right(1).bimap(lambda x: f"L:{x}", lambda x: f"R:{x}") == Right("R:1")
