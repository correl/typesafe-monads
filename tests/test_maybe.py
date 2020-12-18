import pytest  # type: ignore
from typing import Callable, List

from monads.maybe import Maybe, Just, Nothing, maybe, first, last
from monads.result import Ok, Err


def test_types() -> None:
    m: Maybe[int] = Maybe.pure(1)
    map: Maybe[int] = m.map(lambda x: x)
    map_operator: Maybe[int] = m * (lambda x: x)
    bind: Maybe[int] = m.bind(lambda x: Maybe.pure(x))
    bind_operator: Maybe[int] = m >> (lambda x: Maybe.pure(x))
    apply: Maybe[int] = m.apply(Maybe.pure(lambda x: x))
    apply_operator: Maybe[int] = Maybe.pure(lambda x: x) & m
    sequence: Maybe[List[int]] = Maybe.sequence([m])


def test_bind_just() -> None:
    m: Maybe[int] = Just(5)
    increment: Callable[[int], Maybe[int]] = lambda x: Just(x + 1)
    assert Just(6) == m.bind(increment)


def test_bind_nothing() -> None:
    m: Maybe[int] = Nothing()
    increment: Callable[[int], Maybe[int]] = lambda x: Just(x + 1)
    assert Nothing() == m.bind(increment)


def test_apply_just_to_just() -> None:
    m: Maybe[int] = Just(5)
    increment: Callable[[int], int] = lambda x: x + 1
    assert Just(6) == m.apply(Maybe.pure(increment))


def test_apply_just_to_nothing() -> None:
    m: Maybe[int] = Nothing()
    increment: Callable[[int], int] = lambda x: x + 1
    assert Nothing() == m.apply(Maybe.pure(increment))


def test_apply_nothing_to_just() -> None:
    m: Maybe[int] = Just(5)
    f: Maybe[Callable[[int], int]] = Nothing()
    assert Nothing() == m.apply(f)


def test_apply_nothing_to_nothing() -> None:
    m: Maybe[int] = Nothing()
    f: Maybe[Callable[[int], int]] = Nothing()
    assert Nothing() == m.apply(f)


def test_just_withdefault() -> None:
    m: Maybe[int] = Just(5)
    assert 5 == m.withDefault(0)


def test_nothing_withdefault() -> None:
    m: Maybe[int] = Nothing()
    assert 0 == m.withDefault(0)


def test_maybe_none() -> None:
    assert isinstance(maybe(None), Nothing)


def test_maybe_something() -> None:
    assert isinstance(maybe(False), Just)


def test_maybe_boolean_false() -> None:
    assert isinstance(maybe(False, predicate=bool), Nothing)


def test_maybe_boolean_true() -> None:
    assert isinstance(maybe(True, predicate=bool), Just)


def test_first() -> None:
    maybes: List[Maybe[int]] = [Nothing(), Just(1), Just(2)]
    assert Just(1) == first(maybes)


def test_last() -> None:
    maybes: List[Maybe[int]] = [Just(1), Just(2), Nothing()]
    assert Just(2) == last(maybes)


def test_from_empty_list() -> None:
    assert Nothing() == Maybe.fromList([])


def test_from_nonempty_list() -> None:
    assert Just(2) == Maybe.fromList([2, 4, 6])


def test_from_ok() -> None:
    assert Just(3) == Maybe.fromResult(Ok(3))


def test_from_err() -> None:
    assert Nothing() == Maybe.fromResult(Err("oops"))


def test_just_to_result() -> None:
    assert Ok(3) == Just(3).toResult("oops")


def test_nothing_to_result() -> None:
    assert Err("oops") == Nothing().toResult("oops")


def test_from_optional_value() -> None:
    assert Just(2) == Maybe.fromOptional(2)


def test_from_optional_none() -> None:
    assert Nothing() == Maybe.fromOptional(None)


def test_just_to_optional() -> None:
    assert 2 == Just(2).toOptional()


def test_nothing_to_optional() -> None:
    assert None == Nothing().toOptional()


def test_as_iterable() -> None:
    m_empty: Maybe[str] = Nothing()
    i = 0
    for n in m_empty:
        i = i + 1
    assert i == 0

    for n in Just("one"):
        i = i + 1
    assert i == 1

    assert len(m_empty) == 0
    assert len(Just("one")) == 1


def test_or_else() -> None:
    m_empty: Maybe[str] = Nothing()
    assert m_empty.or_else("backup") == "backup"

    m_full: Maybe[str] = Just("becon")
    assert m_full.or_else("backup") == "becon"


def test_flatten() -> None:
    m_empty: Maybe[Maybe[str]] = Just(Nothing())
    m_flat: Maybe[str] = m_empty.flatten()
    assert m_flat.or_else("backup") == "backup"

    m_full: Maybe[Maybe[str]] = Just(Just("becon"))
    assert m_full.flatten().or_else("backup") == "becon"
