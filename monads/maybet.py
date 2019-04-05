from typing import Any, Awaitable, Callable, Generic, Type, TypeVar

from .monad import Monad
from . import maybe, future, result

T = TypeVar("T")
S = TypeVar("S")
E = TypeVar("E")


class MaybeT(Monad[T]):
    ...


class Maybe(MaybeT[T]):
    def __init__(self, value: maybe.Maybe[maybe.Maybe[T]]) -> None:
        self.value = value

    @classmethod
    def pure(cls, value: T) -> Maybe[T]:
        return Maybe(maybe.Maybe.pure(maybe.Maybe.pure(value)))

    def map(self, function: Callable[[T], S]) -> Maybe[S]:
        return Maybe(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], Maybe[S]]) -> Maybe[S]:
        def bind_inner(inner: maybe.Maybe[T]) -> maybe.Maybe[maybe.Maybe[S]]:
            if isinstance(inner, maybe.Just):
                return function(inner.value).value
            else:
                empty: maybe.Maybe[S] = maybe.Nothing()
                return maybe.Maybe.pure(empty)

        return Maybe(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<MaybeT<Maybe> {self.value}>"


class Result(MaybeT[T], Generic[T, E]):
    def __init__(self, value: result.Result[maybe.Maybe[T], E]) -> None:
        self.value = value

    @classmethod
    def pure(cls, value: T) -> Result[T, E]:
        return Result(result.Result.pure(maybe.Maybe.pure(value)))

    def map(self, function: Callable[[T], S]) -> Result[S, E]:
        return Result(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], Result[S, E]]) -> Result[S, E]:
        def bind_inner(inner: maybe.Maybe[T]) -> result.Result[maybe.Maybe[S], E]:
            if isinstance(inner, maybe.Just):
                return function(inner.value).value
            else:
                empty: maybe.Maybe[S] = maybe.Nothing()
                return result.Result.pure(empty)

        return Result(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<MaybeT<Result> {self.value}>"

    __rshift__ = bind
    __and__ = lambda other, self: Result.apply(self, other)
    __mul__ = __rmul__ = map


class Future(MaybeT[T]):
    def __init__(self, value: Awaitable[maybe.Maybe[T]]) -> None:
        self.value = future.Future(value)

    @classmethod
    def pure(cls, value: T) -> Future[T]:
        return Future(future.Future.pure(maybe.Maybe.pure(value)))

    def map(self, function: Callable[[T], S]) -> Future[S]:
        return Future(self.value.map(lambda inner: inner.map(function)))

    def bind(self, function: Callable[[T], Future[S]]) -> Future[S]:
        def bind_inner(inner: maybe.Maybe[T]) -> future.Future[maybe.Maybe[S]]:
            if isinstance(inner, maybe.Just):
                return function(inner.value).value
            else:
                empty: maybe.Maybe[S] = maybe.Nothing()
                return future.Future.pure(empty)

        return Future(self.value.bind(bind_inner))

    def __repr__(self):
        return f"<MaybeT<Future> {self.value}>"

    def __await__(self) -> Maybe[T]:
        return self.value.__await__()

    __rshift__ = bind
    __and__ = lambda other, self: Future.apply(self, other)
    __mul__ = __rmul__ = map
