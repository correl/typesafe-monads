import pytest  # type: ignore
from typing import Callable, TypeVar

from monads import Applicative
from .fixtures import monad

T = TypeVar("T")
S = TypeVar("S")


def test_fmap_using_ap(monad) -> None:
    f: Callable[[int], int] = lambda x: x + 1
    m: Applicative[int] = monad.pure(3)
    assert m.map(f) == m.apply(monad.pure(f))


def test_apply_and_operator(monad) -> None:
    subtract: Callable[[int], Callable[[int], int]] = lambda x: lambda y: x - y
    ten = monad.pure(10)
    six = monad.pure(6)
    functor = ten.map(subtract)
    assert six.apply(functor) == subtract * ten & six
