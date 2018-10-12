import pytest  # type: ignore
from typing import List
from monads.maybe import Maybe, Just, Nothing, maybe, first, last


def test_maybe_none():
    assert isinstance(maybe(None), Nothing)


def test_maybe_something():
    assert isinstance(maybe(False), Just)


def test_maybe_boolean_false():
    assert isinstance(maybe(False, predicate=bool), Nothing)


def test_maybe_boolean_true():
    assert isinstance(maybe(True, predicate=bool), Just)


def test_first() -> None:
    maybes: List[Maybe[int]] = [Nothing(), Just(1), Just(2)]
    assert Just(1) == first(maybes)

def test_last() -> None:
    maybes: List[Maybe[int]] = [Just(1), Just(2), Nothing()]
    assert Just(2) == last(maybes)
