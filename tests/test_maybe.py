from hypothesis import given, infer
from hypothesis.strategies import functions

from disregard.maybe import Just, Maybe, Nothing

pure_unary_function = functions(like=lambda x: x, pure=True)


class TestMaybe:
    def test_from_optional_nothing(self):
        assert Maybe.from_optional(None) == Nothing

    @given(value=infer)
    def test_from_optional_just(self, value: str):
        assert Maybe.from_optional(value) == Just(value)


class TestFunctorLaws:
    @given(value=infer)
    def test_identity(self, value: str):
        assert Just(value).map(lambda i: i) == Just(value)

    @given(f=pure_unary_function, g=pure_unary_function, value=infer)
    def test_composition(self, f, g, value: str):
        assert Just(value).map(f).map(g) == Just(g(f(value)))


class TestMonadLaws:
    @given(f=pure_unary_function, value=infer)
    def test_left_identity(self, f, value: str):
        assert Just(value).bind(lambda x: Just(f(x))) == Just(f(value))

    @given(value=infer)
    def test_right_identity(self, value: str):
        assert Just(value).bind(lambda x: Just(x)) == Just(value)

    @given(f=pure_unary_function, g=pure_unary_function, value=infer)
    def test_associativity(self, f, g, value: str):
        assert Just(value).bind(lambda x: Just(f(x))).bind(
            lambda x: Just(g(x))
        ) == Just(g(f(value)))


class TestNothing:
    def test_str(self):
        assert repr(Nothing) == "Nothing"

    def test_is_just(self):
        assert Nothing.is_just() is False

    def test_is_nothing(self):
        assert Nothing.is_nothing() is True


class TestJust:
    def test_str(self):
        assert repr(Just(1)) == "Just(1)"

    def test_is_just(self):
        assert Just(1).is_just() is True

    def test_is_nothing(self):
        assert Just(1).is_nothing() is False
