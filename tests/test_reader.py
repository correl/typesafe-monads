import pytest  # type: ignore
from typing import Any, Callable, TypeVar

from monads import Functor, Applicative, Reader
from monads.reader import curry

T = TypeVar("T")
S = TypeVar("S")


def test_functor_identity() -> None:
    m: Reader = Reader.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m(0) == m.map(identity)(0)


def test_functor_associativity() -> None:
    f: Callable[[int], int] = lambda x: x + 1
    g: Callable[[int], str] = lambda x: str(x)
    m: Reader[int, int] = Reader.pure(3)
    assert m.map(lambda x: g(f(x)))(0) == m.map(f).map(g)(0)


def test_functor_map_mul_operator() -> None:
    m: Reader = Reader.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m.map(identity)(0) == (m * identity)(0)


def test_functor_map_rmul_operator() -> None:
    m: Reader = Reader.pure(3)
    identity: Callable[[T], T] = lambda x: x
    assert m.map(identity)(0) == (identity * m)(0)


def test_applicative_fmap_using_ap() -> None:
    f: Callable[[int], int] = lambda x: x + 1
    m: Reader[int, int] = Reader.pure(3)
    assert m.map(f)(0) == m.apply(Reader.pure(f))(0)


def test_monad_bind() -> None:
    expected: Reader[int, int] = Reader.pure(2)
    m: Reader[int, int] = Reader.pure(1)
    assert expected(0) == m.bind(lambda x: Reader.pure(x + 1))(0)


def test_monad_bind_rshift_operator() -> None:
    m: Reader[int, int] = Reader.pure(2)
    f: Callable[[int], Reader[int, int]] = lambda x: Reader.pure(x + 1)
    assert m.bind(f)(0) == (m >> f)(0)


def test_monad_left_identity() -> None:
    n: int = 3

    def f(n: int) -> Reader[int, int]:
        return Reader.pure(n * 3)

    m: Reader[int, int] = Reader.pure(n)
    assert m.bind(f)(0) == f(n)(0)


def test_monad_right_identity() -> None:
    m: Reader[int, int] = Reader.pure(3)
    assert m(0) == m.bind(lambda x: Reader.pure(x))(0)


def test_monad_associativity() -> None:
    m: Reader[int, int] = Reader.pure(3)

    def f(n: int) -> Reader[int, int]:
        return Reader.pure(n * 3)

    def g(n: int) -> Reader[int, int]:
        return Reader.pure(n + 5)

    assert m.bind(f).bind(g)(0) == m.bind(lambda x: f(x).bind(g))(0)


def test_curry() -> None:
    def add3(a, b, c):
        return a + b + c

    assert add3(1, 2, 3) == curry(add3)(1)(2)(3)


def test_call_curried_function_with_multiple_arguments() -> None:
    @curry
    def add3(a, b, c):
        return a + b + c

    assert add3(1, 2)(3) == add3(1, 2, 3)
