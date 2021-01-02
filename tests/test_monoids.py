import pytest  # type: ignore
from typing import Any, Callable, Tuple, Type

from monads.list import List
from monads.monoid import Monoid, String, Addition, Multiplication
from monads.maybe import First, Last, Just

Constructor = Tuple[Type, Callable[[Any], Any]]


@pytest.fixture(
    scope="module",
    params=[
        (First, lambda x: Just(x)),
        (Last, lambda x: Just(x)),
        (String, lambda x: str(x)),
        (Addition, lambda x: x),
        (Multiplication, lambda x: x),
        (List, lambda x: [x]),
    ],
)
def constructor(request) -> Constructor:
    return request.param


def construct(constructor: Constructor, value: Any) -> Monoid:
    cls, builder = constructor
    return cls(builder(value))


def test_mappend_add_operator(constructor: Constructor) -> None:
    a: Monoid = construct(constructor, 1)
    b: Monoid = construct(constructor, 2)
    assert a.mappend(b) == a + b


def test_associative(constructor: Constructor) -> None:
    a: Monoid = construct(constructor, 1)
    b: Monoid = construct(constructor, 2)
    c: Monoid = construct(constructor, 3)

    assert (a + b) + c == a + (b + c)


def test_mconcat_empty(constructor: Constructor) -> None:
    cls, _ = constructor
    zero: Monoid = cls.mzero()
    assert zero == cls.mconcat([])


def test_mconcat(constructor: Constructor) -> None:
    cls, _ = constructor
    a: Monoid = construct(constructor, 1)
    b: Monoid = construct(constructor, 2)
    c: Monoid = construct(constructor, 3)
    expected: Monoid = a.mappend(b).mappend(c)
    assert expected == cls.mconcat([a, b, c])


def test_immutability(constructor: Constructor) -> None:
    a: Monoid = construct(constructor, 1)
    assert a.value != None
    with pytest.raises(AttributeError) as excinfo:
        # this is ignore on porpouse othewise the mypy test fail. Uncomment to check the Final check with mypy
        a.value = 2  # type: ignore
    assert "can't set attribute" in str(excinfo.value)
