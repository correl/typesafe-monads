import pytest  # type: ignore
from typing import Any, Callable, Type
from monads.monoid import Monoid
from monads.maybe import First, Last, Just

Constructor = Callable[[Any], Monoid]


@pytest.fixture(
    scope="module", params=[lambda x: First(Just(x)), lambda x: Last(Just(x))]
)
def monoid(request) -> Constructor:
    return request.param


def test_associative(monoid: Constructor) -> None:
    a: Monoid = monoid(1)
    b: Monoid = monoid(2)
    c: Monoid = monoid(3)

    assert (a + b) + c == a + (b + c)


def test_mconcat_empty(monoid: Constructor) -> None:
    cls: Type = type(monoid(1))
    zero: Monoid = cls.mzero()
    assert zero == cls.mconcat([])

def test_mconcat(monoid: Constructor) -> None:
    cls: Type = type(monoid(1))
    a: Monoid = monoid(1)
    b: Monoid = monoid(2)
    c: Monoid = monoid(3)
    expected: Monoid = a.mappend(b).mappend(c)
    assert expected == cls.mconcat([a, b, c])
