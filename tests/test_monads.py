from typing import Callable

import pytest  # type: ignore

from monads import Monad
from .fixtures import monad


def test_bind(monad) -> None:
    expected: Monad[int] = monad.pure(2)
    assert expected == monad.pure(1).bind(lambda x: monad.pure(x + 1))


def test_bind_rshift_operator(monad) -> None:
    m: Monad[int] = monad.pure(2)
    f: Callable[[int], Monad[int]] = lambda x: monad.pure(x + 1)
    assert m.bind(f) == m >> f


def test_left_identity(monad) -> None:
    n: int = 3

    def f(n: int) -> Monad[int]:
        return monad.pure(n * 3)

    assert monad.pure(n).bind(f) == f(n)


def test_right_identity(monad) -> None:
    m: Monad[int] = monad.pure(3)
    assert m == m.bind(lambda x: monad.pure(x))


def test_associativity(monad) -> None:
    m: Monad[int] = monad.pure(3)

    def f(n: int) -> Monad[int]:
        return monad.pure(n * 3)

    def g(n: int) -> Monad[int]:
        return monad.pure(n + 5)

    assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))


def test_sequence(monad) -> None:
    assert monad.pure([1, 2, 3]) == monad.sequence(
        [monad.pure(1), monad.pure(2), monad.pure(3)]
    )
