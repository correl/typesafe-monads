from __future__ import annotations
from monads.result import Result, Ok, Err, safe


def test_value() -> None:
    result: Result[int, str] = Ok(5)
    assert 5 == result.withDefault(0)


def test_error() -> None:
    result: Result[int, str] = Err("oops")
    assert 0 == result.withDefault(0)


def test_fmap() -> None:
    result: Result[int, str] = Ok(5)
    mapped: Result[str, str] = result.fmap(str)
    assert "5" == mapped.withDefault("0")


def test_fmap_infix() -> None:
    result: Result[int, str] = Ok(5)
    mapped: Result[str, str] = result * str
    assert "5" == mapped.withDefault("0")


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
