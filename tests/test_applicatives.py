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
