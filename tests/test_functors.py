import pytest  # type: ignore
from typing import Callable, TypeVar

from monads import Functor
from .fixtures import monad

T = TypeVar("T")
S = TypeVar("S")


def test_identity(monad) -> None:
    m: Functor = monad.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m == m.map(identity)


def test_associativity(monad) -> None:
    f: Callable[[int], int] = lambda x: x + 1
    g: Callable[[int], str] = lambda x: str(x)
    m: Functor = monad.pure(3)
    assert m.map(lambda x: g(f(x))) == m.map(f).map(g)


def test_map_mul_operator(monad) -> None:
    m: Functor = monad.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m.map(identity) == m * identity


def test_map_rmul_operator(monad) -> None:
    m: Functor = monad.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m.map(identity) == identity * m
