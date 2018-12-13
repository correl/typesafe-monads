from __future__ import annotations
import asyncio
from typing import Awaitable, Callable, TypeVar, Union
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
    def pure(cls, value: Union[T, Awaitable[T]]) -> Future[T]:
        if isinstance(value, Awaitable):
            return Future(value)
        else:

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

    def __await__(self):
        return self.awaitable.__await__()

    __rshift__ = bind
    __and__ = lambda other, self: Future.apply(self, other)
    __mul__ = __rmul__ = map
