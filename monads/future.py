from __future__ import annotations
import functools
from typing import Awaitable, Callable, Iterable, List, TypeVar, Union
from .monad import Monad

T = TypeVar("T")
S = TypeVar("S")


class Future(Monad[T]):
    """Wraps an Awaitable in a Monad.

    The resulting Future object is, itself, Awaitable.
    """

    def __init__(self, awaitable: Awaitable[T]) -> None:
        self.awaitable = awaitable

    @classmethod
    def pure(cls, value: T) -> Future[T]:
        async def identity(x: T) -> T:
            return x

        return Future(identity(value))

    def map(self, function: Callable[[T], S]) -> Future[S]:
        async def map(f: Callable[[T], S], x: Awaitable[T]) -> S:
            x_ = await x
            return f(x_)

        return Future(map(function, self.awaitable))

    def apply(self, functor: Awaitable[Callable[[T], S]]) -> Future[S]:
        async def apply(f: Awaitable[Callable[[T], S]], x: Awaitable[T]) -> S:
            f_ = await f
            x_ = await x
            return f_(x_)

        return Future(apply(functor, self.awaitable))

    def bind(self, function: Callable[[T], Awaitable[S]]) -> Future[S]:
        async def bind(f: Callable[[T], Awaitable[S]], x: Awaitable[T]) -> S:
            x_ = await x
            y = await function(x_)
            return y

        return Future(bind(function, self.awaitable))

    @classmethod
    def sequence(cls, xs: Iterable[Awaitable[T]]) -> Future[List[T]]:
        """Evaluate monadic actions in sequence, collecting results."""

        def mcons(acc: Future[List[T]], x: Awaitable[T]) -> Future[List[T]]:
            future: Future[T] = x if isinstance(x, Future) else Future(x)
            return acc.bind(lambda acc_: future.map(lambda x_: acc_ + [x_]))

        empty: Future[List[T]] = cls.pure([])
        return functools.reduce(mcons, xs, empty)

    def __await__(self):
        return self.awaitable.__await__()

    __rshift__ = bind
    __and__ = lambda other, self: Future.apply(self, other)
    __mul__ = __rmul__ = map
