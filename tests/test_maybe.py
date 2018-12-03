import pytest  # type: ignore
from typing import Callable, List

from monads.maybe import Maybe, Just, Nothing, maybe, first, last


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
