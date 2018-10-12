import pytest  # type: ignore
from typing import Callable, Type, TypeVar
from monads import Functor, Maybe, Result

T = TypeVar("T")
S = TypeVar("S")


@pytest.fixture(scope="module", params=[Maybe, Result])
def monad(request) -> Type:
    return request.param


def test_identity(monad) -> None:
    m: Functor = monad.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m == m.map(identity)


def test_associativity(monad) -> None:
    f: Callable[[int], int] = lambda x: x + 1
    g: Callable[[int], str] = lambda x: str(x)
    m: Functor = monad.pure(3)
    assert m.map(lambda x: g(f(x))) == m.map(f).map(g)
