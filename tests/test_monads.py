import pytest  # type: ignore
from typing import List, Type
from monads import Monad, Maybe, Result


@pytest.fixture(scope="module", params=[Maybe, Result])
def monad(request) -> Type:
    return request.param


def test_bind(monad) -> None:
    expected: Monad[int] = monad.unit(2)
    assert expected == monad.unit(1).bind(lambda x: monad.unit(x + 1))


def test_left_identity(monad) -> None:
    n: int = 3

    def f(n: int) -> Monad[int]:
        return monad.unit(n * 3)

    assert monad.unit(n).bind(f) == f(n)


def test_right_identity(monad) -> None:
    m: Monad[int] = monad.unit(3)
    assert m == m.bind(lambda x: monad.unit(x))


def test_associativity(monad) -> None:
    m: Monad[int] = monad.unit(3)

    def f(n: int) -> Monad[int]:
        return monad.unit(n * 3)

    def g(n: int) -> Monad[int]:
        return monad.unit(n + 5)

    assert m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))
