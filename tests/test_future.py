import pytest  # type: ignore
from typing import Any, Callable, List, TypeVar

from monads import Functor, Applicative, Future

T = TypeVar("T")
S = TypeVar("S")


@pytest.mark.asyncio
async def test_types() -> None:
    m: Future[int] = Future.pure(1)
    await m
    map: Future[int] = Future.pure(1).map(lambda x: x)
    await map
    map_operator: Future[int] = Future.pure(1) * (lambda x: x)
    await map_operator
    bind: Future[int] = Future.pure(1).bind(lambda x: Future.pure(x))
    await bind
    bind_operator: Future[int] = Future.pure(1) >> (lambda x: Future.pure(x))
    await bind_operator
    apply: Future[int] = Future.pure(1).apply(Future.pure(lambda x: x))
    await apply
    apply_operator: Future[int] = Future.pure(lambda x: x) & Future.pure(1)
    await apply_operator
    sequence: Future[List[int]] = Future.sequence([Future.pure(1)])
    await sequence


@pytest.mark.asyncio
async def test_functor_identity() -> None:
    identity: Callable[[int], int] = lambda x: x
    assert await Future.pure(3) == await Future.pure(3).map(identity)


@pytest.mark.asyncio
async def test_functor_associativity() -> None:
    f: Callable[[int], int] = lambda x: x + 1
    g: Callable[[int], str] = lambda x: str(x)
    assert await Future.pure(3).map(lambda x: g(f(x))) == await Future.pure(3).map(
        f
    ).map(g)


@pytest.mark.asyncio
async def test_functor_map_mul_operator() -> None:
    identity: Callable[[int], int] = lambda x: x
    assert await Future.pure(3).map(identity) == await (Future.pure(3) * identity)


@pytest.mark.asyncio
async def test_functor_map_rmul_operator() -> None:
    identity: Callable[[int], int] = lambda x: x
    assert await Future.pure(3).map(identity) == await (identity * Future.pure(3))


@pytest.mark.asyncio
async def test_applicative_fmap_using_ap() -> None:
    f: Callable[[int], int] = lambda x: x + 1
    assert await Future.pure(3).map(f) == await Future.pure(3).apply(Future.pure(f))


@pytest.mark.asyncio
async def test_monad_bind() -> None:
    expected: Future[int] = Future.pure(2)
    m: Future[int] = Future.pure(1)
    assert await expected == await m.bind(lambda x: Future.pure(x + 1))


@pytest.mark.asyncio
async def test_monad_bind_rshift_operator() -> None:
    f: Callable[[int], Future[int]] = lambda x: Future.pure(x + 1)
    assert await Future.pure(2).bind(f) == await (Future.pure(2) >> f)


@pytest.mark.asyncio
async def test_monad_left_identity() -> None:
    n: int = 3

    def f(n: int) -> Future[int]:
        return Future.pure(n * 3)

    m: Future[int] = Future.pure(n)
    assert await m.bind(f) == await f(n)


@pytest.mark.asyncio
async def test_monad_right_identity() -> None:
    assert await Future.pure(3) == await Future.pure(3).bind(lambda x: Future.pure(x))


@pytest.mark.asyncio
async def test_monad_associativity() -> None:
    def f(n: int) -> Future[int]:
        return Future.pure(n * 3)

    def g(n: int) -> Future[int]:
        return Future.pure(n + 5)

    assert await Future.pure(3).bind(f).bind(g) == await Future.pure(3).bind(
        lambda x: f(x).bind(g)
    )
