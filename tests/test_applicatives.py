import pytest  # type: ignore
from typing import Callable, Type, TypeVar

from monads import Applicative, Functor, Maybe, Result

T = TypeVar("T")
S = TypeVar("S")


@pytest.fixture(scope="module", params=[Maybe, Result])
def monad(request) -> Type:
    return request.param


def test_fmap_using_ap(monad) -> None:
    f: Callable[[int], int] = lambda x: x + 1
    m: Applicative[int] = monad.pure(3)
    assert m.map(f) == m.apply(monad.pure(f))
