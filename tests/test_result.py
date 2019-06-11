from __future__ import annotations
from typing import Callable, List

from monads.maybe import Maybe, Just, Nothing
from monads.result import Result, Ok, Err, safe


def test_types() -> None:
    m: Result[int, str] = Result.pure(1)
    map: Result[int, str] = m.map(lambda x: x)
    map_operator: Result[int, str] = m * (lambda x: x)
    bind: Result[int, str] = m.bind(lambda x: Result.pure(x))
    bind_operator: Result[int, str] = m >> (lambda x: Result.pure(x))
    apply: Result[int, str] = m.apply(Result.pure(lambda x: x))
    apply_operator: Result[int, str] = Result.pure(lambda x: x) & m
    sequence: Result[List[int], str] = Result.sequence([m])


def test_bind_ok() -> None:
    m: Result[int, str] = Ok(5)
    increment: Callable[[int], Result[int, str]] = lambda x: Ok(x + 1)
    assert Ok(6) == m.bind(increment)


def test_bind_err() -> None:
    m: Result[int, str] = Err("oops")
    increment: Callable[[int], Result[int, str]] = lambda x: Ok(x + 1)
    assert Err("oops") == m.bind(increment)


def test_apply_ok_to_ok() -> None:
    m: Result[int, str] = Ok(5)
    increment: Callable[[int], int] = lambda x: x + 1
    assert Ok(6) == m.apply(Result.pure(increment))


def test_apply_ok_to_err() -> None:
    m: Result[int, str] = Err("oops")
    increment: Callable[[int], int] = lambda x: x + 1
    assert Err("oops") == m.apply(Result.pure(increment))


def test_apply_err_to_ok() -> None:
    m: Result[int, str] = Ok(5)
    f: Result[Callable[[int], int], str] = Err("oops")
    assert Err("oops") == m.apply(f)


def test_apply_err_to_err() -> None:
    m: Result[int, str] = Err("oops")
    f: Result[Callable[[int], int], str] = Err("oops")
    assert Err("oops") == m.apply(f)


def test_ok_withdefault() -> None:
    m: Result[int, str] = Ok(5)
    assert 5 == m.withDefault(0)


def test_err_withdefault() -> None:
    m: Result[int, str] = Err("oops")
    assert 0 == m.withDefault(0)


def test_map() -> None:
    result: Result[int, str] = Ok(5)
    mapped: Result[str, str] = result.map(str)
    assert "5" == mapped.withDefault("0")


def test_map_infix() -> None:
    result: Result[int, str] = Ok(5)
    mapped: Result[str, str] = result * str
    assert "5" == mapped.withDefault("0")


def test_map_error_err() -> None:
    m: Result[int, str] = Err("oops")
    assert Err(4) == m.mapError(len)


def test_map_error_ok() -> None:
    m: Result[int, str] = Ok(123)
    assert Ok(123) == m.mapError(len)


def test_bind() -> None:
    result: Result[int, str] = Ok(5)
    incremented: Result[int, str] = result.bind(lambda x: Ok(x + 1))
    assert 6 == incremented.withDefault(0)


def test_bind_infix() -> None:
    result: Result[int, str] = Ok(5)
    incremented: Result[int, str] = result >> (lambda x: Ok(x + 1))
    assert 6 == incremented.withDefault(0)


def test_pipeline() -> None:
    class Frobnicator(object):
        @classmethod
        def create(cls, config: dict) -> Result[Frobnicator, str]:
            return Ok(cls())

        def dostuff(self) -> Result[list, str]:
            return Ok(["a", "b", "c", "d"])

    def load_config() -> Result[dict, str]:
        return Ok({"foo": "bar"})

    result: Result[int, str] = (
        load_config()
        >> Frobnicator.create
        >> Frobnicator.dostuff
        >> (lambda res: Ok(len(res)))
    )
    assert 4 == result.withDefault(0)


def test_unsafe_wrapped_function_returns_error() -> None:
    error: Exception = Exception("oops")

    @safe
    def unsafe(x: int) -> int:
        if x > 5:
            raise error
        else:
            return x + 1

    result: Result[int, Exception] = unsafe(10)
    assert Err(error) == result


def test_safe_wrapped_function_returns_ok() -> None:
    error: Exception = Exception("oops")

    @safe
    def unsafe(x: int) -> int:
        if x > 5:
            raise error
        else:
            return x + 1

    result: Result[int, Exception] = unsafe(5)
    assert Ok(6) == result


def test_from_just() -> None:
    m: Maybe[int] = Just(6)
    result: Result[int, str] = Result.fromMaybe(m, "error")
    assert Ok(6) == result


def test_from_nothing() -> None:
    m: Maybe[int] = Nothing()
    result: Result[int, str] = Result.fromMaybe(m, "error")
    assert Err("error") == result


def test_ok_to_maybe() -> None:
    result: Result[int, str] = Ok(6)
    assert Just(6) == result.toMaybe()


def test_err_to_maybe() -> None:
    result: Result[int, str] = Err("error")
    assert Nothing() == result.toMaybe()


def test_from_optional_value() -> None:
    assert Just(2) == Maybe.fromOptional(2)


def test_from_optional_none() -> None:
    assert Err("error") == Result.fromOptional(None, "error")


def test_ok_to_optional() -> None:
    assert 2 == Ok(2).toOptional()


def test_err_to_optional() -> None:
    assert None == Err("error").toOptional()
